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
      <div className={`lg-campos${erro ? ' com-erro' : ''}`}>
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
        <div className="lg-senha">
          <label htmlFor="senha" className="sr-only">
            Senha
          </label>
          <input
            id="senha"
            name="password"
            type="password"
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
          <button className="lg-ir" type="submit" disabled={entrando} aria-label="Entrar">
            {entrando ? (
              <span className="lg-giro" aria-hidden="true" />
            ) : (
              <svg viewBox="0 0 24 24" aria-hidden="true">
                <path d="M5 12h13M13 6l6 6-6 6" />
              </svg>
            )}
          </button>
        </div>
      </div>
      {erro && (
        <p id="loginErr" className="lg-erro" role="alert">
          {erro}
        </p>
      )}
      <p className="lg-ajuda">Esqueceu a senha? Fale com quem criou o seu acesso.</p>
    </form>
  )
}
