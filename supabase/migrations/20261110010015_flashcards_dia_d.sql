-- Flashcards Dia D (regra do Mauricio, 10/11/2026): baralho de véspera de cada aula, feito para resolver
-- as questões das Provas da FAG. Tabela própria: fica fora da Revisão do dia e não guarda progresso do aluno.
create table public.flashcards_dia_d (
  id text not null,
  aula_id text not null,
  ordem integer default 0 not null,
  frente text not null,
  verso text not null,
  questoes text[] default '{}'::text[] not null, -- ids das questões FAG que o card ajuda a resolver
  constraint flashcards_dia_d_pkey primary key (id),
  constraint flashcards_dia_d_aula_id_fkey foreign key (aula_id) references public.aulas(id) on delete cascade
);
create index flashcards_dia_d_aula_idx on public.flashcards_dia_d (aula_id, ordem);
alter table public.flashcards_dia_d enable row level security;
create policy "Alunos leem os cards do Dia D" on public.flashcards_dia_d
  as permissive for select to authenticated using (true);
revoke all on public.flashcards_dia_d from anon, authenticated;
grant select on public.flashcards_dia_d to authenticated;
grant all on public.flashcards_dia_d to service_role;
