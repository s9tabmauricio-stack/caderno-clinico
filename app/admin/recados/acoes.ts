'use server'

import { revalidatePath } from 'next/cache'
import { clienteAdmin } from '@/lib/admin'

const STATUS = ['novo', 'visto', 'corrigido']

function atualizarTelas() {
  // a bolinha da engrenagem aparece em todas as telas
  revalidatePath('/', 'layout')
}

export async function marcarRecado(form: FormData) {
  const id = String(form.get('id') ?? '')
  const status = String(form.get('status') ?? '')
  if (!id || !STATUS.includes(status)) return
  const admin = await clienteAdmin()
  const { error } = await admin.from('recados').update({ status }).eq('id', id)
  if (error) throw new Error(`Não deu para salvar: ${error.message}`)
  atualizarTelas()
}

export async function marcarTodosVistos() {
  const admin = await clienteAdmin()
  const { error } = await admin.from('recados').update({ status: 'visto' }).eq('status', 'novo')
  if (error) throw new Error(`Não deu para salvar: ${error.message}`)
  atualizarTelas()
}

export async function apagarRecado(form: FormData) {
  const id = String(form.get('id') ?? '')
  if (!id) return
  const admin = await clienteAdmin()
  const { error } = await admin.from('recados').delete().eq('id', id)
  if (error) throw new Error(`Não deu para apagar: ${error.message}`)
  atualizarTelas()
}
