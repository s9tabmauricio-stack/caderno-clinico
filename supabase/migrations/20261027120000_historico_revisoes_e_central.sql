-- Histórico de revisões dos flashcards: cada vez que o aluno avalia um card fica guardada uma linha
-- (a tabela revisoes guarda só o estado atual de cada card). Um gatilho grava o histórico; o app não precisa mudar.
-- E a função que junta os números da Central (Configurações → Central), só para a chave secreta.
-- (aplicada pelo conector em 27/10/2026; cópia para referência)
create table public.historico_revisoes (
  id bigint generated always as identity primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  flashcard_id text not null references public.flashcards(id) on delete cascade,
  errou boolean not null,
  intervalo_dias real not null,
  revisada_em timestamptz not null default now()
);
create index historico_revisoes_aluno_idx on public.historico_revisoes (user_id, flashcard_id, revisada_em);
create index historico_revisoes_dia_idx on public.historico_revisoes (revisada_em);

alter table public.historico_revisoes enable row level security;
-- O aluno só lê o próprio histórico. Não há política de inserir, alterar nem apagar: só o gatilho mexe.
create policy "Ver o próprio histórico de revisões" on public.historico_revisoes
  for select using ((select auth.uid()) = user_id);

-- Revisão nova (ultima_revisao mais recente): grava uma linha.
-- "Desfazer" volta o card ao estado anterior (ultima_revisao mais antiga): tira a linha da revisão desfeita.
-- Card apagado de revisoes ("Desfazer" de um card novo ou "Apagar progresso"): o histórico dele vai junto.
-- Se algo falhar aqui, a revisão do aluno continua sendo salva normalmente.
create function public.registrar_historico_revisao() returns trigger
language plpgsql security definer set search_path = public as $$
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
$$;
revoke all on function public.registrar_historico_revisao() from public, anon, authenticated;

create trigger revisoes_historico
  after insert or update or delete on public.revisoes
  for each row execute function public.registrar_historico_revisao();

-- O que já foi revisado até hoje entra como a última revisão de cada card
insert into public.historico_revisoes (user_id, flashcard_id, errou, intervalo_dias, revisada_em)
select user_id, flashcard_id, intervalo_dias = 0 and lapsos > 0, intervalo_dias, ultima_revisao from public.revisoes;

-- Números da Central (um só pedido ao banco). Só a chave secreta (servidor) pode chamar.
create function public.central_resumo() returns jsonb
language sql stable security definer set search_path = public as $$
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
$$;
revoke all on function public.central_resumo() from public, anon, authenticated;
grant execute on function public.central_resumo() to service_role;
