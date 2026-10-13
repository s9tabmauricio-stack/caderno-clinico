import type { Metadata } from 'next'
import { Pagina, recadosNovos } from '@/components/Pagina'
import { PerfilAcoes } from '@/components/PerfilAcoes'
import Link from 'next/link'
import { carregarMaterias, carregarProgresso, pendentes, sessao } from '@/lib/dados'
import { ehAdmin } from '@/lib/admin'

export const metadata: Metadata = { title: 'Configurações' }

export default async function PerfilPage() {
  const { supabase, userId, email } = await sessao()
  const [perfil, progresso, materias, novos] = await Promise.all([
    supabase.from('perfis').select('nome, grupo').eq('id', userId).maybeSingle(),
    carregarProgresso(supabase),
    carregarMaterias(supabase),
    recadosNovos(),
  ])
  // Aulas agrupadas na ordem das matérias, para o seletor de "Apagar progresso"
  const aulas = materias.flatMap((m) =>
    progresso.filter((a) => a.materia_id === m.id).map((a) => ({ id: a.aula_id, titulo: a.titulo, materiaId: m.id })),
  )
  const nome = perfil.data?.nome || (/^\d{11}$/.test(email.split('@')[0]) ? 'Aluno' : email.split('@')[0])

  return (
    <Pagina pendentes={pendentes(progresso).hoje}>
      <header className="top">
        <div>
          <h1 className="big">Configurações</h1>
        </div>
      </header>

      <PerfilAcoes
        userId={userId}
        nomeInicial={nome}
        email={email}
        grupoInicial={perfil.data?.grupo ?? null}
        materias={materias}
        aulas={aulas}
      />

      {ehAdmin(email) && (
        <>
          <div className="sec">Administração</div>
          <div className="group">
            <Link className="row" href="/admin/recados">
              <span className="main">
                <span className="t">Recados da turma</span>
                <span className="s">Dicas e erros que os alunos deixaram nas questões</span>
              </span>
              {novos > 0 && <span className="cnt" aria-label={`${novos} novos`}>{novos}</span>}
            </Link>
            <Link className="row" href="/admin/painel">
              <span className="main">
                <span className="t">Painel do conteúdo</span>
                <span className="s">Aulas no ar, questões e flashcards por matéria</span>
              </span>
            </Link>
            <Link className="row" href="/admin">
              <span className="main">
                <span className="t">Alunos</span>
                <span className="s">Criar contas e trocar senhas</span>
              </span>
            </Link>
            <Link className="row" href="/admin/conteudo">
              <span className="main">
                <span className="t">Conteúdo</span>
                <span className="s">Editar e apagar aulas, questões e flashcards</span>
              </span>
            </Link>
            <Link className="row" href="/admin/agenda">
              <span className="main">
                <span className="t">Agenda da semana</span>
                <span className="s">Colar o cronograma do WhatsApp</span>
              </span>
            </Link>
          </div>
        </>
      )}

      <div className="sec">Instalar no celular</div>
      <div className="how">
        <div className="how-i">
          <div className="kick">iPhone</div>
          <p>No Safari, toque em Compartilhar e depois em Adicionar à Tela de Início.</p>
        </div>
        <div className="how-i">
          <div className="kick">Android</div>
          <p>No Chrome, abra o menu de três pontos e toque em Instalar app ou Adicionar à tela inicial.</p>
        </div>
      </div>

      <form action="/auth/sair" method="post">
        <button className="btn ghost wide out" type="submit">
          Sair
        </button>
      </form>
    </Pagina>
  )
}
