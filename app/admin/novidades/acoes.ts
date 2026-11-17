'use server'

import { revalidatePath } from 'next/cache'
import { clienteAdmin } from '@/lib/admin'

export type ResultadoNovidade = { ok: boolean; texto: string } | null

// Novidade nova vai para o topo e faz a bolinha do sininho piscar para toda a turma
export async function publicarNovidade(_: ResultadoNovidade, form: FormData): Promise<ResultadoNovidade> {
  const titulo = String(form.get('titulo') ?? '').trim()
  const texto = String(form.get('texto') ?? '').trim()
  if (!titulo || !texto) return { ok: false, texto: 'Escreva o título e o texto.' }
  if (titulo.length > 120) return { ok: false, texto: 'Título muito longo (até 120 letras).' }
  if (texto.length > 1000) return { ok: false, texto: 'Texto muito longo (até 1000 letras).' }
  try {
    const { error } = await (await clienteAdmin()).from('novidades').insert({ titulo, texto })
    if (error) return { ok: false, texto: `Não deu para salvar: ${error.message}` }
  } catch (e) {
    return { ok: false, texto: (e as Error).message }
  }
  revalidatePath('/', 'layout')
  return { ok: true, texto: 'Publicada: a turma já vê a bolinha no sininho.' }
}

export async function apagarNovidade(form: FormData) {
  const id = String(form.get('id') ?? '')
  if (!id) return
  await (await clienteAdmin()).from('novidades').delete().eq('id', id)
  revalidatePath('/', 'layout')
}
