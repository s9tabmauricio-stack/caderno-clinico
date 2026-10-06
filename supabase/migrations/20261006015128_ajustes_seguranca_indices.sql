-- A função só deve rodar pelo gatilho de cadastro, nunca chamada pela API
revoke execute on function public.criar_perfil() from public, anon, authenticated;

-- Índices para as chaves estrangeiras do progresso
create index respostas_questao_idx on public.respostas (questao_id);
create index revisoes_flashcard_idx on public.revisoes (flashcard_id);
