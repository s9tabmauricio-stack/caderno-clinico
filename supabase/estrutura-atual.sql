-- Estrutura atual do banco do Med Genius (Supabase, projeto xtlpmtylifbalzxnfkib)
-- Copiada do próprio banco em 02/11/2026 (PostgreSQL 17.11); campo questoes.cai_na_prova incluído em 03/11/2026. Só a estrutura, sem dados.
-- Classificação pessoal de questões incluída em 05/11/2026: migração 20261105214247_classificacao_individual_questoes.sql.
-- Suspensão individual aplicada em 03/11/2026: migração 20261103162543_suspensao_individual_flashcards.sql.
--
-- Para que serve: é a referência confiável de como o banco está montado
-- (tabelas, regras, visões, funções, gatilhos e permissões do esquema public).
-- As migrações em supabase/migrations/ não contam toda a história; esta cópia conta.
--
-- Não rode este arquivo no banco que está no ar: ele descreve o que já existe.
-- Mudou a estrutura (migração nova)? Gere a cópia de novo, como explicado em docs/banco.md.
--
-- Extensões: plpgsql, pg_stat_statements, uuid-ossp, pgcrypto, supabase_vault.

-- ============================================================
-- Tabelas
-- ============================================================

create table public.agenda_eventos (
  id bigint generated always as identity not null,
  semana date not null,
  data date not null,
  inicio time without time zone,
  fim time without time zone,
  materia text,
  tipo text default 'aula'::text not null,
  titulo text not null,
  professor text,
  local text,
  grupos integer[],
  cancelado boolean default false not null,
  notas text[],
  ordem integer default 0 not null,
  fixo boolean default false not null,
  constraint agenda_eventos_pkey PRIMARY KEY (id),
  constraint agenda_eventos_semana_fkey FOREIGN KEY (semana) REFERENCES agenda_semanas(semana) ON DELETE CASCADE
);

create table public.agenda_semanas (
  semana date not null,
  titulo text,
  aviso text,
  texto text,
  atualizado_em timestamp with time zone default now() not null,
  constraint agenda_semanas_pkey PRIMARY KEY (semana)
);

create table public.aulas (
  id text not null,
  materia_id text not null,
  ordem integer not null,
  titulo text not null,
  resumo text,
  apostila_html text,
  pdf_caminho text,
  publicada boolean default true not null,
  criado_em timestamp with time zone default now() not null,
  data_aula date,
  professor text,
  constraint aulas_pkey PRIMARY KEY (id),
  constraint aulas_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE
);

create table public.flashcards (
  id text not null,
  aula_id text not null,
  ordem integer default 0 not null,
  frente text not null,
  verso text not null,
  constraint flashcards_pkey PRIMARY KEY (id),
  constraint flashcards_aula_id_fkey FOREIGN KEY (aula_id) REFERENCES aulas(id) ON DELETE CASCADE
);

