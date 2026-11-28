-- Turmas (28/11/2026): T28 e T29 no mesmo app, cada uma vê só as próprias matérias e a própria agenda.
-- perfis.turma: 't28' ou 't29' (contas novas nascem T29); vazio = vê todas (o administrador).
-- materias.turmas: de quais turmas é a matéria (uma matéria pode servir às duas).
-- agenda_semanas.turma: de qual turma é a semana; os eventos seguem a semana.
-- Questões, flashcards, cards do Dia D e aulas seguem a matéria; as visões das telas (security_invoker) herdam o filtro.
-- A chave secreta (Administração, scripts) não passa pela RLS e continua vendo tudo.

alter table public.perfis add column turma text default 't29';
alter table public.perfis add constraint perfis_turma_check check (turma is null or turma in ('t28', 't29'));
update public.perfis set turma = 't29';

alter table public.materias add column turmas text[] not null default '{t29}';
update public.materias set turmas = '{t28}' where id = 'neuro';

alter table public.agenda_semanas add column turma text not null default 't29';

-- Laura é da T28; a conta do administrador (CPF) vê todas.
update public.perfis set turma = 't28' where id = 'b4ba0f8c-3b95-4a92-a1c9-858b36450aac';
update public.perfis set turma = null where id = '4629e618-8b2c-4a6a-90fb-718c4239f2f6';

-- Quem entrou vê o que é de uma destas turmas? Sem perfil = T29; perfil com turma vazia = vê tudo.
create or replace function public.ve_turma(turmas text[])
 returns boolean
 language sql
 stable security definer
 set search_path to ''
as $function$
  select coalesce(
    (select p.turma is null or p.turma = any(turmas) from public.perfis p where p.id = (select auth.uid())),
    't29' = any(turmas))
$function$;
revoke all on function public.ve_turma(text[]) from public, anon;
grant execute on function public.ve_turma(text[]) to authenticated;

drop policy "Alunos leem matérias" on public.materias;
create policy "Alunos leem as matérias da turma" on public.materias as permissive for select to authenticated
  using (public.ve_turma(turmas));

drop policy "Alunos leem aulas" on public.aulas;
create policy "Alunos leem as aulas da turma" on public.aulas as permissive for select to authenticated
  using (publicada and materia_id in (select m.id from public.materias m));

drop policy "Alunos leem questões" on public.questoes;
create policy "Alunos leem as questões da turma" on public.questoes as permissive for select to authenticated
  using (materia_id in (select m.id from public.materias m));

drop policy "Alunos leem flashcards" on public.flashcards;
create policy "Alunos leem os flashcards da turma" on public.flashcards as permissive for select to authenticated
  using (aula_id in (select a.id from public.aulas a));

drop policy "Alunos leem os cards do Dia D" on public.flashcards_dia_d;
create policy "Alunos leem os cards do Dia D da turma" on public.flashcards_dia_d as permissive for select to authenticated
  using (aula_id in (select a.id from public.aulas a));

drop policy "Alunos leem as semanas" on public.agenda_semanas;
create policy "Alunos leem as semanas da turma" on public.agenda_semanas as permissive for select to authenticated
  using (public.ve_turma(array[turma]));

drop policy "Alunos leem a agenda" on public.agenda_eventos;
create policy "Alunos leem a agenda da turma" on public.agenda_eventos as permissive for select to authenticated
  using (semana in (select s.semana from public.agenda_semanas s));
