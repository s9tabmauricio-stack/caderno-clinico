import type { createClient } from '@/lib/supabase/client'

export type Falha = { texto: string; sessao: boolean }

// Explica, em palavras do aluno, por que uma gravação no banco não deu certo:
// sem internet, sessão expirada (precisa entrar de novo) ou outro motivo.
// `oQue` completa a frase, ex.: "esta resposta", "a última revisão".
export async function explicarFalha(supabase: ReturnType<typeof createClient>, oQue: string): Promise<Falha> {
  if (typeof navigator !== 'undefined' && !navigator.onLine) {
    return { texto: `Você está sem internet, então ${oQue} não foi salva.`, sessao: false }
  }
  const { data, error } = await supabase.auth.getUser()
  if (!data.user && (!error || error.status === 401 || error.status === 403 || /session|jwt|token/i.test(error.message))) {
    return { texto: `Sua sessão expirou, então ${oQue} não foi salva. Entre de novo para continuar.`, sessao: true }
  }
  return { texto: `Não deu para salvar ${oQue}. Confira a internet.`, sessao: false }
}
