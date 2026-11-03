-- Marca própria para "o professor disse ou deu a entender que cai na prova".
-- Antes, essa marca estava no campo prova ('PROVA'), que serve para dizer de qual prova a questão veio.
-- Aplicada em 03/11/2026 em dois passos: (1) campo novo, cópia das marcas e visão; (2) depois do site novo
-- no ar, o campo prova dessas questões volta a ficar vazio (todas eram montadas da aula, sem prova de origem).

alter table public.questoes add column cai_na_prova boolean not null default false;
comment on column public.questoes.cai_na_prova is 'O professor disse ou deu a entender que o ponto cobrado cai na prova (selo PROVA da apostila ou ênfase em aula). Independe de prova (de qual prova a questão veio).';
update public.questoes set cai_na_prova = true where prova = 'PROVA';

create or replace view public.questoes_do_aluno with (security_invoker=true) as
 SELECT q.id, q.aula_id, q.ordem, q.enunciado, q.alternativas, q.correta, q.comentario,
    r.escolhida, r.correta AS acertou, r.tentativas, r.respondida_em,
    q.materia_id, q.por_que_erradas, q.tema, q.prova, q.fonte, q.origem, q.cai_na_prova
   FROM ((questoes q
     LEFT JOIN aulas a ON ((a.id = q.aula_id)))
     LEFT JOIN respostas r ON (((r.questao_id = q.id) AND (r.user_id = ( SELECT auth.uid() AS uid)))))
  WHERE (((q.aula_id IS NULL) OR a.publicada) AND (q.substituida_por IS NULL));

-- Passo 2 (depois do site novo no ar):
update public.questoes set prova = null where prova = 'PROVA' and fonte = 'Montada (aula 2026)';
