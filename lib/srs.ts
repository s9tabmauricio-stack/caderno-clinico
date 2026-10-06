// Repetição espaçada: variação simples do algoritmo do Anki (SM-2).
// O card que o aluno erra volta em minutos; o que ele acerta volta em dias,
// e o intervalo cresce a cada acerto conforme a "facilidade" do card.

export type EstadoCard = {
  repeticoes: number
  intervalo_dias: number
  facilidade: number
  lapsos: number
  proxima_revisao: string
  ultima_revisao: string
}

export type Nota = 0 | 1 | 2 | 3 // Errei, Difícil, Bom, Fácil

const DIA = 86_400_000
const MINUTO = 60_000
const arred = (n: number) => Math.round(n * 100) / 100

export function intervalos(s: EstadoCard | null) {
  if (!s || s.repeticoes === 0) return { dificil: 0.5, bom: 1, facil: 4 }
  if (s.repeticoes === 1) return { dificil: 1, bom: 3, facil: 6 }
  const dificil = Math.max(1, Math.round(s.intervalo_dias * 1.2))
  const bom = Math.max(dificil + 1, Math.round(s.intervalo_dias * s.facilidade))
  const facil = Math.max(bom + 1, Math.round(s.intervalo_dias * s.facilidade * 1.3))
  return { dificil, bom, facil }
}

export function avaliar(s: EstadoCard | null, nota: Nota, agora = Date.now()): EstadoCard {
  const base = s ?? { repeticoes: 0, intervalo_dias: 0, facilidade: 2.5, lapsos: 0 }
  const ultima_revisao = new Date(agora).toISOString()

  if (nota === 0) {
    return {
      repeticoes: 0,
      intervalo_dias: 0,
      facilidade: Math.max(1.3, arred(base.facilidade - 0.2)),
      lapsos: base.lapsos + 1,
      proxima_revisao: new Date(agora + 10 * MINUTO).toISOString(),
      ultima_revisao,
    }
  }

  const iv = intervalos(s)
  const dias = nota === 1 ? iv.dificil : nota === 2 ? iv.bom : iv.facil
  const facilidade =
    nota === 1 ? Math.max(1.3, arred(base.facilidade - 0.15)) : nota === 3 ? arred(base.facilidade + 0.15) : base.facilidade

  return {
    repeticoes: base.repeticoes + 1,
    intervalo_dias: dias,
    facilidade,
    lapsos: base.lapsos,
    proxima_revisao: new Date(agora + dias * DIA).toISOString(),
    ultima_revisao,
  }
}

export function vencido(s: EstadoCard | null, agora = Date.now()) {
  return s !== null && new Date(s.proxima_revisao).getTime() <= agora
}
