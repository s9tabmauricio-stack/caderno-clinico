// Agenda da turma: lê o cronograma no formato que chega no WhatsApp e ajuda as telas a mostrar o dia e a semana.

export type EventoAgenda = {
  data: string // AAAA-MM-DD
  inicio: string | null // HH:MM
  fim: string | null
  materia: string | null
  tipo: 'pratica' | 'teorica' | 'seminario' | 'prova' | 'aviso' | 'aula'
  titulo: string
  professor: string | null
  local: string | null
  grupos: number[] | null // null = turma toda
  cancelado: boolean
  notas: string[]
  ordem: number
}

export type SemanaLida = {
  semana: string // segunda-feira, AAAA-MM-DD
  titulo: string | null
  aviso: string | null
  eventos: EventoAgenda[]
  dias: string[]
}

const MESES: Record<string, number> = {
  janeiro: 1, fevereiro: 2, marco: 3, março: 3, abril: 4, maio: 5, junho: 6,
  julho: 7, agosto: 8, setembro: 9, outubro: 10, novembro: 11, dezembro: 12,
}

const EMOJI_MATERIA: [string, string][] = [
  ['🫁', 'pneumo'], ['🍽', 'gastro'], ['🚰', 'nefro'], ['🚻', 'uro'], ['🦴', 'orto'],
  ['🥼', 'pass'], ['🗣', 'sem'], ['🩸', 'angio'],
]
const PALAVRA_MATERIA: [RegExp, string][] = [
  [/pneumo/i, 'pneumo'], [/gastro/i, 'gastro'], [/nefro/i, 'nefro'], [/urolog/i, 'uro'],
  [/ortop/i, 'orto'], [/\bPASS\b/, 'pass'], [/angio/i, 'angio'], [/semin[aá]rio/i, 'sem'],
]

export const NOME_MATERIA: Record<string, string> = {
  pneumo: 'Pneumologia', gastro: 'Gastroenterologia', nefro: 'Nefrologia', uro: 'Urologia',
  orto: 'Ortopedia', pass: 'PASS', sem: 'Seminário', angio: 'Angiologia',
}
export const COR_MATERIA: Record<string, string> = {
  pneumo: '#4FDDFF', gastro: '#3EE6A8', nefro: '#6A8BFF', uro: '#B07BFF',
  orto: '#FFB547', pass: '#FF5CD6', sem: '#9AA3BD', angio: '#FF5C8A',
}

const DIA_SEMANA = /^\s*(segunda|ter[cç]a|quarta|quinta|sexta|s[aá]bado|domingo)(?:-feira)?\s*\|\s*(\d{1,2})\s*\/\s*([a-zç]+|\d{1,2})/i
const HORARIO = /^(\d{1,2})h(\d{2})?(?:\s*[-–a]\s*(\d{1,2})h(\d{2})?)?\s*:\s*(.+)$/i
const MARCADOR = /^[\s\u2060]*[-*•·]\s*[\u2060]?\s*/

function hora(h?: string, m?: string) {
  return h ? `${h.padStart(2, '0')}:${(m ?? '00').padStart(2, '0')}` : null
}
function semAcento(s: string) {
  return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '')
}
function limparEmoji(s: string) {
  return s.replace(/^[^\p{L}\p{N}]+/u, '').trim()
}
function materiaDe(linha: string, texto: string) {
  for (const [r, m] of PALAVRA_MATERIA) if (r.test(texto)) return m
  for (const [e, m] of EMOJI_MATERIA) if (linha.includes(e)) return m
  return null
}
function gruposDe(texto: string): number[] | null {
  const m = texto.match(/\bgrupos?\s+((?:\d+\s*(?:,|e)?\s*)+)/i)
  if (!m) return null
  const ns = (m[1].match(/\d+/g) ?? []).map(Number)
  return ns.length ? ns : null
}
function segunda(iso: string) {
  const d = new Date(`${iso}T12:00:00Z`)
  const dia = d.getUTCDay() || 7
  d.setUTCDate(d.getUTCDate() - (dia - 1))
  return d.toISOString().slice(0, 10)
}
function primeiraMaiuscula(s: string) {
  return s.charAt(0).toUpperCase() + s.slice(1)
}

