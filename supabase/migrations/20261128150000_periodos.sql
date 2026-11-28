-- Períodos (28/11/2026): cada matéria é de um período do curso, e cada turma tem um período atual.
-- A aba Matérias abre no período atual da turma; os anteriores ficam num seletor acima da barra de matérias.
-- T29: 5º período (o que já existia) → atual 6º. T28: 6º (Neurologia) → atual 7º.

create table public.turmas (
  id text not null,
  nome text not null,
  periodo_atual smallint not null,
  constraint turmas_pkey PRIMARY KEY (id),
  constraint turmas_periodo_atual_check CHECK (((periodo_atual >= 1) AND (periodo_atual <= 12)))
);
insert into public.turmas (id, nome, periodo_atual) values ('t28', 'T28', 7), ('t29', 'T29', 6);
alter table public.turmas enable row level security;
create policy "Alunos leem as turmas" on public.turmas as permissive for select to authenticated using (true);
revoke all on public.turmas from anon, authenticated;
grant select on public.turmas to authenticated;
grant all on public.turmas to service_role;

-- Vazio = período atual de quem vê (sempre preencha numa matéria nova).
alter table public.materias add column periodo smallint;
alter table public.materias add constraint materias_periodo_check CHECK (((periodo IS NULL) OR ((periodo >= 1) AND (periodo <= 12))));
update public.materias set periodo = 5 where 't29' = any(turmas);
update public.materias set periodo = 6 where id = 'neuro';

-- perfis.turma passa a apontar para a tabela de turmas.
alter table public.perfis drop constraint perfis_turma_check;
alter table public.perfis add constraint perfis_turma_fkey FOREIGN KEY (turma) REFERENCES public.turmas(id);
