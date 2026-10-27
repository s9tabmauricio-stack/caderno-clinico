// Números da Central (Configurações → Central). Só roda no servidor, com a chave secreta.
import { clienteAdmin, ehAdmin } from '@/lib/admin'
import { agoraBrasilia } from '@/lib/agenda'
import { formatarCpf, cpfDoEmail } from '@/lib/cpf'

export type AlunoCentral = {
  id: string
  nome: string
  grupo: number | null
  admin: boolean
  ultimoAcesso: string | null
  diasSemEntrar: number | null
  questoes: number
  certas: number
  cards: number
}
export type DiaCentral = { dia: string; questoes: number; cards: number }
export type MateriaCentral = {
  id: string
  nome: string
  cor_inicio: string | null
  cor_fim: string | null
  aulas: number
  questoes: number
  cards: number
  aulas_sem_questoes: number
}
export type ErradaCentral = {
  id: string
  materia_id: string
  aula_id: string | null
  enunciado: string
  tentativas: number
  erros: number
  alunos: number
}
export type ProvaCentral = { titulo: string; data: string; inicio: string | null }

type Resumo = {
  alunos: { id: string; email: string | null; nome: string | null; grupo: number | null; ultimo_acesso: string | null; questoes: number; certas: number; cards: number }[]
  dias: DiaCentral[]
  materias: MateriaCentral[]
  erradas: ErradaCentral[]
  recados: { novos: number; erros_abertos: number }
  banco_bytes: number
}

/** Limite do banco no plano gratuito do Supabase. */
export const LIMITE_BANCO = 500 * 1024 * 1024
/** Quantos dias sem entrar para o aluno contar como "sumido". */
export const DIAS_SUMIDO = 7

const DIA = 86_400_000

/** Segunda-feira (AAAA-MM-DD) da semana de `data`, somando `semanas`. */
function segunda(data: string, semanas = 0) {
  const d = new Date(`${data}T12:00:00Z`)
  d.setUTCDate(d.getUTCDate() - ((d.getUTCDay() + 6) % 7) + 7 * semanas)
  return d.toISOString().slice(0, 10)
}

export type DadosCentral = Awaited<ReturnType<typeof carregarCentral>>

export async function carregarCentral() {
  const admin = await clienteAdmin()
  const { data: hoje, ms } = agoraBrasilia()
  const estaSemana = segunda(hoje)
  const proxima = segunda(hoje, 1)
  const [resumo, provas, semanas] = await Promise.all([
    admin.rpc('central_resumo'),
    admin
      .from('agenda_eventos')
      .select('titulo, data, inicio')
      .eq('fixo', true)
      .eq('tipo', 'prova')
      .gte('data', hoje)
      .order('data')
      .order('inicio'),
    admin.from('agenda_semanas').select('semana, texto').in('semana', [estaSemana, proxima]),
  ])
  if (resumo.error) throw new Error(`Não deu para ler os números da Central: ${resumo.error.message}`)
  const r = resumo.data as Resumo

  const alunos: AlunoCentral[] = r.alunos.map((a) => {
    const cpf = cpfDoEmail(a.email ?? '')
    return {
      id: a.id,
      nome: a.nome?.trim() || (cpf ? `CPF ${formatarCpf(cpf)}` : (a.email ?? 'Sem nome')),
      grupo: a.grupo,
      admin: ehAdmin(a.email ?? ''),
      ultimoAcesso: a.ultimo_acesso,
      diasSemEntrar: a.ultimo_acesso ? Math.floor((ms - new Date(a.ultimo_acesso).getTime()) / DIA) : null,
      questoes: Number(a.questoes),
      certas: Number(a.certas),
      cards: Number(a.cards),
    }
  })
  const publicada = (s: string) => Boolean(semanas.data?.some((x) => x.semana === s && x.texto?.trim()))

  return {
    hoje,
    agora: ms,
    alunos,
    dias: r.dias,
    materias: r.materias,
    erradas: r.erradas,
    recados: r.recados,
    bancoBytes: r.banco_bytes,
    provas: (provas.data ?? []) as ProvaCentral[],
    agenda: [
      { semana: estaSemana, publicada: publicada(estaSemana) },
      { semana: proxima, publicada: publicada(proxima) },
    ],
  }
}
