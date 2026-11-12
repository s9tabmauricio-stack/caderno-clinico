// O login é feito com CPF e senha. O Supabase exige um e-mail como identificador,
// então cada CPF vira um "e-mail interno" que nunca recebe mensagens.
export const DOMINIO_LOGIN = 'caderno-clinico.vercel.app'

export function soDigitos(v: string) {
  return v.replace(/\D/g, '').slice(0, 11)
}

export function formatarCpf(v: string) {
  const d = soDigitos(v)
  return d
    .replace(/^(\d{3})(\d)/, '$1.$2')
    .replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3')
    .replace(/\.(\d{3})(\d{1,2})$/, '.$1-$2')
}

export function cpfParaEmail(cpf: string) {
  return `${soDigitos(cpf)}@${DOMINIO_LOGIN}`
}

/** CPF a partir do e-mail interno; devolve null para contas de e-mail comum. */
export function cpfDoEmail(email: string) {
  const [local, dominio] = email.split('@')
  return dominio === DOMINIO_LOGIN && /^\d{11}$/.test(local) ? local : null
}

// Entrar com CPF ou e-mail (pedido do Mauricio, 12/11/2026). O e-mail é só um nome de
// usuário, como o CPF: a conta é criada já confirmada e o app nunca manda mensagem para ele.
const EMAIL_VALIDO = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

/** Formata enquanto digita: só números vira CPF com pontos; com letra ou @, fica como está. */
export function formatarLogin(v: string) {
  if (/[^\d.\-\s]/.test(v) || v.replace(/\D/g, '').length > 11) return v.trim()
  return formatarCpf(v)
}

/** Transforma o que a pessoa digitou (CPF ou e-mail) no e-mail que o Supabase usa. */
export function loginParaEmail(texto: string): { email: string; cpf: string | null } | { erro: string } {
  const v = texto.trim()
  if (v.includes('@')) {
    const email = v.toLowerCase()
    if (!EMAIL_VALIDO.test(email)) return { erro: 'E-mail incompleto. Confira o que foi digitado.' }
    return { email, cpf: cpfDoEmail(email) }
  }
  const cpf = soDigitos(v)
  if (v.replace(/\D/g, '').length !== 11) return { erro: 'Digite os 11 números do CPF ou o e-mail.' }
  return { email: cpfParaEmail(cpf), cpf }
}
