import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { AdminAgenda } from '@/components/AdminAgenda'
import { chaveConfigurada, ehAdmin } from '@/lib/admin'
import { sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Agenda da semana' }

export default async function AdminAgendaPage() {
  const { supabase, email } = await sessao()
  if (!ehAdmin(email)) notFound()
  const { data: semanas } = await supabase.from('agenda_semanas').select('semana, atualizado_em').order('semana', { ascending: false }).limit(5)

  return (
    <Pagina pendentes={0}>
      <Voltar href="/perfil" rotulo="Perfil" />
      <header className="top">
        <div>
          <div className="eyebrow">Administração</div>
          <h1 className="big">Agenda da semana</h1>
        </div>
      </header>
      {chaveConfigurada() ? (
        <>
          <p className="foot" style={{ marginTop: 0, marginBottom: 12 }}>
            Cole o cronograma do jeito que chega no WhatsApp e clique em publicar. Se a semana já existir, ela é substituída
            pela nova versão.
          </p>
          <AdminAgenda />
          {!!semanas?.length && (
            <>
              <div className="sec">Semanas publicadas</div>
              <div className="group">
                {semanas.map((s) => (
                  <div key={s.semana} className="row static">
                    <span className="main">
                      <span className="t">
                        Semana de{' '}
                        {new Intl.DateTimeFormat('pt-BR', { day: 'numeric', month: 'long', timeZone: 'UTC' }).format(new Date(`${s.semana}T12:00:00Z`))}
                      </span>
                      <span className="s">
                        Atualizada em{' '}
                        {new Intl.DateTimeFormat('pt-BR', { dateStyle: 'short', timeStyle: 'short', timeZone: 'America/Sao_Paulo' }).format(new Date(s.atualizado_em))}
                      </span>
                    </span>
                  </div>
                ))}
              </div>
            </>
          )}
        </>
      ) : (
        <p className="vazio">Falta a chave secreta do Supabase na Vercel (SUPABASE_SECRET_KEY).</p>
      )}
    </Pagina>
  )
}
