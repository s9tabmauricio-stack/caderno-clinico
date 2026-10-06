import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = { title: 'Link inválido' }

export default function ErroLogin() {
  return (
    <main className="wrap">
      <div className="centro view">
        <h1>Este link não funcionou</h1>
        <p>
          Ele pode ter expirado, já ter sido usado ou ter sido aberto em outro navegador. Peça um link novo e abra o e-mail
          no mesmo navegador em que você pediu.
        </p>
        <Link className="btn" href="/login">
          Pedir um link novo
        </Link>
      </div>
    </main>
  )
}
