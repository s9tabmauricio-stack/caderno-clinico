import Link from 'next/link'
import { GraficoCentral } from '@/components/GraficoCentral'
import { Icone } from '@/components/Icones'
import { fmtHora, inicioMs } from '@/lib/agenda'
import { DIAS_SUMIDO, LIMITE_BANCO, type DadosCentral } from '@/lib/central'
import { pct, plural } from '@/lib/formato'
import { fmtHa } from '@/lib/recados'

const svg = (d: React.ReactNode) => (
  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    {d}
  </svg>
)
const ICONE = {
  aviso: svg(
    <>
      <path d="M12 9v4M12 17h.01" />
      <path d="M10.3 3.9L1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z" />
    </>,
  ),
  aluno: svg(
    <>
      <circle cx="9" cy="8" r="4" />
      <path d="M2 21a7 7 0 0 1 14 0M19 8v5M19 16h.01" />
    </>,
  ),
  agenda: svg(
    <>
      <rect x="3" y="4" width="18" height="17" rx="3" />
      <path d="M3 9h18M8 2v4M16 2v4" />
    </>,
  ),
  recado: svg(<path d="M21 12a8 8 0 0 1-11.6 7.1L3 21l1.9-6.4A8 8 0 1 1 21 12z" />),
  ok: svg(<path d="M20 6L9 17l-5-5" />),
}

const ddmm = (data: string) => `${data.slice(8, 10)}/${data.slice(5, 7)}`
const diaSemana = (data: string) =>
  new Intl.DateTimeFormat('pt-BR', { weekday: 'long', timeZone: 'UTC' }).format(new Date(`${data}T12:00:00Z`)).replace('-feira', '')
const mb = (bytes: number) => `${Math.max(1, Math.round(bytes / 1024 / 1024))} MB`

function Alerta({ href, tipo, icone, titulo, texto }: { href: string; tipo: 'aviso' | 'ok'; icone: React.ReactNode; titulo: string; texto: string }) {
  return (
    <Link className="row" href={href}>
      <span className={`ct-ic ${tipo}`}>{icone}</span>
      <span className="main">
        <span className="t">{titulo}</span>
        <span className="s">{texto}</span>
      </span>
      {Icone.seta}
    </Link>
  )
}

