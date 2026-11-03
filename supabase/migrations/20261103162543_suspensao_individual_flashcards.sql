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

-- Colunas novas vão no fim, preservando os leitores e os totais históricos.
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

