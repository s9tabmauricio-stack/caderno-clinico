import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { Central } from '@/components/admin/Central'
import { chaveConfigurada, ehAdmin } from '@/lib/admin'
import { carregarCentral } from '@/lib/central'
import { sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Central' }

export default async function CentralPage() {
  const { email } = await sessao()
  if (!ehAdmin(email)) notFound()
  if (!chaveConfigurada()) {
    return (
      <Pagina>
        <Voltar href="/perfil" rotulo="Configurações" />
        <p className="vazio">Falta a chave secreta do Supabase na Vercel (SUPABASE_SECRET_KEY).</p>
      </Pagina>
    )
  }
  const c = await carregarCentral()
  return (
    <Pagina larga>
      <Voltar href="/perfil" rotulo="Configurações" />
      <Central c={c} />
    </Pagina>
  )
}
