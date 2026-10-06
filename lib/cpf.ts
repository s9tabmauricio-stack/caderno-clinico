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
