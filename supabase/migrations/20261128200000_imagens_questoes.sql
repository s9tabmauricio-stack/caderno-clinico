-- Imagens nas questões (28/11/2026): só as que têm (ECG, raio X, foto de lesão…); a maioria fica vazia.
-- questoes.imagens = caminhos no espaço público "questoes" do Storage (ex.: 'neuro29-a1/neuro29-a1-q05-1.webp'), na ordem.
-- Quem grava é o scripts/imagem-questao.mjs ou o gravar-rascunho.mjs (linha **Imagem:**), com a chave secreta.

alter table public.questoes add column imagens text[] not null default '{}'::text[];

create or replace view public.questoes_do_aluno with (security_invoker=true) as
 select q.id, q.aula_id, q.ordem, q.enunciado, q.alternativas, q.correta, q.comentario,
    r.escolhida, r.correta as acertou, r.tentativas, r.respondida_em,
    q.materia_id, q.por_que_erradas, q.tema, q.prova, q.fonte, q.origem, q.cai_na_prova,
    c.classificacao, q.professor_disse_que_cai, q.imagens
 from public.questoes q
 left join public.aulas a on a.id = q.aula_id
 left join public.respostas r on r.questao_id = q.id and r.user_id = (select auth.uid())
 left join public.classificacoes_questoes c on c.questao_id = q.id and c.user_id = (select auth.uid())
 where (q.aula_id is null or a.publicada) and q.substituida_por is null;

-- Espaço público (o link da imagem abre sem login, como as imagens das apostilas em public/); só a chave secreta grava.
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('questoes', 'questoes', true, 5242880, array['image/webp', 'image/png', 'image/jpeg'])
on conflict (id) do nothing;
