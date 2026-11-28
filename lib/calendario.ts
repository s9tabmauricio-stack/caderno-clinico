// Calendário acadêmico da FAG (tabela `calendario`, vale para todas as turmas).
// Funções puras: a Agenda e o Início usam para mostrar feriados, semanas de provas e o próximo marco.

export type Marco = { id: number; inicio: string; fim: string | null; tipo: string; titulo: string }

export const TIPOS_CALENDARIO: Record<string, { rotulo: string; emoji: string; cor: string }> = {
  feriado: { rotulo: 'Feriado', emoji: '🎉', cor: 'aviso' },
  recesso: { rotulo: 'Recesso', emoji: '🏖️', cor: 'aviso' },
  provas: { rotulo: 'Provas', emoji: '📝', cor: 'azul' },
  segunda_chamada: { rotulo: 'Segunda chamada', emoji: '📝', cor: 'azul' },
  exames: { rotulo: 'Exames', emoji: '📝', cor: 'azul' },
  semana_livre: { rotulo: 'Semana livre', emoji: '🌿', cor: 'verde' },
  letivo: { rotulo: 'Semestre', emoji: '🎓', cor: 'neutro' },
  evento: { rotulo: 'Evento', emoji: '📣', cor: 'roxo' },
  notas: { rotulo: 'Notas', emoji: '📊', cor: 'neutro' },
  docentes: { rotulo: 'Docentes', emoji: '👩‍🏫', cor: 'neutro' },
}

/** Tipos que valem aviso no dia da Agenda e no Início (prazos de nota e férias dos professores ficam só na lista do ano). */
const TIPOS_DESTAQUE = new Set(['feriado', 'recesso', 'provas', 'segunda_chamada', 'exames', 'semana_livre', 'letivo', 'evento'])

export const fimDo = (m: Marco) => m.fim ?? m.inicio

export function ehDestaque(m: Marco) {
  return TIPOS_DESTAQUE.has(m.tipo)
}

/** Marcos de destaque que valem num dia (AAAA-MM-DD). */
export function marcosDoDia(marcos: Marco[], data: string) {
  return marcos.filter((m) => ehDestaque(m) && m.inicio <= data && fimDo(m) >= data)
}

/** Marcos de destaque que tocam a semana de `segunda` a domingo. */
export function marcosDaSemana(marcos: Marco[], segunda: string) {
  const domingo = somarDias(segunda, 6)
  return marcos.filter((m) => ehDestaque(m) && m.inicio <= domingo && fimDo(m) >= segunda)
}

/** O que mostrar no Início: o que está valendo hoje (se houver) e o próximo marco que ainda vai começar. */
export function marcoDoInicio(marcos: Marco[], hoje: string) {
  const destaque = marcos.filter(ehDestaque).sort((a, b) => a.inicio.localeCompare(b.inicio))
  const agora = destaque.filter((m) => m.inicio <= hoje && fimDo(m) >= hoje)
  const proximo = destaque.find((m) => m.inicio > hoje) ?? null
  return { agora, proximo }
}

export function somarDias(data: string, n: number) {
  const d = new Date(`${data}T12:00:00Z`)
  d.setUTCDate(d.getUTCDate() + n)
  return d.toISOString().slice(0, 10)
}

export function diasEntre(de: string, ate: string) {
  return Math.round((Date.parse(`${ate}T12:00:00Z`) - Date.parse(`${de}T12:00:00Z`)) / 86_400_000)
}

const fmt = (data: string, o: Intl.DateTimeFormatOptions) =>
  new Intl.DateTimeFormat('pt-BR', { ...o, timeZone: 'UTC' }).format(new Date(`${data}T12:00:00Z`)).replace(/\./g, '')

/** "9 de fev" ou "5 a 16 de abr" ou "28 de jun a 2 de jul". */
export function fmtPeriodo(m: Marco) {
  const fim = fimDo(m)
  if (fim === m.inicio) return fmt(m.inicio, { day: 'numeric', month: 'short' })
  if (m.inicio.slice(0, 7) === fim.slice(0, 7)) return `${fmt(m.inicio, { day: 'numeric' })} a ${fmt(fim, { day: 'numeric', month: 'short' })}`
  return `${fmt(m.inicio, { day: 'numeric', month: 'short' })} a ${fmt(fim, { day: 'numeric', month: 'short' })}`
}

/** Dia da semana curto do início ("ter"), só para marcos de um dia. */
export function fmtDiaSemana(m: Marco) {
  return m.fim && m.fim !== m.inicio ? '' : fmt(m.inicio, { weekday: 'short' })
}

/** "hoje", "amanhã", "em 12 dias". */
export function fmtFalta(hoje: string, data: string) {
  const n = diasEntre(hoje, data)
  return n <= 0 ? 'hoje' : n === 1 ? 'amanhã' : `em ${n} dias`
}

/** Marcos agrupados por mês ("2027-04" → lista), em ordem. */
export function porMes(marcos: Marco[]) {
  const meses = new Map<string, Marco[]>()
  for (const m of [...marcos].sort((a, b) => a.inicio.localeCompare(b.inicio) || a.id - b.id)) {
    const k = m.inicio.slice(0, 7)
    meses.set(k, [...(meses.get(k) ?? []), m])
  }
  return [...meses.entries()]
}

export function nomeMes(chave: string) {
  const s = fmt(`${chave}-01`, { month: 'long', year: 'numeric' })
  return s.charAt(0).toUpperCase() + s.slice(1)
}
