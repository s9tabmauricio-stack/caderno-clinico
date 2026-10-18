'use client'

import Link from 'next/link'
import { TabBar } from '@/components/TabBar'

// retry() busca os dados de novo no servidor; reset() só redesenharia a tela com o mesmo erro
export default function Erro({ retry }: { error: Error & { digest?: string }; retry: () => void }) {
  return (
    <>
      <main className="wrap">
        <div className="centro view">
          <h1>Não foi possível carregar</h1>
          <p>Confira sua conexão com a internet e tente de novo.</p>
          <button className="btn" onClick={() => retry()}>
            Tentar de novo
          </button>
          <Link className="btn ghost" href="/">
            Voltar ao início
          </Link>
        </div>
      </main>
      <TabBar pendentes={0} />
    </>
  )
}
