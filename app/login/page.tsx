import type { Metadata } from 'next'
import { Icone } from '@/components/Icones'
import { LoginForm } from '@/components/LoginForm'

export const metadata: Metadata = { title: 'Entrar' }

export default function LoginPage() {
  return (
    <main className="wrap">
      <div className="login view">
        <div className="brand">
          <span className="mark">{Icone.pulso}</span>
          <h1 className="big">Caderno Clínico</h1>
          <p className="lead">Apostilas, questões e flashcards de cada aula, com o seu progresso salvo.</p>
        </div>
        <LoginForm />
      </div>
    </main>
  )
}
