-- Histórico de tentativas das questões: cada resposta dada fica guardada, mesmo que o aluno refaça a questão
-- (a tabela respostas guarda só a última). Um gatilho grava o histórico; o app não precisa mudar para gravar.
-- (aplicada pelo conector em 18/10/2026; cópia para referência)
create table public.historico_respostas (
  id bigint generated always as identity primary key,
  user_id uuid not null default auth.uid() references auth.users(id) on delete cascade,
  questao_id text not null references public.questoes(id) on delete cascade,
  escolhida smallint not null,
  correta boolean not null,
  respondida_em timestamptz not null default now()
);
create index historico_respostas_aluno_idx on public.historico_respostas (user_id, questao_id, respondida_em);

alter table public.historico_respostas enable row level security;
-- O aluno vê e pode apagar o próprio histórico (Configurações → Apagar progresso). Não há política de
-- inserir nem de alterar: só o gatilho grava, então o histórico não pode ser forjado nem editado.
create policy "Ver o próprio histórico" on public.historico_respostas
  for select using ((select auth.uid()) = user_id);
create policy "Apagar o próprio histórico" on public.historico_respostas
  for delete using ((select auth.uid()) = user_id);

-- Grava uma linha no histórico a cada resposta nova ou refeita. Se algo falhar aqui, a resposta do aluno
-- continua sendo salva normalmente (o histórico nunca atrapalha responder).
create function public.registrar_historico_resposta() returns trigger
language plpgsql security definer set search_path = public as $$
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
$$;
revoke all on function public.registrar_historico_resposta() from public, anon, authenticated;

create trigger respostas_historico
  after insert or update on public.respostas
  for each row execute function public.registrar_historico_resposta();

-- O que já foi respondido até hoje entra como a primeira tentativa de cada questão
insert into public.historico_respostas (user_id, questao_id, escolhida, correta, respondida_em)
select user_id, questao_id, escolhida, correta, coalesce(respondida_em, now()) from public.respostas;

-- Por matéria, para o aluno logado: tentativas no total e acerto só na primeira vez que respondeu cada questão
-- (mesmas regras das outras visões: sem aulas não publicadas nem versões antigas de questões)
create view public.progresso_tentativas with (security_invoker = true) as
select q.materia_id,
       count(*)::integer as tentativas,
       (count(*) filter (where h.n = 1))::integer as primeiras,
       (count(*) filter (where h.n = 1 and h.correta))::integer as acertos_primeira
from (
  select x.*, row_number() over (partition by x.questao_id order by x.respondida_em, x.id) as n
  from public.historico_respostas x
  where x.user_id = (select auth.uid())
) h
join public.questoes q on q.id = h.questao_id
left join public.aulas a on a.id = q.aula_id
where q.substituida_por is null and (q.aula_id is null or a.publicada)
group by q.materia_id;
