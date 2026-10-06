import type { Metadata } from 'next'
import { LoginForm } from '@/components/LoginForm'

export const metadata: Metadata = { title: { absolute: 'Med Genius · Entrar' } }

export default function LoginPage() {
  return (
    <main className="tela-entrar">
      <div className="lg-fundo" aria-hidden="true">
        <span className="o1" />
        <span className="o2" />
        <span className="o3" />
      </div>

      <section className="lg-vidro">
        <img className="lg-logo" src="/brand/med-genius.svg" width={88} height={88} alt="" />
        <h1>Med Genius</h1>
        <p className="lg-sub">Entre com seu CPF e senha</p>
        <LoginForm />
      </section>

      <footer className="lg-rodape">By Mauricio</footer>
    </main>
  )
}
