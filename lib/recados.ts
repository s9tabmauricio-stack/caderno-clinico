// Recados da turma: textos comuns à conversa embaixo da questão e à tela do administrador

export type Recado = {
  id: string
  questao_id: string
  user_id: string
  autor: string
  tipo: string
  texto: string
  status: string
  criado_em: string
}

// Quem cuida dos avisos de erro (aparece para a turma)
export const NOME_ADMIN = 'Mauricio'

/** "Augusto deixou uma dica" / "Augusto achou um erro" (sem artigo, vale para qualquer nome) */
export const tituloRecado = (r: Pick<Recado, 'autor' | 'tipo'>) =>
  r.tipo === 'erro' ? `${r.autor} achou um erro` : `${r.autor} deixou uma dica`

export function situacaoErro(status: string) {
  if (status === 'corrigido') return { texto: `✓ Corrigido pelo ${NOME_ADMIN}`, cls: 'ok' }
  if (status === 'visto') return { texto: `${NOME_ADMIN} está vendo`, cls: 'vendo' }
  return { texto: `Aguardando o ${NOME_ADMIN}`, cls: 'espera' }
}

/** "agora", "há 5 min", "há 2 h", "ontem", "há 3 dias", "12/09" */
export function fmtHa(iso: string, agora = Date.now()) {
  const min = Math.floor((agora - new Date(iso).getTime()) / 60_000)
  if (min < 1) return 'agora'
  if (min < 60) return `há ${min} min`
  const h = Math.floor(min / 60)
  if (h < 24) return `há ${h} h`
  const d = Math.floor(h / 24)
  if (d === 1) return 'ontem'
  if (d < 30) return `há ${d} dias`
  return new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: '2-digit', timeZone: 'America/Sao_Paulo' }).format(new Date(iso))
}

export const primeiroNome = (nome: string | null | undefined) => nome?.trim().split(/\s+/)[0] || 'Colega'
