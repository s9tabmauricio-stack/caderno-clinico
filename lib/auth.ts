/** Só as telas de autenticação ficam abertas sem sessão, mais a rota do robô do Gmail (que tem chave própria). */
export function rotaPublica(pathname: string): boolean {
  return pathname === '/login' || pathname === '/auth' || pathname.startsWith('/auth/') || pathname === '/api/contas-gmail'
}

/** Valida o retorno do login, inclusive barras e controles codificados. */
export function destinoAposLogin(valor: unknown): string {
  if (typeof valor !== 'string' || valor.length > 2000) return '/'
  try {
    const decodificado = decodeURIComponent(valor)
    if (!decodificado.startsWith('/') || decodificado.startsWith('//') || /[\\\x00-\x1f\x7f]/.test(decodificado)) return '/'
    const url = new URL(valor, 'https://medgenius.local')
    const caminho = new URL(decodificado, 'https://medgenius.local').pathname
    if (url.origin !== 'https://medgenius.local' || rotaPublica(caminho)) return '/'
    return `${url.pathname}${url.search}${url.hash}`
  } catch {
    return '/'
  }
}
