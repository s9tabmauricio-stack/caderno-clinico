// Pequenos ajudantes de texto em português

export const FUSO = 'America/Sao_Paulo'

// Quantos cards novos entram por sessão de revisão (como o limite diário do Anki)
export const LIMITE_NOVOS = 20

export const plural = (n: number, um: string, varios: string) => (n === 1 ? um : varios)

export function fmtIntervalo(dias: number) {
  if (dias < 1 / 24) return `${Math.max(1, Math.round(dias * 1440))} min`
  if (dias < 1) return `${Math.round(dias * 24)} h`
  const d = Math.round(dias)
  if (d < 30) return `${d} ${plural(d, 'dia', 'dias')}`
  const m = Math.round(d / 30)
  return `${m} ${plural(m, 'mês', 'meses')}`
}

export function fmtQuando(iso: string, agora = Date.now()) {
  const dias = (new Date(iso).getTime() - agora) / 86_400_000
  if (dias <= 0) return 'agora'
  if (dias >= 0.75 && dias < 1.5) return 'amanhã'
  return `em ${fmtIntervalo(dias)}`
}

export function saudacao(agora = new Date()) {
  const hora = Number(new Intl.DateTimeFormat('pt-BR', { hour: 'numeric', hourCycle: 'h23', timeZone: FUSO }).format(agora))
  const texto = hora < 12 ? 'Bom dia' : hora < 18 ? 'Boa tarde' : 'Boa noite'
  const data = new Intl.DateTimeFormat('pt-BR', { weekday: 'long', day: 'numeric', month: 'long', timeZone: FUSO }).format(agora)
  return { texto, data }
}

export const pct = (parte: number, total: number) => (total ? Math.round((100 * parte) / total) : 0)
