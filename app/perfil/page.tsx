import type { Metadata } from 'next'
import { Pagina } from '@/components/Pagina'
import { PerfilAcoes } from '@/components/PerfilAcoes'
import { carregarProgresso, pendentes, sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Perfil' }

export default async function PerfilPage() {
  const { supabase, userId, email } = await sessao()
  const [perfil, progresso] = await Promise.all([
    supabase.from('perfis').select('nome').eq('id', userId).maybeSingle(),
    carregarProgresso(supabase),
  ])
  const nome = perfil.data?.nome || (/^\d{11}$/.test(email.split('@')[0]) ? 'Aluno' : email.split('@')[0])

  return (
    <Pagina pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <div className="eyebrow">Conta</div>
          <h1 className="big">Perfil</h1>
        </div>
      </header>

      <PerfilAcoes userId={userId} nomeInicial={nome} email={email} />

      <div className="sec">Instalar no celular</div>
      <div className="how">
        <div className="how-i">
          <div className="kick">iPhone</div>
          <p>No Safari, toque em Compartilhar e depois em Adicionar à Tela de Início.</p>
        </div>
        <div className="how-i">
          <div className="kick">Android</div>
          <p>No Chrome, abra o menu de três pontos e toque em Instalar app ou Adicionar à tela inicial.</p>
        </div>
      </div>

      <form action="/auth/sair" method="post">
        <button className="btn ghost wide out" type="submit">
          Sair
        </button>
      </form>
    </Pagina>
  )
}
