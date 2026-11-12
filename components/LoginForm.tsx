'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { formatarLogin, loginParaEmail } from '@/lib/cpf'

export function LoginForm({ destino = '/' }: { destino?: string }) {
  const router = useRouter()
  const [cpf, setCpf] = useState('')
  const [senha, setSenha] = useState('')
  const [entrando, setEntrando] = useState(false)
  const [entrou, setEntrou] = useState(false)
  const [erro, setErro] = useState('')
  const [tremendo, setTremendo] = useState(false)
  const [ver, setVer] = useState(false)
  const [capsLock, setCapsLock] = useState(false)

  function dispararErro(mensagem: string) {
    setErro(mensagem)
    setTremendo(false)
    requestAnimationFrame(() => setTremendo(true))
  }

  function checarCapsLock(e: React.KeyboardEvent<HTMLInputElement> | React.MouseEvent<HTMLInputElement>) {
    setCapsLock(e.getModifierState('CapsLock'))
  }

  async function entrar(e: React.FormEvent) {
    e.preventDefault()
    const login = loginParaEmail(cpf)
    if ('erro' in login) {
      dispararErro(login.erro)
      return
    }
    if (!senha) {
      dispararErro('Digite a senha.')
      return
    }
    setErro('')
    setEntrando(true)
    const supabase = createClient()
    const { error } = await supabase.auth.signInWithPassword({ email: login.email, password: senha })
    if (error) {
      dispararErro(
        error.status === 429
          ? 'Muitas tentativas em pouco tempo. Espere alguns minutos e tente de novo.'
          : /invalid/i.test(error.message)
            ? login.cpf ? 'CPF ou senha incorretos.' : 'E-mail ou senha incorretos.'
            : 'Não foi possível entrar agora. Tente de novo em instantes.',
      )
      setEntrando(false)
      return
    }
    setEntrou(true)
    router.replace(destino)
    router.refresh()
  }

  return (
    <form
      className={`lg-form${tremendo ? ' treme' : ''}`}
      onSubmit={entrar}
      onAnimationEnd={() => setTremendo(false)}
      noValidate
    >
      <label className="lg-rotulo" htmlFor="cpf">
        CPF ou e-mail
      </label>
      <div className={`lg-campo${erro ? ' com-erro' : ''}`}>
        <svg className="lg-ico" viewBox="0 0 24 24" aria-hidden="true">
          <circle cx="12" cy="8" r="4" />
          <path d="M4 21a8 8 0 0 1 16 0" />
        </svg>
        <input
          id="cpf"
          name="username"
          autoComplete="username"
          autoCapitalize="none"
          autoCorrect="off"
          spellCheck={false}
          placeholder="CPF ou e-mail"
          value={cpf}
          onChange={(e) => {
            setCpf(formatarLogin(e.target.value))
            setErro('')
          }}
          aria-invalid={erro ? true : undefined}
          aria-describedby={erro ? 'loginErr' : undefined}
        />
      </div>
      <label className="lg-rotulo" htmlFor="senha">
        Senha
      </label>
      <div className={`lg-campo${erro ? ' com-erro' : ''}`}>
        <svg className="lg-ico" viewBox="0 0 24 24" aria-hidden="true">
          <rect x="4" y="11" width="16" height="10" rx="2" />
          <path d="M8 11V7a4 4 0 0 1 8 0v4" />
        </svg>
        <input
          id="senha"
          name="password"
          type={ver ? 'text' : 'password'}
          autoComplete="current-password"
          placeholder="Sua senha"
          value={senha}
          onChange={(e) => {
            setSenha(e.target.value)
            setErro('')
          }}
          onKeyDown={checarCapsLock}
          onKeyUp={checarCapsLock}
          onClick={checarCapsLock}
          onBlur={() => setCapsLock(false)}
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
      {capsLock && (
        <p className="lg-caps" role="status">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 4l-7 8h4v4h6v-4h4zM9 19h6" />
          </svg>
          Caps Lock ativado
        </p>
      )}
      {erro && (
        <p id="loginErr" className="lg-erro" role="alert">
          <svg viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="12" cy="12" r="9" />
            <path d="M12 8v4.5M12 16h.01" />
          </svg>
          <span>{erro}</span>
        </p>
      )}
      <button className="lg-entrar" type="submit" disabled={entrando || entrou}>
        {entrou ? (
          <span className="lg-status">
            <svg className="lg-check" viewBox="0 0 24 24" aria-hidden="true">
              <path d="M5 12.5l4.5 4.5L19 7.5" />
            </svg>
            Entrando…
          </span>
        ) : entrando ? (
          <span className="lg-status">
            <span className="lg-giro" aria-hidden="true" />
            Entrando…
          </span>
        ) : (
          'Entrar'
        )}
      </button>
    </form>
  )
}
