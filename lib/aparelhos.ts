// Limite de aparelhos por conta (perfis.max_aparelhos; gatilho limitar_aparelhos em auth.sessions).
// Quem entra num aparelho novo derruba o usado há mais tempo; aqui fica o que o app faz no aparelho derrubado.

/** Cookie que guarda qual sessão foi conferida por último e quando (segundos). */
export const COOKIE_APARELHO = 'mg_aparelho'

/** De quanto em quanto tempo o app pergunta ao banco se a sessão deste aparelho ainda existe. */
export const CONFERIR_A_CADA_S = 120

/** Valor de `?saiu=` na tela de entrada quando a conta entrou em outro aparelho. */
export const SAIU_OUTRO_APARELHO = 'aparelho'

export function valorCookieAparelho(sessaoId: string, agoraS: number): string {
  return `${sessaoId}.${Math.floor(agoraS)}`
}

/** Precisa perguntar ao banco? Sim se nunca conferiu esta sessão ou se já passou o intervalo. */
export function precisaConferir(cookie: string | undefined, sessaoId: string, agoraS: number): boolean {
  if (!cookie) return true
  const ponto = cookie.lastIndexOf('.')
  if (ponto < 1 || cookie.slice(0, ponto) !== sessaoId) return true
  const quando = Number(cookie.slice(ponto + 1))
  if (!Number.isFinite(quando) || quando > agoraS + 60) return true
  return agoraS - quando >= CONFERIR_A_CADA_S
}

/** Texto do limite para a Administração. */
export function rotuloLimite(max: number | null): string {
  if (max === null) return 'sem limite de aparelhos'
  return max === 1 ? '1 aparelho' : `até ${max} aparelhos`
}
