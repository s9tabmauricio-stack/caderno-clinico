-- Calendário acadêmico da FAG (vale para todas as turmas). Dados de cada ano em supabase/calendario/<ano>.sql.
create table public.calendario (
  id bigint generated always as identity primary key,
  inicio date not null,
  fim date,
  tipo text not null check (tipo in ('feriado','recesso','provas','segunda_chamada','exames','semana_livre','letivo','evento','notas','docentes')),
  titulo text not null check (char_length(btrim(titulo)) between 1 and 160),
  check (fim is null or fim >= inicio)
);
comment on table public.calendario is 'Calendário acadêmico da FAG (vale para todas as turmas); fim vazio = um dia só';
create index calendario_inicio_idx on public.calendario (inicio);
alter table public.calendario enable row level security;
create policy "Turma lê o calendário" on public.calendario as permissive for select to authenticated using (true);
revoke all on public.calendario from anon, authenticated;
grant select on public.calendario to authenticated;
