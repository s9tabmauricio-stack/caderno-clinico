import type { Metadata } from 'next'
import { Pagina } from '@/components/Pagina'
import { PerfilAcoes } from '@/components/PerfilAcoes'
import { TemaEscolha } from '@/components/TemaEscolha'
import { carregarMaterias, carregarProgresso, pendentes, sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Configurações' }

export default async function PerfilPage() {
  const { supabase, userId, email } = await sessao()
  const [perfil, progresso, materias] = await Promise.all([
    supabase.from('perfis').select('nome, grupo').eq('id', userId).maybeSingle(),
    carregarProgresso(supabase),
    carregarMaterias(supabase),
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

      <div className="sec">Aparência</div>
      <TemaEscolha />
      <p className="foot">Auto segue o modo do celular (claro de dia, escuro à noite). A escolha vale só neste aparelho.</p>

      <div className="sec">Instalar o app</div>
      <div className="how">
        <div className="how-i">
          <div className="kick">iPhone e iPad</div>
          <p>No Safari, toque em Compartilhar e depois em Adicionar à Tela de Início.</p>
        </div>
        <div className="how-i">
          <div className="kick">Android (celular e tablet)</div>
          <p>No Chrome, abra o menu de três pontos e toque em Instalar app ou Adicionar à tela inicial.</p>
        </div>
      </div>

      <form action="/auth/sair" method="post">
        <button className="btn danger wide out" type="submit">
          Sair
        </button>
      </form>
    </Pagina>
  )
}
