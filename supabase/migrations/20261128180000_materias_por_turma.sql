-- Cada turma com as suas matérias (28/11/2026, regra do Mauricio: "cada um no seu quadrado").
-- A mesma disciplina em duas turmas vira duas matérias, com aulas, questões e cards próprios.
-- materias.chave_agenda: como o cronograma chama a matéria ('neuro'); vazio = o próprio id.
-- O app leva cada aula da agenda para a matéria da turma daquela agenda.

alter table public.materias add column chave_agenda text;

-- Neurologia da T29 (6º período), separada da Neurologia da T28 (id neuro): aulas neuro29-a1, neuro29-a2…
insert into public.materias (id, nome, descricao, ordem, cor_inicio, cor_fim, turmas, periodo, chave_agenda)
select 'neuro29', 'Neurologia', null, 9, cor_inicio, cor_fim, '{t29}', 6, 'neuro' from public.materias where id = 'neuro';
