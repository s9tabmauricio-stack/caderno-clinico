-- Último acesso da Central: a atividade mais recente, não só o último login.
-- (Antes, 'último acesso' vinha de auth.users.last_sign_in_at, que só muda no login.)
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
      select u.id, u.email, p.nome, p.grupo,
        -- último acesso = a atividade mais recente: login, sessão renovada, resposta ou revisão
        -- (last_sign_in_at só muda no login, e quem fica logado nunca aparece como ativo)
        greatest(u.last_sign_in_at,
          (select max(coalesce(s.updated_at, s.created_at)) from auth.sessions s where s.user_id = u.id),
          (select max(h.respondida_em) from historico_respostas h where h.user_id = u.id),
          (select max(h.revisada_em) from historico_revisoes h where h.user_id = u.id)) as ultimo_acesso,
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
