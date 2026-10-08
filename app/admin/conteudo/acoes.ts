'use server'

import { revalidatePath } from 'next/cache'
import { clienteAdmin } from '@/lib/admin'

export type Msg = { ok: boolean; texto: string } | null

type Admin = Awaited<ReturnType<typeof clienteAdmin>>

function atualizarTelas() {
  revalidatePath('/', 'layout')
}

function texto(form: FormData, campo: string) {
  const v = String(form.get(campo) ?? '').trim()
  return v || null
}

/** Apaga questões e tudo que depende delas (respostas e referências de versão).
 *  Os recados da turma de uma versão antiga passam para a versão nova. */
async function apagarQuestoes(admin: Admin, ids: string[]) {
  if (!ids.length) return null
  const { data: antigas, error: e0 } = await admin.from('questoes').select('id, substituida_por').in('id', ids).not('substituida_por', 'is', null)
  if (e0) return e0.message
  for (const q of (antigas ?? []) as { id: string; substituida_por: string }[]) {
    const r0 = await admin.from('recados').update({ questao_id: q.substituida_por }).eq('questao_id', q.id)
    if (r0.error) return r0.error.message
  }
  const r1 = await admin.from('respostas').delete().in('questao_id', ids)
  if (r1.error) return r1.error.message
  const r2 = await admin.from('questoes').update({ substituida_por: null }).in('substituida_por', ids)
  if (r2.error) return r2.error.message
  const r3 = await admin.from('questoes').delete().in('id', ids)
  return r3.error?.message ?? null
}

/** Apaga flashcards e as revisões dos alunos. */
async function apagarCards(admin: Admin, ids: string[]) {
  if (!ids.length) return null
  const r1 = await admin.from('revisoes').delete().in('flashcard_id', ids)
  if (r1.error) return r1.error.message
  const r2 = await admin.from('flashcards').delete().in('id', ids)
  return r2.error?.message ?? null
}

// ---------- Questões ----------

export async function salvarQuestao(_: Msg, form: FormData): Promise<Msg> {
  const id = String(form.get('id') ?? '')
  const enunciado = texto(form, 'enunciado')
  const alternativas = String(form.get('alternativas') ?? '')
    .split('\n')
    .map((l) => l.replace(/^\s*[A-Ea-e][).:-]\s+/, '').trim())
    .filter(Boolean)
  const correta = Number(form.get('correta'))
  if (!id || !enunciado) return { ok: false, texto: 'O enunciado não pode ficar vazio.' }
  if (alternativas.length < 2) return { ok: false, texto: 'Coloque pelo menos duas alternativas, uma por linha.' }
  if (!(correta >= 0 && correta < alternativas.length)) return { ok: false, texto: 'Escolha a alternativa certa.' }
  try {
    const admin = await clienteAdmin()
    const { error } = await admin
      .from('questoes')
      .update({
        enunciado,
        alternativas,
        correta,
        comentario: texto(form, 'comentario'),
        por_que_erradas: texto(form, 'por_que_erradas'),
        tema: texto(form, 'tema'),
        prova: texto(form, 'prova'),
        fonte: texto(form, 'fonte'),
        aula_id: texto(form, 'aula_id'),
      })
      .eq('id', id)
    if (error) return { ok: false, texto: `Não deu para salvar: ${error.message}` }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  atualizarTelas()
  return { ok: true, texto: 'Questão salva.' }
}

export async function apagarQuestao(form: FormData) {
  const admin = await clienteAdmin()
  const erro = await apagarQuestoes(admin, [String(form.get('id'))])
  if (erro) throw new Error(erro)
  atualizarTelas()
}

/** Remove as versões antigas de questões que foram corrigidas. */
export async function limparVersoesAntigas() {
  const admin = await clienteAdmin()
  const { data } = await admin.from('questoes').select('id').not('substituida_por', 'is', null)
  const erro = await apagarQuestoes(admin, (data ?? []).map((q: { id: string }) => q.id))
  if (erro) throw new Error(erro)
  atualizarTelas()
}

// ---------- Aulas ----------

export async function salvarAula(_: Msg, form: FormData): Promise<Msg> {
  const id = String(form.get('id') ?? '')
  const titulo = texto(form, 'titulo')
  if (!id || !titulo) return { ok: false, texto: 'O título não pode ficar vazio.' }
  try {
    const admin = await clienteAdmin()
    const { error } = await admin
      .from('aulas')
      .update({ titulo, resumo: texto(form, 'resumo'), publicada: form.get('publicada') === 'on', ordem: Number(form.get('ordem')) || 0 })
      .eq('id', id)
    if (error) return { ok: false, texto: `Não deu para salvar: ${error.message}` }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  atualizarTelas()
  return { ok: true, texto: 'Aula salva.' }
}

export async function apagarAula(form: FormData) {
  const id = String(form.get('id'))
  const admin = await clienteAdmin()
  const [{ data: cards }, { data: qs }] = await Promise.all([
    admin.from('flashcards').select('id').eq('aula_id', id),
    admin.from('questoes').select('id').eq('aula_id', id),
  ])
  const e1 = await apagarCards(admin, (cards ?? []).map((c: { id: string }) => c.id))
  if (e1) throw new Error(e1)
  const e2 = await apagarQuestoes(admin, (qs ?? []).map((q: { id: string }) => q.id))
  if (e2) throw new Error(e2)
  const { error } = await admin.from('aulas').delete().eq('id', id)
  if (error) throw new Error(error.message)
  atualizarTelas()
}

// ---------- Flashcards ----------

export async function salvarCard(_: Msg, form: FormData): Promise<Msg> {
  const id = String(form.get('id') ?? '')
  const frente = texto(form, 'frente')
  const verso = texto(form, 'verso')
  if (!id || !frente || !verso) return { ok: false, texto: 'Frente e verso não podem ficar vazios.' }
  try {
    const admin = await clienteAdmin()
    const { error } = await admin.from('flashcards').update({ frente, verso }).eq('id', id)
    if (error) return { ok: false, texto: `Não deu para salvar: ${error.message}` }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  atualizarTelas()
  return { ok: true, texto: 'Flashcard salvo.' }
}

export async function apagarCard(form: FormData) {
  const admin = await clienteAdmin()
  const erro = await apagarCards(admin, [String(form.get('id'))])
  if (erro) throw new Error(erro)
  atualizarTelas()
}
