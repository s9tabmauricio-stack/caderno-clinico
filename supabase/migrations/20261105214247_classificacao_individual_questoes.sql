-- Aplicada em produção por scripts/sql.mjs em 05/11/2026; validada com supabase/tests/classificacao_questoes.sql.
-- Registro no histórico confirmado em 05/11/2026, após verificar estrutura, RLS, permissões e teste transacional.
-- Uma prioridade por aluno e questão, independente das respostas e do histórico.
create table public.classificacoes_questoes (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  questao_id text not null references public.questoes(id) on delete cascade,
  classificacao text not null check (classificacao in ('rever', 'se_der_tempo', 'basico')),
  atualizada_em timestamptz not null default now(),
  primary key (user_id, questao_id)
);

create index classificacoes_questoes_questao_idx on public.classificacoes_questoes (questao_id);
alter table public.classificacoes_questoes enable row level security;

create policy "Ver as próprias classificações" on public.classificacoes_questoes
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Marcar as próprias questões" on public.classificacoes_questoes
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Atualizar as próprias classificações" on public.classificacoes_questoes
  for update to authenticated using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
create policy "Desmarcar as próprias questões" on public.classificacoes_questoes
  for delete to authenticated using ((select auth.uid()) = user_id);

revoke all on public.classificacoes_questoes from anon, authenticated;
grant select, insert, update, delete on public.classificacoes_questoes to authenticated;
grant all on public.classificacoes_questoes to service_role;

create or replace view public.questoes_do_aluno with (security_invoker=true) as
 select q.id, q.aula_id, q.ordem, q.enunciado, q.alternativas, q.correta, q.comentario,
    r.escolhida, r.correta as acertou, r.tentativas, r.respondida_em,
    q.materia_id, q.por_que_erradas, q.tema, q.prova, q.fonte, q.origem, q.cai_na_prova,
    c.classificacao
 from public.questoes q
 left join public.aulas a on a.id = q.aula_id
 left join public.respostas r on r.questao_id = q.id and r.user_id = (select auth.uid())
 left join public.classificacoes_questoes c on c.questao_id = q.id and c.user_id = (select auth.uid())
 where (q.aula_id is null or a.publicada) and q.substituida_por is null;
