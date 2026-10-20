'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { cpfParaEmail, formatarCpf, soDigitos } from '@/lib/cpf'

export function LoginForm() {
  const router = useRouter()
  const [cpf, setCpf] = useState('')
  const [senha, setSenha] = useState('')
  const [entrando, setEntrando] = useState(false)
  const [erro, setErro] = useState('')
  const [ver, setVer] = useState(false)

  async function entrar(e: React.FormEvent) {
    e.preventDefault()
    if (soDigitos(cpf).length !== 11) {
      setErro('Digite os 11 números do CPF.')
      return
    }
    if (!senha) {
      setErro('Digite a senha.')
      return
    }
    setErro('')
    setEntrando(true)
    const supabase = createClient()
    const { error } = await supabase.auth.signInWithPassword({ email: cpfParaEmail(cpf), password: senha })
    if (error) {
      setErro(
        error.status === 429
          ? 'Muitas tentativas em pouco tempo. Espere alguns minutos e tente de novo.'
          : /invalid/i.test(error.message)
            ? 'CPF ou senha incorretos.'
            : 'Não foi possível entrar agora. Tente de novo em instantes.',
      )
      setEntrando(false)
      return
    }
    router.replace('/')
    router.refresh()
  }

  return (
    <form className="lg-form" onSubmit={entrar} noValidate>
      <div className={`lg-campo${erro ? ' com-erro' : ''}`}>
        <svg className="lg-ico" viewBox="0 0 24 24" aria-hidden="true">
          <rect x="3" y="5" width="18" height="14" rx="3" />
          <path d="M8 11h4M8 15h8" />
        </svg>
        <label htmlFor="cpf" className="sr-only">
          CPF
        </label>
        <input
          id="cpf"
          name="username"
          autoComplete="username"
          inputMode="numeric"
          placeholder="CPF"
          value={cpf}
          onChange={(e) => {
            setCpf(formatarCpf(e.target.value))
            setErro('')
          }}
          aria-invalid={erro ? true : undefined}
          aria-describedby={erro ? 'loginErr' : undefined}
        />
      </div>
      <div className={`lg-campo${erro ? ' com-erro' : ''}`}>
        <svg className="lg-ico" viewBox="0 0 24 24" aria-hidden="true">
          <rect x="5" y="11" width="14" height="9" rx="2" />
          <path d="M8 11V8a4 4 0 0 1 8 0v3" />
        </svg>
        <label htmlFor="senha" className="sr-only">
          Senha
        </label>
        <input
          id="senha"
          name="password"
          type={ver ? 'text' : 'password'}
          autoComplete="current-password"
          placeholder="Senha"
          value={senha}
          onChange={(e) => {
            setSenha(e.target.value)
            setErro('')
          }}
          aria-invalid={erro ? true : undefined}
          aria-describedby={erro ? 'loginErr' : undefined}
        />
        <button
          className="lg-olho"
          type="button"
          onClick={() => setVer((v) => !v)}
          aria-label={ver ? 'Esconder a senha' : 'Mostrar a senha'}
          aria-pressed={ver}
        >
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z" />
            <circle cx="12" cy="12" r="3" />
            {ver && <path d="M4 4l16 16" />}
          </svg>
        </button>
      </div>
      {erro && (
        <p id="loginErr" className="lg-erro" role="alert">
          {erro}
        </p>
      )}
      <button className="lg-entrar" type="submit" disabled={entrando}>
        {entrando ? <span className="lg-giro" aria-hidden="true" /> : 'Entrar'}
      </button>
      <p className="lg-ajuda">Esqueceu a senha? Fale com quem criou o seu acesso.</p>
    </form>
  )
}
