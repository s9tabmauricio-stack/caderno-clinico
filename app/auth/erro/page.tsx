import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = { title: 'Não foi possível entrar' }

export default function ErroLogin() {
  return (
    <main className="wrap">
      <div className="centro view">
        <h1>Não foi possível entrar</h1>
        <p>
          Esse link de acesso não vale mais. Para entrar no Med Genius, use o seu CPF e a sua senha. Se não souber a senha,
          peça ao Mauricio para criar uma nova.
        </p>
        <Link className="btn" href="/login">
          Ir para a entrada
        </Link>
      </div>
    </main>
  )
}
