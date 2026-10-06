'use server'

import { revalidatePath } from 'next/cache'
import { clienteAdmin } from '@/lib/admin'
import { cpfParaEmail, formatarCpf, soDigitos } from '@/lib/cpf'

export type Resultado = { ok: boolean; texto: string } | null

function lerCpfESenha(form: FormData) {
  const cpf = soDigitos(String(form.get('cpf') ?? ''))
  const senha = String(form.get('senha') ?? '')
  if (cpf.length !== 11) return { erro: 'Digite os 11 números do CPF.' }
  if (senha.length < 6) return { erro: 'A senha precisa ter pelo menos 6 caracteres.' }
  return { cpf, senha }
}

export async function criarAluno(_: Resultado, form: FormData): Promise<Resultado> {
  const dados = lerCpfESenha(form)
  if ('erro' in dados) return { ok: false, texto: dados.erro! }
  const nome = String(form.get('nome') ?? '').trim()
  try {
    const admin = await clienteAdmin()
    const { error } = await admin.auth.admin.createUser({
      email: cpfParaEmail(dados.cpf),
      password: dados.senha,
      email_confirm: true,
      user_metadata: nome ? { full_name: nome } : {},
    })
    if (error) {
      return {
        ok: false,
        texto: /already|registered|exists/i.test(error.message)
          ? 'Já existe um aluno com esse CPF.'
          : `Não deu para criar: ${error.message}`,
      }
    }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  revalidatePath('/admin')
  return { ok: true, texto: `Aluno ${nome || formatarCpf(dados.cpf)} criado. Ele já pode entrar com o CPF e a senha.` }
}

export async function trocarSenhaAluno(_: Resultado, form: FormData): Promise<Resultado> {
  const id = String(form.get('id') ?? '')
  const senha = String(form.get('senha') ?? '')
  if (!id) return { ok: false, texto: 'Escolha o aluno.' }
  if (senha.length < 6) return { ok: false, texto: 'A senha precisa ter pelo menos 6 caracteres.' }
  try {
    const admin = await clienteAdmin()
    const { error } = await admin.auth.admin.updateUserById(id, { password: senha })
    if (error) return { ok: false, texto: `Não deu para trocar: ${error.message}` }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  return { ok: true, texto: 'Senha trocada.' }
}