/** Separa título, professor e local de "aula prática de X para o grupo 2 com Dra. Fulana no CAE." */
function destrinchar(textoBruto: string) {
  let t = textoBruto.trim().replace(/[.!]+$/, '')
  let local: string | null = null
  let professor: string | null = null
  const prof = t.match(/\s+com\s+(?:[oa]\s+)?((?:Dr|Dra|Prof|Profa)\.?\s.+)$/i)
  if (prof) {
    t = t.slice(0, prof.index)
    professor = prof[1]
    const lugar = professor.match(/\s+n[oa]s?\s+(.+)$/i)
    if (lugar) {
      local = lugar[1]
      professor = professor.slice(0, lugar.index)
    }
  } else {
    const lugar = t.match(/\s+n[oa]s?\s+((?:auditório|ambulatório|CAE|CISOP|Renalclin|\d|Instituto|sala|HSL|bloco).*)$/i)
    if (lugar) {
      local = lugar[1]
      t = t.slice(0, lugar.index)
    }
  }
  const grupos = gruposDe(t)
  t = t.replace(/\s+para\s+(?:o|os)\s+grupos?\s+.*$/i, '')
  t = t.replace(/^aula\s+/i, '')
  if (local) local = primeiraMaiuscula(local.replace(/^d[oa]\s+/i, ''))
  return { titulo: primeiraMaiuscula(t.trim()), professor: professor?.trim() ?? null, local, grupos }
}

function tipoDe(texto: string): EventoAgenda['tipo'] {
  const s = semAcento(texto.toLowerCase())
  if (/vista d[ae] prova|prova/.test(s) && !/teorica/.test(s)) return 'prova'
  if (/pratica/.test(s)) return 'pratica'
  if (/teorica/.test(s)) return 'teorica'
  if (/seminario/.test(s)) return 'seminario'
  return 'aula'
}

/** Lê o texto do cronograma semanal colado do WhatsApp. */
export function lerCronograma(texto: string, ano = new Date().getFullYear()): SemanaLida {
  const linhas = texto.replace(/\r/g, '').split('\n')
  const eventos: EventoAgenda[] = []
  const dias: string[] = []
  let titulo: string | null = null
  let aviso: string | null = null
  let data: string | null = null
  let ultimo: EventoAgenda | null = null
  let vazioDesdeUltimo = false
  let ordem = 0
  const letras: Record<string, Record<string, [number, number]>> = {}

  for (const bruta of linhas) {
    const linha = bruta.trim()
    if (!linha) {
      vazioDesdeUltimo = true
      continue
    }

    const dia = linha.match(DIA_SEMANA)
    if (dia) {
      const n = Number(dia[2])
      const mesTxt = semAcento(dia[3].toLowerCase())
      const mes = /^\d+$/.test(mesTxt) ? Number(mesTxt) : (MESES[mesTxt] ?? MESES[dia[3].toLowerCase()])
      data = `${ano}-${String(mes).padStart(2, '0')}-${String(n).padStart(2, '0')}`
      dias.push(data)
      ultimo = null
      continue
    }

    if (!data) {
      // Cabeçalho da semana
      if (/observa[cç][aã]o/i.test(linha)) aviso = limparEmoji(linha).replace(/^observa[cç][aã]o:\s*/i, '')
      else if (!titulo && /cronograma/i.test(linha)) titulo = limparEmoji(linha)
      continue
    }

    // Grupos por letra: "- A = práticas 1 a 7"
    const mapa = linha.replace(MARCADOR, '').match(/^([A-Z])\s*=\s*pr[aá]ticas?\s*(\d+)\s*a\s*(\d+)/i)
    if (mapa) {
      ;(letras[data] ??= {})[mapa[1].toUpperCase()] = [Number(mapa[2]), Number(mapa[3])]
    }

    const semEmoji = limparEmoji(linha)
    const h = semEmoji.match(HORARIO)
    if (h) {
      const corpo = h[5]
      const d = destrinchar(corpo)
      ultimo = {
        data,
        inicio: hora(h[1], h[2]),
        fim: hora(h[3], h[4]),
        materia: materiaDe(linha, corpo),
        tipo: tipoDe(corpo),
        titulo: d.titulo,
        professor: d.professor,
        local: d.local,
        grupos: d.grupos,
        cancelado: false,
        notas: [],
        ordem: ordem++,
      }
      eventos.push(ultimo)
      vazioDesdeUltimo = false
      continue
    }

    if (linha.startsWith('❌')) {
      const corpo = semEmoji.replace(/^n[aã]o\s+haver[aá]\s+/i, '')
      const d = destrinchar(corpo)
      ultimo = {
        data,
        inicio: null,
        fim: null,
        materia: materiaDe(linha, corpo),
        tipo: tipoDe(corpo),
        titulo: d.titulo,
        professor: d.professor,
        local: d.local,
        grupos: d.grupos,
        cancelado: true,
        notas: [],
        ordem: ordem++,
      }
      eventos.push(ultimo)
      vazioDesdeUltimo = false
      continue
    }

    const ehMarcador = MARCADOR.test(bruta) && /^[\s\u2060]*[-*•·]/.test(bruta)
    const nota = linha.replace(MARCADOR, '').replace(/^\u2060/, '').trim()
    if (ehMarcador && ultimo && (!vazioDesdeUltimo || ultimo.tipo === 'aviso')) {
      ultimo.notas.push(nota)
      continue
    }
    // Texto solto: vira um aviso do dia
    if (ultimo && ultimo.tipo === 'aviso' && !vazioDesdeUltimo) {
      ultimo.notas.push(nota)
    } else {
      ultimo = {
        data, inicio: null, fim: null, materia: null, tipo: 'aviso', titulo: nota, professor: null, local: null,
        grupos: null, cancelado: false, notas: [], ordem: ordem++,
      }
      eventos.push(ultimo)
    }
    vazioDesdeUltimo = false
  }

  // Aulas divididas por letra ("Grupo A: Dr. Eduardo") valem para os grupos daquelas letras
  for (const ev of eventos) {
    const mapaDia = letras[ev.data]
    if (!mapaDia || ev.grupos) continue
    const usadas = ev.notas.flatMap((n) => [...n.matchAll(/\bGrupo\s+([A-Z])\b/g)].map((m) => m[1]))
    if (!usadas.length) continue
    const gs = new Set<number>()
    for (const l of usadas) {
      const r = mapaDia[l]
      if (r) for (let i = r[0]; i <= r[1]; i++) gs.add(i)
    }
    if (gs.size) ev.grupos = [...gs].sort((a, b) => a - b)
  }

  const primeira = dias[0] ?? new Date().toISOString().slice(0, 10)
  return { semana: segunda(primeira), titulo, aviso, eventos, dias }
}

