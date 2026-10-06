-- Banco de questões da matéria: a questão pertence à matéria e, se couber
-- no assunto de uma aula, aparece também na aba Questões dessa aula.

alter table public.questoes add column materia_id text references public.materias (id) on delete cascade;
update public.questoes q set materia_id = a.materia_id from public.aulas a where a.id = q.aula_id;
alter table public.questoes alter column materia_id set not null;
alter table public.questoes alter column aula_id drop not null;

alter table public.questoes
  add column tema            text,   -- ex.: "Doença renal crônica"
  add column prova           text,   -- ex.: "p2-t19", para filtrar por prova
  add column fonte           text,   -- ex.: "P2 T19 · nº 1"
  add column origem          text,   -- "professor" (corrigida em sala), "unica", "inferido"
  add column por_que_erradas text;   -- por que cada alternativa errada está errada

create index questoes_materia_idx on public.questoes (materia_id, tema);

-- Visão das questões com a resposta do aluno logado
drop view public.questoes_do_aluno;
create view public.questoes_do_aluno with (security_invoker = true) as
select q.id, q.materia_id, q.aula_id, q.ordem, q.enunciado, q.alternativas, q.correta,
       q.comentario, q.por_que_erradas, q.tema, q.prova, q.fonte, q.origem,
       r.escolhida, r.correta as acertou, r.tentativas, r.respondida_em
from public.questoes q
left join public.aulas a on a.id = q.aula_id
left join public.respostas r on r.questao_id = q.id and r.user_id = (select auth.uid())
where q.aula_id is null or a.publicada;

-- Números do banco de questões por matéria
create view public.progresso_materias with (security_invoker = true) as
select m.id as materia_id,
  (select count(*)::int from public.questoes q where q.materia_id = m.id) as total_questoes,
  (select count(*)::int from public.respostas r join public.questoes q on q.id = r.questao_id
     where q.materia_id = m.id and r.user_id = (select auth.uid())) as respondidas,
  (select count(*)::int from public.respostas r join public.questoes q on q.id = r.questao_id
     where q.materia_id = m.id and r.user_id = (select auth.uid()) and r.correta) as acertos
from public.materias m;

-- Números por tema (para o desempenho e os filtros do banco)
create view public.progresso_temas with (security_invoker = true) as
select q.materia_id, coalesce(q.tema, 'Sem tema') as tema,
  count(*)::int as total_questoes,
  count(r.questao_id)::int as respondidas,
  count(*) filter (where r.correta)::int as acertos
from public.questoes q
left join public.respostas r on r.questao_id = q.id and r.user_id = (select auth.uid())
group by q.materia_id, coalesce(q.tema, 'Sem tema');

grant select on public.questoes_do_aluno, public.progresso_materias, public.progresso_temas to authenticated;
