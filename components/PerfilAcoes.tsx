'use client'

import { useMemo, useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'
import { cpfDoEmail, formatarCpf } from '@/lib/cpf'

type OQue = 'ambos' | 'questoes' | 'flashcards'
type Onde = 'tudo' | 'materia' | 'aula'

export function PerfilAcoes({
  userId,
  nomeInicial,
  email,
  grupoInicial,
  materias,
  aulas,
}: {
  userId: string
  nomeInicial: string
  email: string
  grupoInicial: number | null
  materias: { id: string; nome: string }[]
  aulas: { id: string; titulo: string; materiaId: string }[]
}) {
  const supabase = useMemo(() => createClient(), [])
  const router = useRouter()
  const [nome, setNome] = useState(nomeInicial)
  const [grupo, setGrupo] = useState(grupoInicial ? String(grupoInicial) : '')
  const [editando, setEditando] = useState(false)
  const [msgDados, setMsgDados] = useState<{ ok: boolean; texto: string } | null>(null)
  const [confirmar, setConfirmar] = useState(false)
  const [msgApagar, setMsgApagar] = useState<{ ok: boolean; texto: string } | null>(null)
  const [oQue, setOQue] = useState<OQue>('ambos')
  const [onde, setOnde] = useState<Onde>('tudo')
  const [alvo, setAlvo] = useState('')
  async function salvarDados(e: React.FormEvent) {
    e.preventDefault()
    const v = nome.trim()
    const n = grupo.trim() ? Number(grupo) : null
    if (!v) {
      setMsgDados({ ok: false, texto: 'Digite um nome.' })
      return
    }
    if (n !== null && (!Number.isInteger(n) || n < 1 || n > 99)) {
      setMsgDados({ ok: false, texto: 'Digite o número do grupo, como 7.' })
      return
    }
    const { error } = await supabase.from('perfis').update({ nome: v, grupo: n }).eq('id', userId)
    setMsgDados(error ? { ok: false, texto: 'Não deu para salvar. Tente de novo.' } : { ok: true, texto: 'Dados salvos.' })
    if (!error) {
      setEditando(false)
      router.refresh()
    }
  }

  function cancelarEdicao() {
    setNome(nomeInicial)
    setGrupo(grupoInicial ? String(grupoInicial) : '')
    setEditando(false)
    setMsgDados(null)
  }
  const [senha, setSenha] = useState('')
  const [senha2, setSenha2] = useState('')
  const [msgSenha, setMsgSenha] = useState<{ ok: boolean; texto: string } | null>(null)
  const cpf = cpfDoEmail(email)

  async function trocarSenha(e: React.FormEvent) {
    e.preventDefault()
    if (senha.length < 6) {
      setMsgSenha({ ok: false, texto: 'A senha precisa ter pelo menos 6 caracteres.' })
      return
    }
    if (senha !== senha2) {
      setMsgSenha({ ok: false, texto: 'As duas senhas não são iguais.' })
      return
    }
    const { error } = await supabase.auth.updateUser({ password: senha })
    if (error) {
      setMsgSenha({
        ok: false,
        texto: /different|same/i.test(error.message)
          ? 'A nova senha precisa ser diferente da atual.'
          : 'Não deu para trocar a senha. Tente de novo.',
      })
      return
    }
    setSenha('')
    setSenha2('')
    setMsgSenha({ ok: true, texto: 'Senha trocada. Use a nova senha no próximo acesso.' })
  }

  // Texto que descreve o que vai ser apagado, ex.: "as respostas das questões de Nefrologia"
  const aulasDaMateria = aulas.filter((a) => a.materiaId === alvo).map((a) => a.id)
  const alvoNome =
    onde === 'materia' ? materias.find((m) => m.id === alvo)?.nome : aulas.find((a) => a.id === alvo)?.titulo
  const descricaoApagar = [
    oQue === 'questoes'
      ? 'as respostas das questões'
      : oQue === 'flashcards'
        ? 'as revisões dos flashcards'
        : 'as respostas das questões e as revisões dos flashcards',
    onde === 'tudo' ? 'de todas as matérias' : onde === 'materia' ? `de ${alvoNome}` : `da aula ${alvoNome}`,
  ].join(' ')
  const pronto = onde === 'tudo' || alvo !== ''

  async function apagarProgresso() {
    let falhou = false

    if (oQue !== 'flashcards') {
      let ids: string[] | null = null
      if (onde !== 'tudo') {
        const busca = supabase.from('questoes').select('id')
        const { data, error } = await (onde === 'materia' ? busca.eq('materia_id', alvo) : busca.eq('aula_id', alvo))
        falhou ||= Boolean(error)
        ids = (data ?? []).map((r) => r.id)
      }
      if (!falhou && (ids === null || ids.length > 0)) {
        const del = supabase.from('respostas').delete().eq('user_id', userId)
        const { error } = await (ids ? del.in('questao_id', ids) : del)
        falhou ||= Boolean(error)
      }
    }

    if (oQue !== 'questoes' && !falhou) {
      let ids: string[] | null = null
      if (onde !== 'tudo') {
        const { data, error } = await supabase
          .from('flashcards')
          .select('id')
          .in('aula_id', onde === 'materia' ? aulasDaMateria : [alvo])
        falhou ||= Boolean(error)
        ids = (data ?? []).map((r) => r.id)
      }
      if (!falhou && (ids === null || ids.length > 0)) {
        const del = supabase.from('revisoes').delete().eq('user_id', userId)
        const { error } = await (ids ? del.in('flashcard_id', ids) : del)
        falhou ||= Boolean(error)
      }
    }

    setConfirmar(false)
    setMsgApagar(
      falhou
        ? {
            ok: false,
            texto: 'Não deu para apagar tudo. Parte pode já ter sido apagada; confira a internet e tente de novo.',
          }
        : { ok: true, texto: `Apagado: ${descricaoApagar}.` },
    )
    router.refresh()
  }

  return (
    <>
      <div className="group">
        <div className="row static">
          <span className="avatar lg" aria-hidden="true">
            {(nome || email).charAt(0).toUpperCase()}
          </span>
          <span className="main">
            <span className="t">{nomeInicial}</span>
            <span className="s">
              {cpf ? `CPF ${formatarCpf(cpf)}` : email}
              {grupoInicial ? ` · Grupo ${grupoInicial}` : ''}
            </span>
          </span>
          {!editando && (
            <button
              className="btn ghost sm"
              onClick={() => {
                setEditando(true)
                setMsgDados(null)
              }}
            >
              Editar
            </button>
          )}
        </div>
        {editando && (
          <form className="editar-form" onSubmit={salvarDados} noValidate>
            <label htmlFor="nome" className="rotulo">
              Como você quer ser chamado
            </label>
            <input
              id="nome"
              className="campo"
              value={nome}
              maxLength={60}
              autoComplete="given-name"
              onChange={(e) => setNome(e.target.value)}
            />
            <label htmlFor="grupo" className="rotulo">
              Seu grupo de prática
            </label>
            <input
              id="grupo"
              className="campo"
              inputMode="numeric"
              placeholder="Ex.: 7"
              value={grupo}
              maxLength={2}
              onChange={(e) => setGrupo(e.target.value.replace(/\D/g, ''))}
            />
            <p className="foot">Com o grupo salvo, a agenda mostra as teóricas da turma e só as práticas do seu grupo.</p>
            <div className="actions">
              <button className="btn ghost" type="button" onClick={cancelarEdicao}>
                Cancelar
              </button>
              <button className="btn" type="submit">
                Salvar
              </button>
            </div>
          </form>
        )}
      </div>
      {msgDados && (
        <p className={msgDados.ok ? 'ok-msg' : 'err'} role="status">
          {msgDados.texto}
        </p>
      )}

      <div className="sec">Trocar senha</div>
      <form className="senha-form" onSubmit={trocarSenha} noValidate>
        <label htmlFor="nova-senha" className="sr-only">
          Nova senha
        </label>
        <input
          id="nova-senha"
          className="campo"
          type="password"
          autoComplete="new-password"
          placeholder="Nova senha"
          value={senha}
          onChange={(e) => {
            setSenha(e.target.value)
            setMsgSenha(null)
          }}
        />
        <label htmlFor="nova-senha2" className="sr-only">
          Repita a nova senha
        </label>
        <input
          id="nova-senha2"
          className="campo"
          type="password"
          autoComplete="new-password"
          placeholder="Repita a nova senha"
          value={senha2}
          onChange={(e) => {
            setSenha2(e.target.value)
            setMsgSenha(null)
          }}
        />
        <button className="btn" type="submit">
          Trocar senha
        </button>
      </form>
      {msgSenha && (
        <p className={msgSenha.ok ? 'ok-msg' : 'err'} role="status">
          {msgSenha.texto}
        </p>
      )}

      <div className="sec">Apagar progresso</div>
      <form
        className="apagar-form"
        onSubmit={(e) => {
          e.preventDefault()
          if (!pronto) return
          setConfirmar(true)
          setMsgApagar(null)
        }}
        noValidate
      >
        <label htmlFor="apagar-o-que" className="rotulo">
          O que apagar
        </label>
        <select
          id="apagar-o-que"
          className="campo"
          value={oQue}
          onChange={(e) => {
            setOQue(e.target.value as OQue)
            setConfirmar(false)
          }}
        >
          <option value="ambos">Questões e flashcards</option>
          <option value="questoes">Só questões</option>
          <option value="flashcards">Só flashcards</option>
        </select>

        <label htmlFor="apagar-onde" className="rotulo">
          De onde
        </label>
        <select
          id="apagar-onde"
          className="campo"
          value={onde}
          onChange={(e) => {
            setOnde(e.target.value as Onde)
            setAlvo('')
            setConfirmar(false)
          }}
        >
          <option value="tudo">Todas as matérias</option>
          <option value="materia">Uma matéria</option>
          <option value="aula">Uma aula</option>
        </select>

        {onde === 'materia' && (
          <>
            <label htmlFor="apagar-materia" className="rotulo">
              Matéria
            </label>
            <select
              id="apagar-materia"
              className="campo"
              value={alvo}
              onChange={(e) => setAlvo(e.target.value)}
            >
              <option value="">Escolha a matéria</option>
              {materias.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.nome}
                </option>
              ))}
            </select>
          </>
        )}

        {onde === 'aula' && (
          <>
            <label htmlFor="apagar-aula" className="rotulo">
              Aula
            </label>
            <select id="apagar-aula" className="campo" value={alvo} onChange={(e) => setAlvo(e.target.value)}>
              <option value="">Escolha a aula</option>
              {materias.map((m) => (
                <optgroup key={m.id} label={m.nome}>
                  {aulas
                    .filter((a) => a.materiaId === m.id)
                    .map((a) => (
                      <option key={a.id} value={a.id}>
                        {a.titulo}
                      </option>
                    ))}
                </optgroup>
              ))}
            </select>
          </>
        )}

        <button className="btn danger wide" type="submit" disabled={!pronto}>
          Apagar
        </button>
      </form>

      {confirmar && (
        <div className="group">
          <div className="row static confirm">
            <span className="main">
              <span className="t">Apagar {descricaoApagar}?</span>
              <span className="s">Não dá para desfazer.</span>
            </span>
            <button className="btn ghost sm" onClick={() => setConfirmar(false)}>
              Cancelar
            </button>
            <button className="btn danger sm" onClick={apagarProgresso}>
              Apagar
            </button>
          </div>
        </div>
      )}
      {msgApagar && (
        <p className={msgApagar.ok ? 'ok-msg' : 'err'} role="status">
          {msgApagar.texto}
        </p>
      )}
    </>
  )
}
