import Link from 'next/link'

export default function NaoEncontrado() {
  return (
    <main className="wrap">
      <div className="centro view">
        <h1>Página não encontrada</h1>
        <p>Essa aula ou matéria não existe ou ainda não foi publicada.</p>
        <Link className="btn" href="/">
          Voltar ao início
        </Link>
      </div>
    </main>
  )
}
