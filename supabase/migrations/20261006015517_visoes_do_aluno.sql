-- Visões que juntam o conteúdo com o progresso de quem está logado.
-- security_invoker: a visão respeita as regras de segurança de cada aluno.

create view public.questoes_do_aluno with (security_invoker = true) as
select q.id, q.aula_id, q.ordem, q.enunciado, q.alternativas, q.correta, q.comentario,
       r.escolhida, r.correta as acertou, r.tentativas, r.respondida_em
from public.questoes q
join public.aulas a on a.id = q.aula_id and a.publicada
left join public.respostas r on r.questao_id = q.id and r.user_id = (select auth.uid());

create view public.flashcards_do_aluno with (security_invoker = true) as
select f.id, f.aula_id, f.ordem, f.frente, f.verso,
       a.titulo as aula_titulo, a.ordem as aula_ordem,
       m.id as materia_id, m.nome as materia_nome, m.ordem as materia_ordem,
       v.repeticoes, v.intervalo_dias, v.facilidade, v.lapsos, v.proxima_revisao, v.ultima_revisao
from public.flashcards f
join public.aulas a on a.id = f.aula_id and a.publicada
join public.materias m on m.id = a.materia_id
left join public.revisoes v on v.flashcard_id = f.id and v.user_id = (select auth.uid());

-- Uma linha por aula com os números do aluno (para barras de progresso e badges)
create view public.progresso_aulas with (security_invoker = true) as
select a.id as aula_id, a.materia_id, a.ordem, a.titulo,
  (select count(*)::int from public.questoes q where q.aula_id = a.id) as total_questoes,
  (select count(*)::int from public.respostas r join public.questoes q on q.id = r.questao_id
     where q.aula_id = a.id and r.user_id = (select auth.uid())) as respondidas,
  (select count(*)::int from public.respostas r join public.questoes q on q.id = r.questao_id
     where q.aula_id = a.id and r.user_id = (select auth.uid()) and r.correta) as acertos,
  (select count(*)::int from public.flashcards f where f.aula_id = a.id) as total_cards,
  (select count(*)::int from public.revisoes v join public.flashcards f on f.id = v.flashcard_id
     where f.aula_id = a.id and v.user_id = (select auth.uid())) as cards_estudados,
  (select count(*)::int from public.revisoes v join public.flashcards f on f.id = v.flashcard_id
     where f.aula_id = a.id and v.user_id = (select auth.uid()) and v.proxima_revisao <= now()) as cards_vencidos,
  greatest(
    (select max(r.respondida_em) from public.respostas r join public.questoes q on q.id = r.questao_id
       where q.aula_id = a.id and r.user_id = (select auth.uid())),
    (select max(v.ultima_revisao) from public.revisoes v join public.flashcards f on f.id = v.flashcard_id
       where f.aula_id = a.id and v.user_id = (select auth.uid()))
  ) as ultima_atividade
from public.aulas a
where a.publicada;

grant select on public.questoes_do_aluno, public.flashcards_do_aluno, public.progresso_aulas to authenticated;
