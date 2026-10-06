-- Caderno Clínico · estrutura do banco (tabelas, segurança e armazenamento)

-- ---------------------------------------------------------
-- 1. Conteúdo do site
-- ---------------------------------------------------------
create table public.materias (
  id          text primary key,
  nome        text not null,
  descricao   text,
  ordem       int  not null default 0,
  cor_inicio  text,
  cor_fim     text,
  criado_em   timestamptz not null default now()
);

create table public.aulas (
  id             text primary key,
  materia_id     text not null references public.materias (id) on delete cascade,
  ordem          int  not null,
  titulo         text not null,
  resumo         text,
  apostila_html  text,           -- resumo da apostila mostrado na página
  pdf_caminho    text,           -- caminho do PDF no armazenamento "apostilas"
  publicada      boolean not null default true,
  criado_em      timestamptz not null default now()
);
create index aulas_materia_idx on public.aulas (materia_id, ordem);

create table public.questoes (
  id            text primary key,
  aula_id       text not null references public.aulas (id) on delete cascade,
  ordem         int  not null default 0,
  enunciado     text not null,
  alternativas  jsonb not null check (jsonb_typeof(alternativas) = 'array'),
  correta       smallint not null check (correta >= 0),   -- 0 = A, 1 = B ...
  comentario    text
);
create index questoes_aula_idx on public.questoes (aula_id, ordem);

create table public.flashcards (
  id       text primary key,
  aula_id  text not null references public.aulas (id) on delete cascade,
  ordem    int  not null default 0,
  frente   text not null,
  verso    text not null
);
create index flashcards_aula_idx on public.flashcards (aula_id, ordem);

-- ---------------------------------------------------------
-- 2. Alunos e progresso
-- ---------------------------------------------------------
create table public.perfis (
  id         uuid primary key references auth.users (id) on delete cascade,
  nome       text,
  admin      boolean not null default false,
  criado_em  timestamptz not null default now()
);

-- Uma linha por questão respondida (guarda a última tentativa)
create table public.respostas (
  user_id        uuid not null default auth.uid() references auth.users (id) on delete cascade,
  questao_id     text not null references public.questoes (id) on delete cascade,
  escolhida      smallint not null,
  correta        boolean  not null,
  tentativas     int      not null default 1,
  respondida_em  timestamptz not null default now(),
  primary key (user_id, questao_id)
);

-- Uma linha por flashcard já estudado (estado da repetição espaçada)
create table public.revisoes (
  user_id          uuid not null default auth.uid() references auth.users (id) on delete cascade,
  flashcard_id     text not null references public.flashcards (id) on delete cascade,
  repeticoes       int  not null default 0,
  intervalo_dias   real not null default 0,
  facilidade       real not null default 2.5,
  lapsos           int  not null default 0,
  proxima_revisao  timestamptz not null,
  ultima_revisao   timestamptz not null default now(),
  primary key (user_id, flashcard_id)
);
create index revisoes_proxima_idx on public.revisoes (user_id, proxima_revisao);

-- Cria o perfil automaticamente quando alguém entra pela primeira vez
create or replace function public.criar_perfil()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
  insert into public.perfis (id, nome)
  values (
    new.id,
    coalesce(
      new.raw_user_meta_data ->> 'full_name',
      new.raw_user_meta_data ->> 'name',
      split_part(new.email, '@', 1)
    )
  );
  return new;
end;
$$;

create trigger ao_criar_usuario
  after insert on auth.users
  for each row execute procedure public.criar_perfil();

-- ---------------------------------------------------------
-- 3. Segurança: cada aluno só enxerga o próprio progresso
-- ---------------------------------------------------------
alter table public.materias   enable row level security;
alter table public.aulas      enable row level security;
alter table public.questoes   enable row level security;
alter table public.flashcards enable row level security;
alter table public.perfis     enable row level security;
alter table public.respostas  enable row level security;
alter table public.revisoes   enable row level security;

grant select on public.materias, public.aulas, public.questoes, public.flashcards to authenticated;
grant select, insert, update, delete on public.respostas, public.revisoes to authenticated;
grant select on public.perfis to authenticated;
-- o aluno pode trocar o próprio nome, mas nunca se tornar administrador
revoke update on public.perfis from authenticated, anon;
grant update (nome) on public.perfis to authenticated;

-- Conteúdo: qualquer aluno logado lê; só o painel do Supabase altera
create policy "Alunos leem matérias"   on public.materias   for select to authenticated using (true);
create policy "Alunos leem aulas"      on public.aulas      for select to authenticated using (publicada);
create policy "Alunos leem questões"   on public.questoes   for select to authenticated using (true);
create policy "Alunos leem flashcards" on public.flashcards for select to authenticated using (true);

-- Perfil
create policy "Ver o próprio perfil" on public.perfis
  for select to authenticated using ((select auth.uid()) = id);
create policy "Editar o próprio perfil" on public.perfis
  for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

-- Respostas das questões
create policy "Ver as próprias respostas" on public.respostas
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Registrar as próprias respostas" on public.respostas
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Atualizar as próprias respostas" on public.respostas
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "Apagar as próprias respostas" on public.respostas
  for delete to authenticated using ((select auth.uid()) = user_id);

-- Revisões dos flashcards
create policy "Ver as próprias revisões" on public.revisoes
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Registrar as próprias revisões" on public.revisoes
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Atualizar as próprias revisões" on public.revisoes
  for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
create policy "Apagar as próprias revisões" on public.revisoes
  for delete to authenticated using ((select auth.uid()) = user_id);

-- ---------------------------------------------------------
-- 4. Armazenamento dos PDFs das apostilas (privado)
-- ---------------------------------------------------------
insert into storage.buckets (id, name, public)
values ('apostilas', 'apostilas', false)
on conflict (id) do nothing;

create policy "Alunos leem apostilas" on storage.objects
  for select to authenticated using (bucket_id = 'apostilas');
