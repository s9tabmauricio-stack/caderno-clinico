'use client'

import { useActionState, useEffect, useRef, useState } from 'react'
import { criarAluno, trocarSenhaAluno, type Resultado } from '@/app/admin/acoes'
import { formatarCpf } from '@/lib/cpf'

function Mensagem({ r }: { r: Resultado }) {
  if (!r) return null
  return (
    <p className={r.ok ? 'ok-msg' : 'err'} role="status">
      {r.texto}
    </p>
  )
}

export function CriarAluno() {
  const [r, acao, enviando] = useActionState(criarAluno, null)
  const [cpf, setCpf] = useState('')
  const form = useRef<HTMLFormElement>(null)
  useEffect(() => {
    if (r?.ok) {
      form.current?.reset()
      setCpf('')
    }
  }, [r])

  return (
    <form ref={form} action={acao} className="admin-form" noValidate>
      <label className="flabel" htmlFor="a-cpf">
        CPF
      </label>
      <input
        id="a-cpf"
        name="cpf"
        className="campo"
        inputMode="numeric"
        placeholder="000.000.000-00"
        autoComplete="off"
        value={cpf}
        onChange={(e) => setCpf(formatarCpf(e.target.value))}
      />
      <label className="flabel" htmlFor="a-nome">
        Nome
      </label>
      <input id="a-nome" name="nome" className="campo" maxLength={60} autoComplete="off" />
      <label className="flabel" htmlFor="a-senha">
        Senha inicial
      </label>
      <input id="a-senha" name="senha" className="campo" autoComplete="new-password" />
      <button className="btn" type="submit" disabled={enviando}>
        {enviando ? 'Criando…' : 'Criar aluno'}
      </button>
      <Mensagem r={r} />
    </form>
  )
}

export function TrocarSenha({ alunos }: { alunos: { id: string; rotulo: string }[] }) {
  const [r, acao, enviando] = useActionState(trocarSenhaAluno, null)
  return (
    <form action={acao} className="admin-form" noValidate>
      <label className="flabel" htmlFor="t-id">
        Aluno
      </label>
      <select id="t-id" name="id" className="campo" defaultValue="">
        <option value="" disabled>
          Escolha
        </option>
        {alunos.map((a) => (
          <option key={a.id} value={a.id}>
            {a.rotulo}
          </option>
        ))}
      </select>
      <label className="flabel" htmlFor="t-senha">
        Nova senha
      </label>
      <input id="t-senha" name="senha" className="campo" autoComplete="new-password" />
      <button className="btn" type="submit" disabled={enviando}>
        {enviando ? 'Trocando…' : 'Trocar senha'}
      </button>
      <Mensagem r={r} />
    </form>
  )
}