// ---------- Ajudas para as telas ----------

export const FUSO_AGENDA = 'America/Sao_Paulo'

/** Data (AAAA-MM-DD) e minutos do dia agora, no horário de Brasília. */
export function agoraBrasilia(base = new Date()) {
  const p = Object.fromEntries(
    new Intl.DateTimeFormat('en-CA', { timeZone: FUSO_AGENDA, year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' })
      .formatToParts(base)
      .map((x) => [x.type, x.value]),
  )
  return { data: `${p.year}-${p.month}-${p.day}`, minutos: Number(p.hour) * 60 + Number(p.minute) }
}

export function minutos(h: string | null) {
  if (!h) return null
  const [a, b] = h.split(':').map(Number)
  return a * 60 + b
}

/** "07:30" → "7h30", "08:00" → "8h" */
export function fmtHora(h: string | null) {
  if (!h) return ''
  const [a, b] = h.split(':')
  return `${Number(a)}h${b === '00' ? '' : b}`
}

export function fmtFalta(min: number) {
  if (min < 60) return `Em ${min} min`
  const h = Math.floor(min / 60)
  const m = min % 60
  return m ? `Em ${h}h${String(m).padStart(2, '0')}` : `Em ${h}h`
}

export type Situacao = 'passou' | 'agora' | 'proxima' | 'depois'

/** Situação de cada aula do dia de hoje (a primeira que ainda vai começar é a "próxima"). */
export function situacoes<T extends { inicio: string | null; fim: string | null; cancelado: boolean; tipo: string }>(
  eventos: T[],
  agoraMin: number,
) {
  let achouProxima = false
  return eventos.map((e) => {
    const ini = minutos(e.inicio)
    if (e.cancelado || e.tipo === 'aviso' || ini === null) return { evento: e, situacao: 'depois' as Situacao, falta: 0 }
    const fim = minutos(e.fim) ?? ini + 60
    if (agoraMin >= fim) return { evento: e, situacao: 'passou' as Situacao, falta: 0 }
    if (agoraMin >= ini) return { evento: e, situacao: 'agora' as Situacao, falta: 0 }
    if (!achouProxima) {
      achouProxima = true
      return { evento: e, situacao: 'proxima' as Situacao, falta: ini - agoraMin }
    }
    return { evento: e, situacao: 'depois' as Situacao, falta: ini - agoraMin }
  })
}

/** A aula vale para o aluno? (teóricas e avisos valem para todos) */
export function ehDoAluno(grupos: number[] | null, grupo: number | null) {
  return !grupos || !grupos.length || grupo === null || grupos.includes(grupo)
}
