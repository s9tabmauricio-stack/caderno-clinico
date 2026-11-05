-- Verificação real de RLS e persistência; tudo é desfeito ao terminar.
-- Rodar com: node scripts/sql.mjs supabase/tests/classificacao_questoes.sql
begin;
do $$
declare
  aluno uuid;
  colega uuid;
  questao text;
  historico bigint;
  linhas bigint;
begin
  select id into aluno from auth.users order by id limit 1;
  select id into colega from auth.users where id <> aluno order by id limit 1;
  select q.id into questao from public.questoes q
    left join public.aulas a on a.id = q.aula_id
    where q.substituida_por is null and (q.aula_id is null or a.publicada)
    and not exists (select 1 from public.classificacoes_questoes c where c.questao_id = q.id)
    limit 1;
  assert aluno is not null and colega is not null and questao is not null, 'Faltam dados para o teste';

  perform set_config('request.jwt.claim.sub', aluno::text, true);
  set local role authenticated;
  select count(*) into historico from public.historico_respostas;
  insert into public.classificacoes_questoes (questao_id, classificacao) values (questao, 'rever');
  assert (select classificacao = 'rever' from public.questoes_do_aluno where id = questao), 'A visão não trouxe a marcação';
  insert into public.classificacoes_questoes (questao_id, classificacao) values (questao, 'se_der_tempo')
    on conflict (user_id, questao_id) do update set classificacao = excluded.classificacao;
  assert (select classificacao = 'se_der_tempo' from public.questoes_do_aluno where id = questao), 'A troca não persistiu';
  update public.classificacoes_questoes set classificacao = 'basico' where questao_id = questao;
  assert (select classificacao = 'basico' from public.questoes_do_aluno where id = questao), 'A terceira opção falhou';
  begin
    update public.classificacoes_questoes set classificacao = 'invalida' where questao_id = questao;
    raise exception 'Aceitou classificação inválida';
  exception when check_violation then null;
  end;
  begin
    update public.classificacoes_questoes set user_id = colega where questao_id = questao;
    raise exception 'Permitiu transferir a marcação';
  exception when insufficient_privilege then null;
  end;
  assert (select count(*) = historico from public.historico_respostas), 'Alterou o histórico de respostas';

  perform set_config('request.jwt.claim.sub', colega::text, true);
  assert not exists (select 1 from public.classificacoes_questoes where questao_id = questao), 'Colega viu a marcação';
  assert (select classificacao is null from public.questoes_do_aluno where id = questao), 'A visão revelou a marcação do colega';
  update public.classificacoes_questoes set classificacao = 'rever' where questao_id = questao;
  get diagnostics linhas = row_count;
  assert linhas = 0, 'Colega alterou marcação alheia';
  delete from public.classificacoes_questoes where questao_id = questao;
  get diagnostics linhas = row_count;
  assert linhas = 0, 'Colega apagou marcação alheia';
  begin
    insert into public.classificacoes_questoes (user_id, questao_id, classificacao) values (aluno, questao, 'rever');
    raise exception 'Colega gravou em nome de outro aluno';
  exception when insufficient_privilege then null;
  end;
  insert into public.classificacoes_questoes (questao_id, classificacao) values (questao, 'rever');
  assert (select classificacao = 'rever' from public.questoes_do_aluno where id = questao), 'Colega não conseguiu marcar a própria questão';

  perform set_config('request.jwt.claim.sub', aluno::text, true);
  assert (select classificacao = 'basico' from public.questoes_do_aluno where id = questao), 'Uma marcação afetou a do outro aluno';
  delete from public.classificacoes_questoes where questao_id = questao;
  assert (select classificacao is null from public.questoes_do_aluno where id = questao), 'Não desmarcou';
  reset role;
  assert not has_table_privilege('anon', 'public.classificacoes_questoes', 'SELECT'), 'Anônimo pode ler a tabela';
end $$;
rollback;
select 'OK: três opções, troca, remoção, histórico preservado e isolamento entre alunos' as resultado;