create table public.historico_respostas (
  id bigint generated always as identity not null,
  user_id uuid default auth.uid() not null,
  questao_id text not null,
  escolhida smallint not null,
  correta boolean not null,
  respondida_em timestamp with time zone default now() not null,
  constraint historico_respostas_pkey PRIMARY KEY (id),
  constraint historico_respostas_questao_id_fkey FOREIGN KEY (questao_id) REFERENCES questoes(id) ON DELETE CASCADE,
  constraint historico_respostas_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

create table public.historico_revisoes (
  id bigint generated always as identity not null,
  user_id uuid not null,
  flashcard_id text not null,
  errou boolean not null,
  intervalo_dias real not null,
  revisada_em timestamp with time zone default now() not null,
  constraint historico_revisoes_pkey PRIMARY KEY (id),
  constraint historico_revisoes_flashcard_id_fkey FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE,
  constraint historico_revisoes_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

create table public.materias (
  id text not null,
  nome text not null,
  descricao text,
  ordem integer default 0 not null,
  cor_inicio text,
  cor_fim text,
  criado_em timestamp with time zone default now() not null,
  constraint materias_pkey PRIMARY KEY (id)
);

create table public.perfis (
  id uuid not null,
  nome text,
  admin boolean default false not null,
  criado_em timestamp with time zone default now() not null,
  grupo integer,
  constraint perfis_pkey PRIMARY KEY (id),
  constraint perfis_grupo_check CHECK (((grupo >= 1) AND (grupo <= 99))),
  constraint perfis_id_fkey FOREIGN KEY (id) REFERENCES auth.users(id) ON DELETE CASCADE
);

create table public.questoes (
  id text not null,
  aula_id text,
  ordem integer default 0 not null,
  enunciado text not null,
  alternativas jsonb not null,
  correta smallint not null,
  comentario text,
  materia_id text not null,
  tema text,
  prova text,
  fonte text,
  origem text,
  por_que_erradas text,
  substituida_por text,
  cai_na_prova boolean default false not null,
  constraint questoes_pkey PRIMARY KEY (id),
  constraint questoes_alternativas_check CHECK ((jsonb_typeof(alternativas) = 'array'::text)),
  constraint questoes_correta_check CHECK ((correta >= 0)),
  constraint questoes_aula_id_fkey FOREIGN KEY (aula_id) REFERENCES aulas(id) ON DELETE CASCADE,
  constraint questoes_materia_id_fkey FOREIGN KEY (materia_id) REFERENCES materias(id) ON DELETE CASCADE,
  constraint questoes_substituida_por_fkey FOREIGN KEY (substituida_por) REFERENCES questoes(id)
);

create table public.recados (
  id uuid default gen_random_uuid() not null,
  questao_id text not null,
  user_id uuid default auth.uid() not null,
  autor text default 'Colega'::text not null,
  tipo text not null,
  texto text not null,
  status text default 'novo'::text not null,
  criado_em timestamp with time zone default now() not null,
  constraint recados_pkey PRIMARY KEY (id),
  constraint recados_status_check CHECK ((status = ANY (ARRAY['novo'::text, 'visto'::text, 'corrigido'::text]))),
  constraint recados_texto_check CHECK (((char_length(btrim(texto)) >= 1) AND (char_length(btrim(texto)) <= 1000))),
  constraint recados_tipo_check CHECK ((tipo = ANY (ARRAY['insight'::text, 'erro'::text]))),
  constraint recados_questao_id_fkey FOREIGN KEY (questao_id) REFERENCES questoes(id) ON DELETE CASCADE,
  constraint recados_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

create table public.recados_uteis (
  recado_id uuid not null,
  user_id uuid default auth.uid() not null,
  constraint recados_uteis_pkey PRIMARY KEY (recado_id, user_id),
  constraint recados_uteis_recado_id_fkey FOREIGN KEY (recado_id) REFERENCES recados(id) ON DELETE CASCADE,
  constraint recados_uteis_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

create table public.respostas (
  user_id uuid default auth.uid() not null,
  questao_id text not null,
  escolhida smallint not null,
  correta boolean not null,
  tentativas integer default 1 not null,
  respondida_em timestamp with time zone default now() not null,
  constraint respostas_pkey PRIMARY KEY (user_id, questao_id),
  constraint respostas_questao_id_fkey FOREIGN KEY (questao_id) REFERENCES questoes(id) ON DELETE CASCADE,
  constraint respostas_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

create table public.revisoes (
  user_id uuid default auth.uid() not null,
  flashcard_id text not null,
  repeticoes integer default 0 not null,
  intervalo_dias real default 0 not null,
  facilidade real default 2.5 not null,
  lapsos integer default 0 not null,
  proxima_revisao timestamp with time zone not null,
  ultima_revisao timestamp with time zone default now() not null,
  constraint revisoes_pkey PRIMARY KEY (user_id, flashcard_id),
  constraint revisoes_flashcard_id_fkey FOREIGN KEY (flashcard_id) REFERENCES flashcards(id) ON DELETE CASCADE,
  constraint revisoes_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);

-- Suspensão individual, sem alterar avaliações, agendamento ou histórico.
create table public.flashcards_suspensos (
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  flashcard_id text not null references public.flashcards(id) on delete cascade,
  suspenso_em timestamptz not null default now(),
  primary key (user_id, flashcard_id)
);

-- O índice inverso também atende a exclusão de conteúdo por chave estrangeira.
create index flashcards_suspensos_card_idx on public.flashcards_suspensos (flashcard_id);
alter table public.flashcards_suspensos enable row level security;

create policy "Ver os próprios cards suspensos" on public.flashcards_suspensos
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "Suspender os próprios cards" on public.flashcards_suspensos
  for insert to authenticated with check ((select auth.uid()) = user_id);
create policy "Atualizar as próprias suspensões" on public.flashcards_suspensos
  for update to authenticated using ((select auth.uid()) = user_id)
  with check ((select auth.uid()) = user_id);
create policy "Reativar os próprios cards" on public.flashcards_suspensos
  for delete to authenticated using ((select auth.uid()) = user_id);

revoke all on public.flashcards_suspensos from anon, authenticated;
grant select, insert, update, delete on public.flashcards_suspensos to authenticated;
grant all on public.flashcards_suspensos to service_role;


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

-- ============================================================
-- Índices (além das chaves)
-- ============================================================

CREATE INDEX agenda_eventos_data_idx ON public.agenda_eventos USING btree (data, ordem);
CREATE INDEX agenda_eventos_semana_idx ON public.agenda_eventos USING btree (semana);
CREATE INDEX aulas_materia_idx ON public.aulas USING btree (materia_id, ordem);
CREATE INDEX flashcards_aula_idx ON public.flashcards USING btree (aula_id, ordem);
CREATE INDEX historico_respostas_aluno_idx ON public.historico_respostas USING btree (user_id, questao_id, respondida_em);
CREATE INDEX historico_revisoes_aluno_idx ON public.historico_revisoes USING btree (user_id, flashcard_id, revisada_em);
CREATE INDEX historico_revisoes_dia_idx ON public.historico_revisoes USING btree (revisada_em);
CREATE INDEX questoes_aula_idx ON public.questoes USING btree (aula_id, ordem);
CREATE INDEX questoes_materia_idx ON public.questoes USING btree (materia_id, tema);
CREATE INDEX recados_novos_idx ON public.recados USING btree (criado_em) WHERE (status = 'novo'::text);
CREATE INDEX recados_questao_idx ON public.recados USING btree (questao_id, criado_em);
CREATE INDEX recados_user_idx ON public.recados USING btree (user_id);
CREATE INDEX recados_uteis_user_idx ON public.recados_uteis USING btree (user_id);
CREATE INDEX respostas_questao_idx ON public.respostas USING btree (questao_id);
CREATE INDEX revisoes_flashcard_idx ON public.revisoes USING btree (flashcard_id);
CREATE INDEX revisoes_proxima_idx ON public.revisoes USING btree (user_id, proxima_revisao);

-- ============================================================
-- Visões usadas pelas telas (todas com security_invoker: valem as regras do aluno)
-- ============================================================

create or replace view public.flashcards_do_aluno with (security_invoker = true) as
 SELECT f.id,
    f.aula_id,
    f.ordem,
    f.frente,
    f.verso,
    a.titulo AS aula_titulo,
    a.ordem AS aula_ordem,
    m.id AS materia_id,
    m.nome AS materia_nome,
    m.ordem AS materia_ordem,
    v.repeticoes,
    v.intervalo_dias,
    v.facilidade,
    v.lapsos,
    v.proxima_revisao,
    v.ultima_revisao,
    EXISTS (SELECT 1 FROM public.flashcards_suspensos s
      WHERE s.flashcard_id = f.id AND s.user_id = (SELECT auth.uid())) AS suspenso
   FROM flashcards f
     JOIN aulas a ON a.id = f.aula_id AND a.publicada
     JOIN materias m ON m.id = a.materia_id
     LEFT JOIN revisoes v ON v.flashcard_id = f.id AND v.user_id = (( SELECT auth.uid() AS uid));

create or replace view public.progresso_aulas with (security_invoker = true) as
 SELECT id AS aula_id,
    materia_id,
    ordem,
    titulo,
    ( SELECT count(*)::integer AS count
           FROM questoes q
          WHERE q.aula_id = a.id AND q.substituida_por IS NULL) AS total_questoes,
    ( SELECT count(*)::integer AS count
           FROM respostas r
             JOIN questoes q ON q.id = r.questao_id
          WHERE q.aula_id = a.id AND q.substituida_por IS NULL AND r.user_id = (( SELECT auth.uid() AS uid))) AS respondidas,
    ( SELECT count(*)::integer AS count
           FROM respostas r
             JOIN questoes q ON q.id = r.questao_id
          WHERE q.aula_id = a.id AND q.substituida_por IS NULL AND r.user_id = (( SELECT auth.uid() AS uid)) AND r.correta) AS acertos,
    ( SELECT count(*)::integer AS count
           FROM flashcards f
          WHERE f.aula_id = a.id) AS total_cards,
    ( SELECT count(*)::integer AS count
           FROM revisoes v
             JOIN flashcards f ON f.id = v.flashcard_id
          WHERE f.aula_id = a.id AND v.user_id = (( SELECT auth.uid() AS uid))) AS cards_estudados,
    ( SELECT count(*)::integer AS count
           FROM revisoes v
             JOIN flashcards f ON f.id = v.flashcard_id
          WHERE f.aula_id = a.id AND v.user_id = (( SELECT auth.uid() AS uid)) AND v.proxima_revisao <= now()) AS cards_vencidos,
    GREATEST(( SELECT max(r.respondida_em) AS max
           FROM respostas r
             JOIN questoes q ON q.id = r.questao_id
          WHERE q.aula_id = a.id AND r.user_id = (( SELECT auth.uid() AS uid))), ( SELECT max(v.ultima_revisao) AS max
           FROM revisoes v
             JOIN flashcards f ON f.id = v.flashcard_id
          WHERE f.aula_id = a.id AND v.user_id = (( SELECT auth.uid() AS uid)))) AS ultima_atividade,
    susp.cards_suspensos,
    susp.cards_suspensos_estudados,
    susp.cards_suspensos_vencidos
   FROM aulas a
   LEFT JOIN LATERAL (
     SELECT count(*)::integer AS cards_suspensos,
       count(v.flashcard_id)::integer AS cards_suspensos_estudados,
       count(*) FILTER (WHERE v.proxima_revisao <= now())::integer AS cards_suspensos_vencidos
     FROM public.flashcards_suspensos s
     JOIN public.flashcards f ON f.id = s.flashcard_id
     LEFT JOIN public.revisoes v ON v.flashcard_id = s.flashcard_id AND v.user_id = s.user_id
     WHERE s.user_id = (SELECT auth.uid()) AND f.aula_id = a.id
   ) susp ON true
  WHERE publicada;

create or replace view public.progresso_materias with (security_invoker=true) as
 SELECT id AS materia_id,
    ( SELECT (count(*))::integer AS count
           FROM (questoes q
             LEFT JOIN aulas a ON ((a.id = q.aula_id)))
          WHERE ((q.materia_id = m.id) AND ((q.aula_id IS NULL) OR a.publicada) AND (q.substituida_por IS NULL))) AS total_questoes,
    ( SELECT (count(*))::integer AS count
           FROM ((respostas r
             JOIN questoes q ON ((q.id = r.questao_id)))
             LEFT JOIN aulas a ON ((a.id = q.aula_id)))
          WHERE ((q.materia_id = m.id) AND ((q.aula_id IS NULL) OR a.publicada) AND (q.substituida_por IS NULL) AND (r.user_id = ( SELECT auth.uid() AS uid)))) AS respondidas,
    ( SELECT (count(*))::integer AS count
           FROM ((respostas r
             JOIN questoes q ON ((q.id = r.questao_id)))
             LEFT JOIN aulas a ON ((a.id = q.aula_id)))
          WHERE ((q.materia_id = m.id) AND ((q.aula_id IS NULL) OR a.publicada) AND (q.substituida_por IS NULL) AND (r.user_id = ( SELECT auth.uid() AS uid)) AND r.correta)) AS acertos
   FROM materias m;

create or replace view public.progresso_temas with (security_invoker=true) as
 SELECT q.materia_id,
    COALESCE(q.tema, 'Sem tema'::text) AS tema,
    (count(*))::integer AS total_questoes,
    (count(r.questao_id))::integer AS respondidas,
    (count(*) FILTER (WHERE r.correta))::integer AS acertos
   FROM ((questoes q
     LEFT JOIN aulas a ON ((a.id = q.aula_id)))
     LEFT JOIN respostas r ON (((r.questao_id = q.id) AND (r.user_id = ( SELECT auth.uid() AS uid)))))
  WHERE (((q.aula_id IS NULL) OR a.publicada) AND (q.substituida_por IS NULL))
  GROUP BY q.materia_id, COALESCE(q.tema, 'Sem tema'::text);

create or replace view public.progresso_tentativas with (security_invoker=true) as
 SELECT q.materia_id,
    (count(*))::integer AS tentativas,
    (count(*) FILTER (WHERE (h.n = 1)))::integer AS primeiras,
    (count(*) FILTER (WHERE ((h.n = 1) AND h.correta)))::integer AS acertos_primeira
   FROM ((( SELECT x.id,
            x.user_id,
            x.questao_id,
            x.escolhida,
            x.correta,
            x.respondida_em,
            row_number() OVER (PARTITION BY x.questao_id ORDER BY x.respondida_em, x.id) AS n
           FROM historico_respostas x
          WHERE (x.user_id = ( SELECT auth.uid() AS uid))) h
     JOIN questoes q ON ((q.id = h.questao_id)))
     LEFT JOIN aulas a ON ((a.id = q.aula_id)))
  WHERE ((q.substituida_por IS NULL) AND ((q.aula_id IS NULL) OR a.publicada))
  GROUP BY q.materia_id;

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

-- ============================================================
-- Funções
-- ============================================================

-- Números da Central (/admin/central). Só a chave secreta chama (sem execute para anon/authenticated).
CREATE OR REPLACE FUNCTION public.central_resumo()
 RETURNS jsonb
 LANGUAGE sql
 STABLE SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
with hoje as (select (now() at time zone 'America/Sao_Paulo')::date as data)
select jsonb_build_object(
  'alunos', (
    select coalesce(jsonb_agg(x order by x.ultimo_acesso desc nulls last), '[]'::jsonb) from (
      select u.id, u.email, p.nome, p.grupo, u.last_sign_in_at as ultimo_acesso,
        (select count(*) from respostas r where r.user_id = u.id) as questoes,
        (select count(*) from respostas r where r.user_id = u.id and r.correta) as certas,
        (select count(*) from revisoes v where v.user_id = u.id) as cards
      from auth.users u left join perfis p on p.id = u.id
    ) x),
  'dias', (
    select jsonb_agg(jsonb_build_object(
      'dia', g.dia::date,
      'questoes', (select count(*) from historico_respostas h
                   where (h.respondida_em at time zone 'America/Sao_Paulo')::date = g.dia::date),
      'cards', (select count(*) from historico_revisoes h
                where (h.revisada_em at time zone 'America/Sao_Paulo')::date = g.dia::date)
    ) order by g.dia)
    from hoje, generate_series(hoje.data - 13, hoje.data, interval '1 day') as g(dia)),
  'materias', (
    select coalesce(jsonb_agg(jsonb_build_object(
      'id', m.id, 'nome', m.nome, 'cor_inicio', m.cor_inicio, 'cor_fim', m.cor_fim,
      'aulas', (select count(*) from aulas a where a.materia_id = m.id and a.publicada),
      'questoes', (select count(*) from questoes q left join aulas a on a.id = q.aula_id
                   where q.materia_id = m.id and q.substituida_por is null and (q.aula_id is null or a.publicada)),
      'cards', (select count(*) from flashcards f join aulas a on a.id = f.aula_id
                where a.materia_id = m.id and a.publicada),
      'aulas_sem_questoes', (select count(*) from aulas a where a.materia_id = m.id and a.publicada
                             and not exists (select 1 from questoes q where q.aula_id = a.id and q.substituida_por is null))
    ) order by m.ordem), '[]'::jsonb) from materias m),
  'erradas', (
    select coalesce(jsonb_agg(x order by x.erros desc, x.tentativas desc), '[]'::jsonb) from (
      select q.id, q.materia_id, q.aula_id, left(q.enunciado, 200) as enunciado,
        count(*) as tentativas, count(*) filter (where not h.correta) as erros, count(distinct h.user_id) as alunos
      from historico_respostas h
      join questoes q on q.id = h.questao_id
      left join aulas a on a.id = q.aula_id
      where q.substituida_por is null and (q.aula_id is null or a.publicada)
      group by q.id
      having count(*) filter (where not h.correta) > 0
      order by erros desc, tentativas desc
      limit 5
    ) x),
  'recados', jsonb_build_object(
    'novos', (select count(*) from recados where status = 'novo'),
    'erros_abertos', (select count(*) from recados where tipo = 'erro' and status <> 'corrigido')),
  'banco_bytes', pg_database_size(current_database())
);
$function$
;

-- Cria o perfil quando o administrador cria a conta (gatilho em auth.users).
CREATE OR REPLACE FUNCTION public.criar_perfil()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
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
$function$
;

-- Recado novo: autor (primeiro nome), dono, status e data saem daqui, não do aluno.
CREATE OR REPLACE FUNCTION public.recados_preencher()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
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
$function$
;

-- Cada resposta nova ou refeita vira uma linha em historico_respostas.
CREATE OR REPLACE FUNCTION public.registrar_historico_resposta()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
begin
  if tg_op = 'UPDATE' and new.respondida_em is not distinct from old.respondida_em then
    return new;
  end if;
  begin
    insert into public.historico_respostas (user_id, questao_id, escolhida, correta, respondida_em)
    values (new.user_id, new.questao_id, new.escolhida, new.correta, coalesce(new.respondida_em, now()));
  exception when others then
    null;
  end;
  return new;
end;
$function$
;

-- Cada avaliação de flashcard vira uma linha em historico_revisoes;
-- "Desfazer" tira a linha desfeita e apagar o card de revisoes apaga o histórico dele.
CREATE OR REPLACE FUNCTION public.registrar_historico_revisao()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO 'public'
AS $function$
begin
  begin
    if tg_op = 'DELETE' then
      delete from public.historico_revisoes where user_id = old.user_id and flashcard_id = old.flashcard_id;
      return old;
    end if;
    if tg_op = 'UPDATE' and new.ultima_revisao < old.ultima_revisao then
      delete from public.historico_revisoes
      where user_id = old.user_id and flashcard_id = old.flashcard_id and revisada_em = old.ultima_revisao;
      return new;
    end if;
    if tg_op = 'UPDATE' and new.ultima_revisao = old.ultima_revisao then
      return new;
    end if;
    insert into public.historico_revisoes (user_id, flashcard_id, errou, intervalo_dias, revisada_em)
    values (new.user_id, new.flashcard_id,
            new.lapsos > (case when tg_op = 'UPDATE' then old.lapsos else 0 end),
            new.intervalo_dias, new.ultima_revisao);
  exception when others then
    null;
  end;
  if tg_op = 'DELETE' then
    return old;
  end if;
  return new;
end;
$function$
;

-- Nenhuma função acima pode ser chamada por anon ou authenticated.
revoke execute on function public.central_resumo() from public, anon, authenticated;
revoke execute on function public.criar_perfil() from public, anon, authenticated;
revoke execute on function public.recados_preencher() from public, anon, authenticated;
revoke execute on function public.registrar_historico_resposta() from public, anon, authenticated;
revoke execute on function public.registrar_historico_revisao() from public, anon, authenticated;

-- ============================================================
-- Gatilhos
-- ============================================================

CREATE TRIGGER ao_criar_usuario AFTER INSERT ON auth.users FOR EACH ROW EXECUTE FUNCTION criar_perfil();
CREATE TRIGGER recados_preencher BEFORE INSERT ON public.recados FOR EACH ROW EXECUTE FUNCTION recados_preencher();
CREATE TRIGGER respostas_historico AFTER INSERT OR UPDATE ON public.respostas FOR EACH ROW EXECUTE FUNCTION registrar_historico_resposta();
CREATE TRIGGER revisoes_historico AFTER INSERT OR DELETE OR UPDATE ON public.revisoes FOR EACH ROW EXECUTE FUNCTION registrar_historico_revisao();

-- ============================================================
-- Segurança por linha (RLS): ligada em todas as tabelas
-- ============================================================

alter table public.agenda_eventos enable row level security;
alter table public.agenda_semanas enable row level security;
alter table public.aulas enable row level security;
alter table public.flashcards enable row level security;
alter table public.historico_respostas enable row level security;
alter table public.historico_revisoes enable row level security;
alter table public.materias enable row level security;
alter table public.perfis enable row level security;
alter table public.questoes enable row level security;
alter table public.recados enable row level security;
alter table public.recados_uteis enable row level security;
alter table public.respostas enable row level security;
alter table public.revisoes enable row level security;

create policy "Alunos leem a agenda" on public.agenda_eventos as permissive for select to authenticated using (true);
create policy "Alunos leem as semanas" on public.agenda_semanas as permissive for select to authenticated using (true);
create policy "Alunos leem aulas" on public.aulas as permissive for select to authenticated using (publicada);
create policy "Alunos leem flashcards" on public.flashcards as permissive for select to authenticated using (true);
create policy "Apagar o próprio histórico" on public.historico_respostas as permissive for delete to public using ((( SELECT auth.uid() AS uid) = user_id));
create policy "Ver o próprio histórico" on public.historico_respostas as permissive for select to public using ((( SELECT auth.uid() AS uid) = user_id));
create policy "Ver o próprio histórico de revisões" on public.historico_revisoes as permissive for select to public using ((( SELECT auth.uid() AS uid) = user_id));
create policy "Alunos leem matérias" on public.materias as permissive for select to authenticated using (true);
create policy "Editar o próprio perfil" on public.perfis as permissive for update to authenticated using ((( SELECT auth.uid() AS uid) = id)) with check ((( SELECT auth.uid() AS uid) = id));
create policy "Ver o próprio perfil" on public.perfis as permissive for select to authenticated using ((( SELECT auth.uid() AS uid) = id));
create policy "Alunos leem questões" on public.questoes as permissive for select to authenticated using (true);
create policy "Aluno apaga o próprio recado" on public.recados as permissive for delete to authenticated using ((( SELECT auth.uid() AS uid) = user_id));
create policy "Aluno escreve o próprio recado" on public.recados as permissive for insert to authenticated with check ((( SELECT auth.uid() AS uid) = user_id));
create policy "Turma lê os recados" on public.recados as permissive for select to authenticated using (true);
create policy "Aluno desmarca útil" on public.recados_uteis as permissive for delete to authenticated using ((( SELECT auth.uid() AS uid) = user_id));
create policy "Aluno marca útil" on public.recados_uteis as permissive for insert to authenticated with check ((( SELECT auth.uid() AS uid) = user_id));
create policy "Turma lê os votos de útil" on public.recados_uteis as permissive for select to authenticated using (true);
create policy "Apagar as próprias respostas" on public.respostas as permissive for delete to authenticated using ((( SELECT auth.uid() AS uid) = user_id));
create policy "Atualizar as próprias respostas" on public.respostas as permissive for update to authenticated using ((( SELECT auth.uid() AS uid) = user_id)) with check ((( SELECT auth.uid() AS uid) = user_id));
create policy "Registrar as próprias respostas" on public.respostas as permissive for insert to authenticated with check ((( SELECT auth.uid() AS uid) = user_id));
create policy "Ver as próprias respostas" on public.respostas as permissive for select to authenticated using ((( SELECT auth.uid() AS uid) = user_id));
create policy "Apagar as próprias revisões" on public.revisoes as permissive for delete to authenticated using ((( SELECT auth.uid() AS uid) = user_id));
create policy "Atualizar as próprias revisões" on public.revisoes as permissive for update to authenticated using ((( SELECT auth.uid() AS uid) = user_id)) with check ((( SELECT auth.uid() AS uid) = user_id));
create policy "Registrar as próprias revisões" on public.revisoes as permissive for insert to authenticated with check ((( SELECT auth.uid() AS uid) = user_id));
create policy "Ver as próprias revisões" on public.revisoes as permissive for select to authenticated using ((( SELECT auth.uid() AS uid) = user_id));

-- ============================================================
-- Permissões das tabelas e visões
-- O padrão do Supabase dá tudo a anon e authenticated; quem barra é a RLS acima.
-- As exceções (perfis, recados, recados_uteis) estão marcadas.
-- ============================================================

grant delete, insert, references, select, trigger, truncate, update on
  public.agenda_eventos, public.agenda_semanas, public.aulas, public.flashcards,
  public.historico_respostas, public.historico_revisoes, public.materias, public.questoes,
  public.respostas, public.revisoes,
  public.flashcards_do_aluno, public.progresso_aulas, public.progresso_materias,
  public.progresso_temas, public.progresso_tentativas, public.questoes_do_aluno
  to anon, authenticated;

-- Exceção: perfis sem update geral; o aluno só muda nome e grupo.
grant delete, insert, references, select, trigger, truncate on public.perfis to anon, authenticated;
grant update (grupo, nome) on public.perfis to authenticated;

-- Exceção: recados só para quem entrou, e sem update (o status muda só pelo admin, com a chave secreta).
grant delete, insert, select on public.recados to authenticated;
grant delete, insert, select on public.recados_uteis to authenticated;
