-- Progresso dos Flashcards Dia D (pedido do Mauricio, 10/11/2026): o aluno sai da aula e, ao voltar,
-- continua de onde parou, em qualquer aparelho. Uma linha por aluno e aula, com a fila que falta,
-- os cards que já passaram e os que ele errou. Continua fora da Revisão do dia.
create table public.progresso_dia_d (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  aula_id text not null references public.aulas(id) on delete cascade,
  fila text[] not null default '{}'::text[],  -- ids dos cards que faltam, na ordem; vazia = baralho fechado
  erros text[] not null default '{}'::text[], -- cards que ele não sabia em alguma volta
  feitos integer not null default 0,          -- cards marcados como "Sabia"
  atualizado_em timestamptz not null default now(),
  primary key (user_id, aula_id)
);
create index progresso_dia_d_aula_idx on public.progresso_dia_d (aula_id);
alter table public.progresso_dia_d enable row level security;

create policy "Ver o próprio progresso do Dia D" on public.progresso_dia_d
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Guardar o próprio progresso do Dia D" on public.progresso_dia_d
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Atualizar o próprio progresso do Dia D" on public.progresso_dia_d
  for update to authenticated using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
create policy "Recomeçar o próprio Dia D" on public.progresso_dia_d
  for delete to authenticated using ((select auth.uid()) = user_id);

revoke all on public.progresso_dia_d from anon, authenticated;
grant select, insert, update, delete on public.progresso_dia_d to authenticated;
grant all on public.progresso_dia_d to service_role;
