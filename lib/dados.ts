import { redirect } from 'next/navigation'
import { createClient, type SupabaseServidor } from '@/lib/supabase/server'
import type { EstadoCard } from '@/lib/srs'
import { LIMITE_NOVOS } from '@/lib/formato'
import type { Json } from '@/lib/database.types'

// ---------- Tipos usados nas telas ----------
export type Materia = {
  id: string
  nome: string
  descricao: string | null
  ordem: number
  cor_inicio: string | null
  cor_fim: string | null
}

export type ProgressoAula = {
  aula_id: string
  materia_id: string
  ordem: number
  titulo: string
  total_questoes: number
  respondidas: number
  acertos: number
  total_cards: number
  cards_estudados: number
  cards_vencidos: number
  ultima_atividade: string | null
}

export type QuestaoAluno = {
  id: string
  ordem: number
  enunciado: string
  alternativas: string[]
  correta: number
  comentario: string | null
  resposta: { escolhida: number; acertou: boolean; tentativas: number } | null
}

export type CardAluno = {
  id: string
  aula_id: string
  frente: string
  verso: string
  aula_titulo: string
  materia_id: string
  materia_nome: string
  estado: EstadoCard | null
}

// ---------- Sessão ----------
export async function sessao() {
  const supabase = await createClient()
  const { data } = await supabase.auth.getClaims()
  const claims = data?.claims
  if (!claims) redirect('/login')
  return { supabase, userId: claims.sub, email: typeof claims.email === 'string' ? claims.email : '' }
}

function falhou(contexto: string, error: { message: string }): never {
  throw new Error(`Não foi possível carregar ${contexto}: ${error.message}`)
}

// ---------- Leituras ----------
export async function carregarMaterias(supabase: SupabaseServidor): Promise<Materia[]> {
  const { data, error } = await supabase
    .from('materias')
    .select('id, nome, descricao, ordem, cor_inicio, cor_fim')
    .order('ordem')
  if (error) falhou('as matérias', error)
  return data ?? []
}

export async function carregarProgresso(supabase: SupabaseServidor): Promise<ProgressoAula[]> {
  const { data, error } = await supabase.from('progresso_aulas').select('*').order('ordem')
  if (error) falhou('o progresso', error)
  return (data ?? []).map((p) => ({
    aula_id: p.aula_id ?? '',
    materia_id: p.materia_id ?? '',
    ordem: p.ordem ?? 0,
    titulo: p.titulo ?? '',
    total_questoes: p.total_questoes ?? 0,
    respondidas: p.respondidas ?? 0,
    acertos: p.acertos ?? 0,
    total_cards: p.total_cards ?? 0,
    cards_estudados: p.cards_estudados ?? 0,
    cards_vencidos: p.cards_vencidos ?? 0,
    ultima_atividade: p.ultima_atividade,
  }))
}

type LinhaQuestao = {
  id: string | null
  ordem: number | null
  enunciado: string | null
  alternativas: Json | null
  correta: number | null
  comentario: string | null
  escolhida: number | null
  acertou: boolean | null
  tentativas: number | null
}

export function paraQuestao(q: LinhaQuestao): QuestaoAluno {
  return {
    id: q.id ?? '',
    ordem: q.ordem ?? 0,
    enunciado: q.enunciado ?? '',
    alternativas: Array.isArray(q.alternativas) ? q.alternativas.map(String) : [],
    correta: q.correta ?? 0,
    comentario: q.comentario,
    resposta:
      q.escolhida !== null && q.acertou !== null
        ? { escolhida: q.escolhida, acertou: q.acertou, tentativas: q.tentativas ?? 1 }
        : null,
  }
}

type LinhaCard = {
  id: string | null
  aula_id: string | null
  frente: string | null
  verso: string | null
  aula_titulo: string | null
  materia_id: string | null
  materia_nome: string | null
  repeticoes: number | null
  intervalo_dias: number | null
  facilidade: number | null
  lapsos: number | null
  proxima_revisao: string | null
  ultima_revisao: string | null
}

export function paraCard(c: LinhaCard): CardAluno {
  return {
    id: c.id ?? '',
    aula_id: c.aula_id ?? '',
    frente: c.frente ?? '',
    verso: c.verso ?? '',
    aula_titulo: c.aula_titulo ?? '',
    materia_id: c.materia_id ?? '',
    materia_nome: c.materia_nome ?? '',
    estado: c.proxima_revisao
      ? {
          repeticoes: c.repeticoes ?? 0,
          intervalo_dias: c.intervalo_dias ?? 0,
          facilidade: c.facilidade ?? 2.5,
          lapsos: c.lapsos ?? 0,
          proxima_revisao: c.proxima_revisao,
          ultima_revisao: c.ultima_revisao ?? c.proxima_revisao,
        }
      : null,
  }
}

// ---------- Contas ----------
export function totais(prog: ProgressoAula[]) {
  return prog.reduce(
    (t, p) => ({
      questoes: t.questoes + p.total_questoes,
      respondidas: t.respondidas + p.respondidas,
      acertos: t.acertos + p.acertos,
      cards: t.cards + p.total_cards,
      estudados: t.estudados + p.cards_estudados,
      vencidos: t.vencidos + p.cards_vencidos,
    }),
    { questoes: 0, respondidas: 0, acertos: 0, cards: 0, estudados: 0, vencidos: 0 },
  )
}

// Cards para hoje: os vencidos mais até LIMITE_NOVOS cards novos
export function pendentes(prog: ProgressoAula[]) {
  const t = totais(prog)
  const novos = t.cards - t.estudados
  return { vencidos: t.vencidos, novos, hoje: t.vencidos + Math.min(novos, LIMITE_NOVOS), emDia: t.estudados - t.vencidos }
}

export function concluido(prog: ProgressoAula[]) {
  const t = totais(prog)
  const total = t.questoes + t.cards
  return total ? Math.round((100 * (t.respondidas + t.estudados)) / total) : 0
}
