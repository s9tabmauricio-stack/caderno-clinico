-- Limite de aparelhos (sessões abertas) por conta. Quem entra num aparelho novo derruba o usado há mais tempo.
-- Aplicada pelo conector em 12/11/2026.
alter table public.perfis add column max_aparelhos smallint default 1
  constraint perfis_max_aparelhos_check check (max_aparelhos is null or max_aparelhos between 1 and 10);
comment on column public.perfis.max_aparelhos is 'Quantos aparelhos a conta pode ter abertos ao mesmo tempo; vazio = sem limite. Contas novas: 1.';

-- Contas de antes de 12/11/2026 ficam com 2; o administrador, sem limite.
update public.perfis set max_aparelhos = 2;
update public.perfis set max_aparelhos = null
  where id in (select id from auth.users where email like '08699426623@%');

-- Fecha as sessões que passam do limite, mantendo as usadas mais recentemente (e a que acabou de abrir).
create or replace function public.podar_aparelhos(p_user uuid, p_manter uuid default null)
returns integer
language plpgsql
security definer
set search_path to ''
as $$
declare
  lim smallint;
  removidas integer;
begin
  select p.max_aparelhos into lim from public.perfis p where p.id = p_user;
  if not found or lim is null then
    return 0;
  end if;
  with fora as (
    select s.id from auth.sessions s
    where s.user_id = p_user
    order by (s.id = p_manter) desc nulls last, greatest(s.created_at, coalesce(s.updated_at, s.created_at)) desc, s.id
    offset lim
  )
  delete from auth.sessions s using fora where s.id = fora.id;
  get diagnostics removidas = row_count;
  return removidas;
end;
$$;
revoke execute on function public.podar_aparelhos(uuid, uuid) from public, anon, authenticated;
grant execute on function public.podar_aparelhos(uuid, uuid) to service_role;

-- Gatilho em auth.sessions: a cada login, aplica o limite. Nunca deixa um erro aqui impedir a entrada.
create or replace function public.limitar_aparelhos()
returns trigger
language plpgsql
security definer
set search_path to ''
as $$
begin
  begin
    perform public.podar_aparelhos(new.user_id, new.id);
  exception when others then
    raise warning 'limitar_aparelhos: %', sqlerrm;
  end;
  return null;
end;
$$;
revoke execute on function public.limitar_aparelhos() from public, anon, authenticated;

create trigger limitar_aparelhos after insert on auth.sessions
  for each row execute function public.limitar_aparelhos();

-- O app pergunta de tempos em tempos se a sessão deste aparelho ainda existe (foi derrubada por outro login?).
create or replace function public.sessao_ativa()
returns boolean
language sql
stable
security definer
set search_path to ''
as $$
  select case
    when nullif(auth.jwt() ->> 'session_id', '') is null then true
    else exists (
      select 1 from auth.sessions s
      where s.id = (auth.jwt() ->> 'session_id')::uuid and s.user_id = auth.uid()
    )
  end;
$$;
revoke execute on function public.sessao_ativa() from public, anon;
grant execute on function public.sessao_ativa() to authenticated;
