-- Recados da turma embaixo de cada questão: insights para os colegas e avisos de erro
-- (aplicada pelo conector em 08/10/2026; cópia para referência)
create table public.recados (
  id uuid primary key default gen_random_uuid(),
  questao_id text not null references public.questoes(id) on delete cascade,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  autor text not null default 'Colega',
  tipo text not null check (tipo in ('insight', 'erro')),
  texto text not null check (char_length(btrim(texto)) between 1 and 1000),
  status text not null default 'novo' check (status in ('novo', 'visto', 'corrigido')),
  criado_em timestamptz not null default now()
);
create index recados_questao_idx on public.recados (questao_id, criado_em);
create index recados_novos_idx on public.recados (criado_em) where status = 'novo';
create index recados_user_idx on public.recados (user_id);

create table public.recados_uteis (
  recado_id uuid not null references public.recados(id) on delete cascade,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  primary key (recado_id, user_id)
);
create index recados_uteis_user_idx on public.recados_uteis (user_id);

-- Quem escreve é sempre o aluno logado; nome (primeiro nome do perfil) e status saem do servidor
create or replace function public.recados_preencher()
returns trigger
language plpgsql
security definer
set search_path = ''
as $$
begin
  if auth.uid() is not null then
    new.user_id := auth.uid();
    new.status := 'novo';
    new.criado_em := now();
    new.autor := coalesce(
      nullif(split_part(btrim((select p.nome from public.perfis p where p.id = auth.uid())), ' ', 1), ''),
      'Colega'
    );
  end if;
  new.texto := btrim(new.texto);
  return new;
end;
$$;
revoke execute on function public.recados_preencher() from public, anon, authenticated;
create trigger recados_preencher before insert on public.recados
  for each row execute function public.recados_preencher();

alter table public.recados enable row level security;
alter table public.recados_uteis enable row level security;

create policy "Turma lê os recados" on public.recados for select to authenticated using (true);
create policy "Aluno escreve o próprio recado" on public.recados for insert to authenticated
  with check ((select auth.uid()) = user_id);
create policy "Aluno apaga o próprio recado" on public.recados for delete to authenticated
  using ((select auth.uid()) = user_id);

create policy "Turma lê os votos de útil" on public.recados_uteis for select to authenticated using (true);
create policy "Aluno marca útil" on public.recados_uteis for insert to authenticated
  with check ((select auth.uid()) = user_id);
create policy "Aluno desmarca útil" on public.recados_uteis for delete to authenticated
  using ((select auth.uid()) = user_id);

revoke all on public.recados, public.recados_uteis from anon, authenticated;
grant select, insert, delete on public.recados to authenticated;
grant select, insert, delete on public.recados_uteis to authenticated;
