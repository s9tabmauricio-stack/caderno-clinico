import type { Metadata } from 'next'
import { Icone } from '@/components/Icones'
import { LoginForm } from '@/components/LoginForm'

export const metadata: Metadata = { title: 'Entrar' }

export default function LoginPage() {
  return (
    <main className="tela-entrar">
      <div className="lg-fundo" aria-hidden="true">
        <span className="o1" />
        <span className="o2" />
        <span className="o3" />
      </div>

      <section className="lg-vidro">
        <span className="lg-icone">{Icone.pulso}</span>
        <h1>Caderno Clínico</h1>
        <p className="lg-sub">Entre com seu CPF e senha</p>
        <LoginForm />
      </section>

      <footer className="lg-rodape">By Mauricio</footer>
    </main>
  )
}
