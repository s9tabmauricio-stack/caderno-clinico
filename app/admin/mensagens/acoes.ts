'use server'

import { revalidatePath } from 'next/cache'
import { clienteAdmin } from '@/lib/admin'

const STATUS = ['nova', 'lida']

function atualizarTelas() {
  // o número no balão do topo aparece em todas as telas
  revalidatePath('/', 'layout')
}

export async function marcarMensagem(form: FormData) {
  const id = String(form.get('id') ?? '')
  const status = String(form.get('status') ?? '')
  if (!id || !STATUS.includes(status)) return
  const { error } = await (await clienteAdmin()).from('mensagens').update({ status }).eq('id', id)
  if (error) throw new Error(`Não deu para salvar: ${error.message}`)
  atualizarTelas()
}

export async function marcarTodasLidas() {
  const { error } = await (await clienteAdmin()).from('mensagens').update({ status: 'lida' }).eq('status', 'nova')
  if (error) throw new Error(`Não deu para salvar: ${error.message}`)
  atualizarTelas()
}

export async function apagarMensagem(form: FormData) {
  const id = String(form.get('id') ?? '')
  if (!id) return
  const { error } = await (await clienteAdmin()).from('mensagens').delete().eq('id', id)
  if (error) throw new Error(`Não deu para apagar: ${error.message}`)
  atualizarTelas()
}
