import type { Metadata } from 'next'
import { notFound } from 'next/navigation'
import { Pagina, Voltar } from '@/components/Pagina'
import { CriarAluno, LimiteAparelhos, TrocarSenha } from '@/components/AdminForms'
import { rotuloLimite } from '@/lib/aparelhos'
import { chaveConfigurada, clienteAdmin, ehAdmin } from '@/lib/admin'
import { cpfDoEmail, formatarCpf } from '@/lib/cpf'
import { sessao } from '@/lib/dados'

export const metadata: Metadata = { title: 'Alunos' }

export default async function AdminPage() {
  const { email } = await sessao()
  if (!ehAdmin(email)) notFound()

  if (!chaveConfigurada()) {
    return (
      <Pagina>
        <Voltar href="/admin/central" rotulo="Administração" />
        <header className="top">
          <h1 className="big">Alunos</h1>
        </header>
        <p className="vazio">
          Falta a chave secreta. No Supabase, em Project Settings → API Keys, copie a secret key. Na Vercel, em Settings →
          Environment Variables, crie a variável SUPABASE_SECRET_KEY com ela e publique de novo (Deployments → Redeploy).
        </p>
      </Pagina>
    )
  }

  const admin = await clienteAdmin()
  const [{ data: usuarios }, { data: perfis }] = await Promise.all([
    admin.auth.admin.listUsers({ perPage: 1000 }),
    admin.from('perfis').select('id, nome, max_aparelhos'),
  ])
  const nomes = new Map((perfis ?? []).map((p) => [p.id as string, p.nome as string | null]))
  const limites = new Map((perfis ?? []).map((p) => [p.id as string, p.max_aparelhos as number | null]))
  const alunos = (usuarios?.users ?? [])
    .map((u) => {
      const cpf = cpfDoEmail(u.email ?? '')
      const nome = nomes.get(u.id)
      const ident = cpf ? formatarCpf(cpf) : (u.email ?? '')
      return { id: u.id, nome: nome && nome !== cpf ? nome : '', ident, ultimo: u.last_sign_in_at, limite: limites.get(u.id) ?? null }
    })
    .sort((a, b) => (a.nome || a.ident).localeCompare(b.nome || b.ident, 'pt-BR'))

  return (
    <Pagina>
      <Voltar href="/admin/central" rotulo="Administração" />
      <header className="top">
        <div>
          <div className="eyebrow">Administração</div>
          <h1 className="big">Alunos</h1>
        </div>
      </header>

      <div className="sec">Novo aluno</div>
      <CriarAluno />

      <div className="sec">Trocar a senha de um aluno</div>
      <TrocarSenha alunos={alunos.map((a) => ({ id: a.id, rotulo: a.nome ? `${a.nome} · ${a.ident}` : a.ident }))} />

      <div className="sec">Aparelhos por aluno</div>
      <LimiteAparelhos
        alunos={alunos.map((a) => ({ id: a.id, rotulo: `${a.nome ? `${a.nome} · ${a.ident}` : a.ident} (${rotuloLimite(a.limite)})` }))}
      />
      <p className="painel-nota">
        Contas novas ficam abertas em 1 aparelho por vez. Quem entra num aparelho novo tira a conta do aparelho usado há mais
        tempo. Navegador e app instalado no mesmo celular contam como dois.
      </p>

      <div className="sec">
        {alunos.length} {alunos.length === 1 ? 'conta' : 'contas'}
      </div>
      <div className="group">
        {alunos.map((a) => (
          <div key={a.id} className="row static">
            <span className="main">
              <span className="t">{a.nome || a.ident}</span>
              <span className="s">
                {a.nome ? `${a.ident} · ` : ''}
                {rotuloLimite(a.limite)} · 
                {a.ultimo ? `último acesso ${new Date(a.ultimo).toLocaleDateString('pt-BR', { timeZone: 'America/Sao_Paulo' })}` : 'nunca entrou'}
              </span>
            </span>
          </div>
        ))}
      </div>
    </Pagina>
  )
}
