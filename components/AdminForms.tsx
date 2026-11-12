'use client'

import { useActionState, useRef, useState } from 'react'
import { criarAluno, definirAparelhos, trocarSenhaAluno, type Resultado } from '@/app/admin/acoes'
import { formatarLogin } from '@/lib/cpf'

function Mensagem({ r }: { r: Resultado }) {
  if (!r) return null
  return (
    <p className={r.ok ? 'ok-msg' : 'err'} role="status">
      {r.texto}
    </p>
  )
}

export function CriarAluno() {
  const [cpf, setCpf] = useState('')
  const form = useRef<HTMLFormElement>(null)
  // Depois de criar o aluno, limpa o formulário para o próximo
  const [r, acao, enviando] = useActionState(async (antes: Resultado, dados: FormData) => {
    const res = await criarAluno(antes, dados)
    if (res?.ok) {
      form.current?.reset()
      setCpf('')
    }
    return res
  }, null)

  return (
    <form ref={form} action={acao} className="admin-form" noValidate>
      <label className="flabel" htmlFor="a-cpf">
        CPF ou e-mail
      </label>
      <input
        id="a-cpf"
        name="cpf"
        className="campo"
        placeholder="CPF ou e-mail"
        autoComplete="off"
        autoCapitalize="none"
        autoCorrect="off"
        spellCheck={false}
        value={cpf}
        onChange={(e) => setCpf(formatarLogin(e.target.value))}
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

export function LimiteAparelhos({ alunos }: { alunos: { id: string; rotulo: string }[] }) {
  const [r, acao, enviando] = useActionState(definirAparelhos, null)
  return (
    <form action={acao} className="admin-form" noValidate>
      <label className="flabel" htmlFor="d-id">
        Aluno
      </label>
      <select id="d-id" name="id" className="campo" defaultValue="">
        <option value="" disabled>
          Escolha
        </option>
        {alunos.map((a) => (
          <option key={a.id} value={a.id}>
            {a.rotulo}
          </option>
        ))}
      </select>
      <label className="flabel" htmlFor="d-limite">
        Aparelhos ao mesmo tempo
      </label>
      <select id="d-limite" name="limite" className="campo" defaultValue="1">
        <option value="1">1 aparelho</option>
        <option value="2">2 aparelhos</option>
        <option value="3">3 aparelhos</option>
        <option value="livre">Sem limite</option>
      </select>
      <button className="btn" type="submit" disabled={enviando}>
        {enviando ? 'Mudando…' : 'Mudar limite'}
      </button>
      <Mensagem r={r} />
    </form>
  )
}
