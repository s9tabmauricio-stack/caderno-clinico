// Separa o texto "por que as outras estão erradas" em uma explicação por alternativa.
// Aceita linhas como "A: ...", "A, C e E: ..." e cabeçalhos como "A, B, C e D são verdadeiras:".

const LETRAS = 'ABCDE'
const GRUPO = /^\s*([A-E](?:\s*(?:,|e)\s*[A-E])*)\s*:\s*(.+)$/
const CABECALHO = /^\s*([A-E](?:\s*(?:,|e)\s*[A-E])+)\s+(.+)$/

function letrasDe(s: string) {
  return (s.match(/[A-E]/g) ?? []).map((l) => LETRAS.indexOf(l))
}
function maiuscula(s: string) {
  const t = s.trim()
  return t.charAt(0).toUpperCase() + t.slice(1)
}

export function explicacoesPorAlternativa(texto: string | null) {
  const porAlt: Record<number, string[]> = {}
  const resto: string[] = []
  if (!texto) return { porAlt: {} as Record<number, string>, resto: '' }
  const linhas = texto.split('\n').map((l) => l.trim()).filter(Boolean)
  const individuais = new Set<number>()
  for (const l of linhas) {
    const g = l.match(GRUPO)
    if (g && letrasDe(g[1]).length === 1) individuais.add(letrasDe(g[1])[0])
  }
  for (const l of linhas) {
    const g = l.match(GRUPO)
    if (g) {
      for (const i of letrasDe(g[1])) (porAlt[i] ??= []).push(maiuscula(g[2]))
      continue
    }
    const c = l.match(CABECALHO)
    if (c) {
      const ls = letrasDe(c[1])
      // Cabeçalho seguido de linhas por letra ("A, B e C são verdadeiras:") não precisa se repetir
      if (ls.every((i) => individuais.has(i))) continue
      for (const i of ls) (porAlt[i] ??= []).push(maiuscula(c[2].replace(/:$/, '.')))
      continue
    }
    resto.push(l)
  }
  return {
    porAlt: Object.fromEntries(Object.entries(porAlt).map(([k, v]) => [Number(k), v.join(' ')])) as Record<number, string>,
    resto: resto.join('\n'),
  }
}
