'use server'

import { revalidatePath } from 'next/cache'
import { clienteAdmin } from '@/lib/admin'
import { DOMINIO_LOGIN, formatarCpf, loginParaEmail } from '@/lib/cpf'

export type Resultado = { ok: boolean; texto: string } | null

/** Lê o CPF ou o e-mail do aluno novo (o e-mail é só nome de usuário, nunca recebe mensagem). */
function lerLoginESenha(form: FormData) {
  const login = loginParaEmail(String(form.get('cpf') ?? ''))
  const senha = String(form.get('senha') ?? '')
  if ('erro' in login) return { erro: login.erro }
  if (!login.cpf && login.email.endsWith(`@${DOMINIO_LOGIN}`)) return { erro: 'Esse e-mail é reservado. Use o CPF ou outro e-mail.' }
  if (senha.length < 6) return { erro: 'A senha precisa ter pelo menos 6 caracteres.' }
  return { ...login, senha }
}

export async function criarAluno(_: Resultado, form: FormData): Promise<Resultado> {
  const dados = lerLoginESenha(form)
  if ('erro' in dados) return { ok: false, texto: dados.erro! }
  const nome = String(form.get('nome') ?? '').trim()
  try {
    const admin = await clienteAdmin()
    const { error } = await admin.auth.admin.createUser({
      email: dados.email,
      password: dados.senha,
      email_confirm: true,
      user_metadata: nome ? { full_name: nome } : {},
    })
    if (error) {
      return {
        ok: false,
        texto: /already|registered|exists/i.test(error.message)
          ? `Já existe um aluno com esse ${dados.cpf ? 'CPF' : 'e-mail'}.`
          : `Não deu para criar: ${error.message}`,
      }
    }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  revalidatePath('/admin')
  const ident = dados.cpf ? formatarCpf(dados.cpf) : dados.email
  return { ok: true, texto: `Aluno ${nome || ident} criado. Ele já pode entrar com o ${dados.cpf ? 'CPF' : 'e-mail'} e a senha.` }
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

/** Muda quantos aparelhos a conta pode ter abertos ao mesmo tempo e fecha na hora os que passarem do novo limite. */
export async function definirAparelhos(_: Resultado, form: FormData): Promise<Resultado> {
  const id = String(form.get('id') ?? '')
  const valor = String(form.get('limite') ?? '')
  if (!id) return { ok: false, texto: 'Escolha o aluno.' }
  const limite = valor === 'livre' ? null : Number(valor)
  if (limite !== null && !(Number.isInteger(limite) && limite >= 1 && limite <= 10)) return { ok: false, texto: 'Escolha o limite.' }
  let fechados = 0
  try {
    const admin = await clienteAdmin()
    const { error } = await admin.from('perfis').update({ max_aparelhos: limite }).eq('id', id)
    if (error) return { ok: false, texto: `Não deu para mudar: ${error.message}` }
    const { data, error: erroPoda } = await admin.rpc('podar_aparelhos', { p_user: id })
    if (erroPoda) return { ok: false, texto: `Limite mudado, mas não deu para fechar os aparelhos a mais: ${erroPoda.message}` }
    fechados = Number(data ?? 0)
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  revalidatePath('/admin')
  const fim = fechados ? ` ${fechados === 1 ? 'Um aparelho saiu' : `${fechados} aparelhos saíram`} da conta.` : ''
  return { ok: true, texto: `Limite mudado.${fim}` }
}

/** Muda a turma do aluno (T28 ou T29); "todas" deixa vazio, como o administrador, que vê as duas. */
export async function definirTurma(_: Resultado, form: FormData): Promise<Resultado> {
  const id = String(form.get('id') ?? '')
  const valor = String(form.get('turma') ?? '')
  if (!id) return { ok: false, texto: 'Escolha o aluno.' }
  if (!['t28', 't29', 'todas'].includes(valor)) return { ok: false, texto: 'Escolha a turma.' }
  try {
    const admin = await clienteAdmin()
    const { error } = await admin.from('perfis').update({ turma: valor === 'todas' ? null : valor }).eq('id', id)
    if (error) return { ok: false, texto: `Não deu para mudar: ${error.message}` }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  revalidatePath('/admin')
  return { ok: true, texto: 'Turma mudada. O aluno vê as matérias da turma nova na próxima tela que abrir.' }
}

/** Muda o período atual de uma turma: a aba Matérias passa a abrir nele. */
export async function definirPeriodo(_: Resultado, form: FormData): Promise<Resultado> {
  const turma = String(form.get('turma') ?? '')
  const periodo = Number(form.get('periodo'))
  if (!['t28', 't29'].includes(turma)) return { ok: false, texto: 'Escolha a turma.' }
  if (!(Number.isInteger(periodo) && periodo >= 1 && periodo <= 12)) return { ok: false, texto: 'Escolha o período.' }
  try {
    const admin = await clienteAdmin()
    const { error } = await admin.from('turmas').update({ periodo_atual: periodo }).eq('id', turma)
    if (error) return { ok: false, texto: `Não deu para mudar: ${error.message}` }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  revalidatePath('/admin')
  return { ok: true, texto: `A ${turma.toUpperCase()} agora está no ${periodo}º período.` }
}
