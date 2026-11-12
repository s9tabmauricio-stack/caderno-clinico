// Robô do Gmail (docs/robo-gmail/): cria a conta de quem mandou e-mail @minha.fag.edu.br com a senha de 6 números.
// Só atende quem manda a chave ROBO_GMAIL_CHAVE (a mesma guardada no robô e na Vercel).
import { clienteServico } from '@/lib/admin'
import { chaveConfere, lerPedidoConta } from '@/lib/contas-gmail'

export async function POST(request: Request) {
  const certa = process.env.ROBO_GMAIL_CHAVE ?? ''
  if (!certa) return Response.json({ ok: false, motivo: 'A chave do robô não está configurada na Vercel.' }, { status: 503 })
  const recebida = (request.headers.get('authorization') ?? '').replace(/^Bearer\s+/i, '')
  if (!chaveConfere(recebida, certa)) return Response.json({ ok: false, motivo: 'Chave errada.' }, { status: 401 })

  const pedido = lerPedidoConta(await request.json().catch(() => null))
  if ('erro' in pedido) return Response.json({ ok: false, motivo: pedido.erro }, { status: 400 })

  try {
    const { error } = await clienteServico().auth.admin.createUser({
      email: pedido.email,
      password: pedido.senha,
      email_confirm: true,
      user_metadata: pedido.nome ? { full_name: pedido.nome } : {},
    })
    if (error) {
      if (/already|registered|exists/i.test(error.message)) {
        return Response.json({ ok: false, motivo: 'Já existe uma conta com esse e-mail.' }, { status: 409 })
      }
      return Response.json({ ok: false, motivo: `Não deu para criar: ${error.message}` }, { status: 500 })
    }
  } catch (e) {
    return Response.json({ ok: false, motivo: (e as Error).message }, { status: 500 })
  }
  return Response.json({ ok: true, email: pedido.email }, { status: 201 })
}
