/** Retornos internos permitidos; nunca aceita URLs externas ou protocolos. */
export function retornoSeguro(valor: unknown): string | null {
  if (typeof valor !== 'string' || valor.length > 2000 || /[\\\r\n]/.test(valor)) return null
  if (!/^\/(?:estudar|desempenho|materia\/[\w-]+(?:\/(?:questoes|flashcards))?|aula\/[\w-]+)(?:[?#]|$)/.test(valor)) return null
  const url = new URL(valor, 'https://medgenius.local')
  if (url.origin !== 'https://medgenius.local') return null
  return `${url.pathname}${url.search}${url.hash}`
}

export function rotuloRetorno(href: string): string {
  if (href.startsWith('/estudar')) return 'Matérias'
  if (href.startsWith('/desempenho')) return 'Desempenho'
  if (href.startsWith('/aula/')) return 'Aula'
  return 'Matéria'
}
