-- Provas da P2 na agenda. `fixo` marca o que foi incluído à parte: a publicação da semana em /admin/agenda não apaga.
alter table public.agenda_eventos add column if not exists fixo boolean not null default false;
comment on column public.agenda_eventos.fixo is 'Evento incluído à parte (ex.: provas da P2): a publicação da semana em /admin/agenda não apaga.';

-- Semanas só com as provas (sem texto do cronograma)
insert into public.agenda_semanas (semana) values ('2026-11-09'), ('2026-11-16'), ('2026-11-23') on conflict (semana) do nothing;

insert into public.agenda_eventos (semana, data, inicio, materia, tipo, titulo, fixo, ordem)
select date_trunc('week', d)::date, d, h::time, m, 'prova', t, true, 0
from (values
  ('2026-11-10'::date, '18:00', 'pneumo', 'P2 de Pneumologia'),
  ('2026-11-12'::date, '10:30', 'nefro',  'P2 de Nefrologia'),
  ('2026-11-13'::date, '20:40', 'orto',   'P2 de Ortopedia (prática)'),
  ('2026-11-16'::date, '17:50', 'pass',   'P2 de PASS'),
  ('2026-11-17'::date, '18:30', 'gastro', 'P2 de Gastroenterologia'),
  ('2026-11-19'::date, '14:00', 'orto',   'P2 de Ortopedia (teórica)'),
  ('2026-11-23'::date, '13:45', 'uro',    'P2 de Urologia'),
  ('2026-11-25'::date, '07:30', 'angio',  'P2 de Angiologia')
) as p(d, h, m, t)
where not exists (select 1 from public.agenda_eventos e where e.fixo and e.data = p.d and e.titulo = p.t);