// Conteúdo da Central (a página carrega os números e mostra isto dentro da moldura do app).
export function Central({ c }: { c: DadosCentral }) {
  const sumidos = c.alunos.filter((a) => !a.admin && (a.diasSemEntrar === null || a.diasSemEntrar >= DIAS_SUMIDO))
  const semQuestoes = c.materias.filter((m) => m.aulas_sem_questoes > 0)
  const aulasSemQuestoes = semQuestoes.reduce((s, m) => s + m.aulas_sem_questoes, 0)
  const total = c.materias.reduce((s, m) => ({ aulas: s.aulas + m.aulas, questoes: s.questoes + m.questoes, cards: s.cards + m.cards }), {
    aulas: 0,
    questoes: 0,
    cards: 0,
  })
  const entraramHoje = c.alunos.filter((a) => a.ultimoAcesso && dataBrasilia(a.ultimoAcesso) === c.hoje).length
  const entraramSemana = c.alunos.filter((a) => a.diasSemEntrar !== null && a.diasSemEntrar < 7).length
  const respondidas = c.alunos.reduce((s, a) => s + a.questoes, 0)
  const usoBanco = pct(c.bancoBytes, LIMITE_BANCO)
  const nomeMateria = new Map(c.materias.map((m) => [m.id, m.nome]))
  const prova = c.provas.find((p) => inicioMs(p) > c.agora)
  const faltam = prova ? Math.round((Date.parse(prova.data) - Date.parse(c.hoje)) / 86_400_000) : 0
  const lista = (nomes: string[]) => (nomes.length > 1 ? `${nomes.slice(0, -1).join(', ')} e ${nomes[nomes.length - 1]}` : nomes[0])

  const alertas: React.ReactNode[] = []
  if (aulasSemQuestoes)
    alertas.push(
      <Alerta
        key="questoes"
        href="#conteudo"
        tipo="aviso"
        icone={ICONE.aviso}
        titulo={`${aulasSemQuestoes} ${plural(aulasSemQuestoes, 'aula sem questões', 'aulas sem questões')}`}
        texto={`Em ${lista(semQuestoes.map((m) => m.nome))}`}
      />,
    )
  if (sumidos.length)
    alertas.push(
      <Alerta
        key="sumidos"
        href="#alunos"
        tipo="aviso"
        icone={ICONE.aluno}
        titulo={`${sumidos.length} ${plural(sumidos.length, 'aluno sumido', 'alunos sumidos')}`}
        texto={`Sem entrar há ${DIAS_SUMIDO} dias ou mais`}
      />,
    )
  for (const [i, s] of c.agenda.entries())
    if (!s.publicada)
      alertas.push(
        <Alerta
          key={s.semana}
          href="/admin/agenda"
          tipo="aviso"
          icone={ICONE.agenda}
          titulo={`Agenda ${i === 0 ? 'desta semana' : `de ${ddmm(s.semana)}`} não publicada`}
          texto="Cole o cronograma do WhatsApp em Agenda da semana"
        />,
      )
  if (c.recados.novos || c.recados.erros_abertos)
    alertas.push(
      <Alerta
        key="recados"
        href="/admin/recados"
        tipo="aviso"
        icone={ICONE.recado}
        titulo={
          c.recados.novos
            ? `${c.recados.novos} ${plural(c.recados.novos, 'recado novo', 'recados novos')}`
            : `${c.recados.erros_abertos} ${plural(c.recados.erros_abertos, 'erro apontado', 'erros apontados')} sem correção`
        }
        texto={
          c.recados.novos && c.recados.erros_abertos
            ? `${c.recados.erros_abertos} ${plural(c.recados.erros_abertos, 'erro apontado', 'erros apontados')} sem correção`
            : 'Abrir os Recados da turma'
        }
      />,
    )
  if (usoBanco >= 80)
    alertas.push(
      <Alerta
        key="banco"
        href="#saude"
        tipo="aviso"
        icone={ICONE.aviso}
        titulo={`Banco com ${usoBanco}% do espaço usado`}
        texto="Perto do limite do plano gratuito do Supabase"
      />,
    )
  if (!c.recados.novos && !c.recados.erros_abertos)
    alertas.push(
      <Alerta key="recados-ok" href="/admin/recados" tipo="ok" icone={ICONE.ok} titulo="Nenhum recado novo" texto="Nenhum erro apontado esperando correção" />,
    )

  return (
    <>
      <header className="top">
        <div>
          <div className="eyebrow">Administração</div>
          <h1 className="big">Central</h1>
          <p className="lead">
            Tudo sobre o Med Genius num lugar só · números de agora, {diaSemana(c.hoje)}, {ddmm(c.hoje)}
          </p>
        </div>
      </header>

      <div className="central">
        <div>
          <div className="sec">Precisa de você</div>
          <div className="group">{alertas}</div>

          <div className="sec">Uso da turma</div>
          <div className="stats quatro">
            <div className="stat">
              <div className="lab">Alunos</div>
              <div className="n">{c.alunos.length}</div>
            </div>
            <div className="stat">
              <div className="lab">Entraram hoje</div>
              <div className="n">{entraramHoje}</div>
            </div>
            <div className="stat">
              <div className="lab">Em 7 dias</div>
              <div className="n">{entraramSemana}</div>
            </div>
            <div className="stat">
              <div className="lab">Respondidas</div>
              <div className="n">{respondidas}</div>
            </div>
          </div>
          <div className="group ct-graf-caixa">
            <GraficoCentral dias={c.dias} />
          </div>

          <div className="sec ct-sec" id="alunos">
            <span>Alunos</span>
            <Link href="/admin">Gerenciar →</Link>
          </div>
          <div className="group">
            {c.alunos.map((a) => {
              const sumido = sumidos.includes(a)
              return (
                <div key={a.id} className="row static">
                  <span className="ct-ic ini">{a.nome.charAt(0).toUpperCase()}</span>
                  <span className="main">
                    <span className="t">
                      {a.nome}
                      {a.admin && ' (você)'}
                    </span>
                    <span className="s">
                      {a.grupo ? `Grupo ${a.grupo}` : 'Sem grupo'} ·{' '}
                      {a.questoes || a.cards
                        ? `${a.questoes} ${plural(a.questoes, 'questão', 'questões')}${a.questoes ? ` (${pct(a.certas, a.questoes)}% certas)` : ''} · ${a.cards} cards`
                        : 'nada feito ainda'}
                    </span>
                  </span>
                  <span className={`ct-acesso${sumido ? ' sumido' : ''}`}>{a.ultimoAcesso ? fmtHa(a.ultimoAcesso) : 'nunca entrou'}</span>
                </div>
              )
            })}
          </div>
          <p className="foot">À direita, o último acesso de cada um. Em amarelo, quem não entra há {DIAS_SUMIDO} dias ou mais.</p>
        </div>

        <div>
          <div className="sec ct-sec" id="conteudo">
            <span>Conteúdo no ar</span>
            <Link href="/admin/conteudo">Editar →</Link>
          </div>
          <div className="stats">
            <div className="stat">
              <div className="lab">Aulas</div>
              <div className="n">{total.aulas}</div>
            </div>
            <div className="stat">
              <div className="lab">Questões</div>
              <div className="n">{total.questoes}</div>
            </div>
            <div className="stat">
              <div className="lab">Flashcards</div>
              <div className="n">{total.cards.toLocaleString('pt-BR')}</div>
            </div>
          </div>
          <div className="group ct-mats">
            {c.materias.map((m) => {
              const aviso = !m.aulas
                ? 'Ainda sem aulas'
                : !m.questoes
                  ? 'Nenhuma questão ainda'
                  : m.aulas_sem_questoes
                    ? `${m.aulas_sem_questoes} ${plural(m.aulas_sem_questoes, 'aula sem questões', 'aulas sem questões')}`
                    : ''
              return (
                <Link
                  key={m.id}
                  className="row ct-mat"
                  href={`/materia/${m.id}`}
                  style={{ '--c1': m.cor_inicio ?? '#2563EB', '--c2': m.cor_fim ?? '#1E3A8A' } as React.CSSProperties}
                >
                  <span className="gema nome-gema">{m.nome}</span>
                  <span className="main">
                    <span className="s">
                      {m.aulas} {plural(m.aulas, 'aula', 'aulas')} · {m.questoes} {plural(m.questoes, 'questão', 'questões')} ·{' '}
                      {m.cards.toLocaleString('pt-BR')} cards
                    </span>
                    {aviso && <span className="ct-aviso">{aviso}</span>}
                  </span>
                </Link>
              )
            })}
          </div>

          <div className="sec">Questões que a turma mais erra</div>
          {c.erradas.length ? (
            <div className="group">
              {c.erradas.map((q) => (
                <div key={q.id} className="row static ct-errada">
                  <span className="ct-taxa" aria-label={`${q.erros} erros em ${q.tentativas} tentativas`}>
                    {q.erros} de {q.tentativas}
                  </span>
                  <span className="main">
                    <span className="t2">
                      {q.enunciado.replace(/\s+/g, ' ').slice(0, 120)}
                      {q.enunciado.length > 120 ? '…' : ''}
                    </span>
                    <span className="s">
                      {nomeMateria.get(q.materia_id)} · {q.alunos} {plural(q.alunos, 'aluno respondeu', 'alunos responderam')}
                    </span>
                  </span>
                  <Link
                    className="btn ghost sm"
                    href={`/admin/conteudo/questoes/${q.materia_id}?${q.aula_id ? `aula=${q.aula_id}&` : ''}q=${encodeURIComponent(q.id)}#q-${q.id}`}
                  >
                    Abrir
                  </Link>
                </div>
              ))}
            </div>
          ) : (
            <p className="vazio">Ninguém errou nenhuma questão ainda.</p>
          )}
          <p className="foot">Erros sobre o total de respostas (contando quem refez). Muita gente errando a mesma questão pode ser gabarito trocado.</p>

          <div className="ct-par">
            <div>
              <div className="sec">Recados</div>
              <Link className="group ct-bloco" href="/admin/recados">
                <span className="ct-nums">
                  <span>
                    <b>{c.recados.novos}</b> {plural(c.recados.novos, 'novo', 'novos')}
                  </span>
                  <span>
                    <b>{c.recados.erros_abertos}</b> {plural(c.recados.erros_abertos, 'erro aberto', 'erros abertos')}
                  </span>
                </span>
                <span className="ct-link">Abrir Recados →</span>
              </Link>
            </div>
            <div>
              <div className="sec">Próxima prova</div>
              {prova ? (
                <Link className="group ct-bloco ct-prova" href="/agenda#provas">
                  <span className="t">{prova.titulo}</span>
                  <span className="s">
                    {diaSemana(prova.data)}, {ddmm(prova.data)}
                    {prova.inicio && ` às ${fmtHora(prova.inicio)}`}
                  </span>
                  <span className="ct-link">{faltam === 0 ? 'É hoje' : faltam === 1 ? 'É amanhã' : `Faltam ${faltam} dias`}</span>
                  <span className="s">
                    {c.provas.length} {plural(c.provas.length, 'prova cadastrada', 'provas cadastradas')}
                  </span>
                </Link>
              ) : (
                <p className="vazio">Nenhuma prova cadastrada daqui para a frente.</p>
              )}
            </div>
          </div>

          <div className="sec" id="saude">
            Agenda e saúde do app
          </div>
          <div className="group">
            {c.agenda.map((s, i) => (
              <Link key={s.semana} className="row" href="/admin/agenda">
                <span className="main">
                  <span className="t">
                    Agenda {i === 0 ? 'desta semana' : 'da próxima semana'} ({ddmm(s.semana)})
                  </span>
                </span>
                <span className={s.publicada ? 'ct-ok' : 'ct-falta'}>{s.publicada ? 'Publicada' : 'Falta publicar'}</span>
              </Link>
            ))}
            <div className="row static ct-banco">
              <span className="main">
                <span className="t">Espaço do banco</span>
                <span className="s">
                  {mb(c.bancoBytes)} de 500 MB · {usoBanco}% usado (limite do plano gratuito do Supabase)
                </span>
                <span className="ct-medidor" role="img" aria-label={`${usoBanco}% do espaço usado`}>
                  <i style={{ width: `${Math.max(1, usoBanco)}%` }} />
                </span>
              </span>
            </div>
            <div className="row static">
              <span className="main">
                <span className="t">Site e publicações</span>
                <span className="s">Última publicação e erros do site (Vercel): por enquanto, pergunte ao Claude</span>
              </span>
              <span className="ct-breve">Em breve</span>
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

/** Data (AAAA-MM-DD) de um instante, no horário de Brasília. */
function dataBrasilia(iso: string) {
  return new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit' }).format(new Date(iso))
}
