-- Acrescenta o laranja sem alterar as classificações existentes.
alter table public.classificacoes_questoes
  drop constraint classificacoes_questoes_classificacao_check;
alter table public.classificacoes_questoes
  add constraint classificacoes_questoes_classificacao_check
  check (classificacao in ('rever', 'complicado', 'se_der_tempo', 'basico'));
