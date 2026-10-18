import Link from 'next/link'
import { TabBar } from './TabBar'
import { Icone } from './Icones'

// Tela de carregamento: mesma moldura das telas logadas (engrenagem e barra de baixo) com blocos
// cinzas no lugar do conteúdo, para o toque na aba responder na hora enquanto os dados chegam.
export function Esqueleto() {
  return (
    <>
      <main className="wrap" aria-busy="true">
        <Link className="avatar engrenagem" href="/perfil" aria-label="Configurações">
          {Icone.engrenagem}
        </Link>
        <div className="view" role="status">
          <span className="sr-only">Carregando…</span>
          <div className="sk sk-eyebrow" aria-hidden="true" />
          <div className="sk sk-titulo" aria-hidden="true" />
          <div className="sk sk-bloco alto" aria-hidden="true" />
          <div className="sk sk-bloco" aria-hidden="true" />
          <div className="sk sk-bloco" aria-hidden="true" />
          <div className="sk sk-bloco" aria-hidden="true" />
        </div>
      </main>
      <TabBar pendentes={0} />
    </>
  )
}
