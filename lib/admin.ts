// Só roda no servidor: usa a chave secreta do Supabase para criar alunos e trocar senhas.
import { createClient } from '@supabase/supabase-js'
import { SUPABASE_URL } from '@/lib/supabase/config'
import { cpfDoEmail } from '@/lib/cpf'
import { sessao } from '@/lib/dados'

// CPFs que podem abrir a página de administrador (dá para trocar pela variável ADMIN_CPFS na Vercel)
const ADMINS = (process.env.ADMIN_CPFS ?? '08699426623').split(',').map((c) => c.replace(/\D/g, ''))

export function ehAdmin(email: string) {
  const cpf = cpfDoEmail(email)
  return cpf !== null && ADMINS.includes(cpf)
}

export function chaveConfigurada() {
  return Boolean(process.env.SUPABASE_SECRET_KEY)
}

/** Confere se quem chamou é administrador e devolve o cliente com a chave secreta. */
export async function clienteAdmin() {
  const { email } = await sessao()
  if (!ehAdmin(email)) throw new Error('Sem permissão.')
  const chave = process.env.SUPABASE_SECRET_KEY
  if (!chave) throw new Error('A chave secreta não está configurada na Vercel.')
  return createClient(SUPABASE_URL, chave, { auth: { persistSession: false, autoRefreshToken: false } })
}
