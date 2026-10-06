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
    <>
      <div className="login-card">
        <form onSubmit={entrar} noValidate>
          <label htmlFor="cpf" className="flabel">
            CPF
          </label>
          <input
            id="cpf"
            name="username"
            autoComplete="username"
            inputMode="numeric"
            placeholder="000.000.000-00"
            value={cpf}
            onChange={(e) => {
              setCpf(formatarCpf(e.target.value))
              setErro('')
            }}
            aria-invalid={erro ? true : undefined}
            aria-describedby={erro ? 'loginErr' : undefined}
          />
          <label htmlFor="senha" className="flabel" style={{ marginTop: 6 }}>
            Senha
          </label>
          <input
            id="senha"
            name="password"
            type="password"
            autoComplete="current-password"
            value={senha}
            onChange={(e) => {
              setSenha(e.target.value)
              setErro('')
            }}
            aria-invalid={erro ? true : undefined}
            aria-describedby={erro ? 'loginErr' : undefined}
          />
          {erro && (
            <p id="loginErr" className="err" role="alert">
              {erro}
            </p>
          )}
          <button className="btn wide" type="submit" disabled={entrando}>
            {entrando ? 'Entrando…' : 'Entrar'}
          </button>
        </form>
      </div>
      <p className="fine">Esqueceu a senha? Fale com quem criou o seu acesso. Seu progresso fica salvo na sua conta.</p>
    </>
  )
}
