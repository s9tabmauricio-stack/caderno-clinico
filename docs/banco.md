# Banco de dados do Med Genius: detalhes

O manual (`AGENTS.md`) tem o resumo e o limite do conector. Aqui ficam as tabelas e as visões. Leia antes de mexer no banco ou numa consulta. A verdade é sempre o banco (`list_tables`, `list_migrations`).

- `materias` (id curto: `nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`; `cor_inicio`/`cor_fim`, `descricao`, `ordem`)
- `aulas` (id `<materia>-a<N>`, ex.: `uro-a2`; `titulo`, `resumo`, `apostila_html`, `publicada`, `ordem`)
- `questoes` (`materia_id`, `aula_id` opcional, `ordem`, `enunciado`, `alternativas` jsonb, `correta` = índice 0–4, `comentario`, `por_que_erradas`, `tema`, `prova` = de qual prova veio (filtro "Prova" do Banco), `fonte`, `origem`, `substituida_por`, `cai_na_prova` = o professor disse ou deu a entender que cai, põe a faixa PROVA; desde 03/11/2026)
- `flashcards` (id `<aula>-fNN`, `frente`, `verso`, `ordem`)
- Progresso: `respostas` (só a última resposta de cada questão), `historico_revisoes` (cada avaliação de flashcard, com `errou` e `intervalo_dias`; gravada por gatilho em `revisoes`: "Desfazer" tira a linha desfeita e apagar o card de `revisoes` apaga o histórico dele; desde 27/10/2026, antes disso só a última revisão de cada card), `historico_respostas` (todas as respostas dadas: um gatilho do banco grava uma linha a cada resposta nova ou refeita; só o gatilho grava e o aluno só lê e apaga o seu; "Refazer" não apaga, só "Apagar progresso"), `revisoes`; alunos: `perfis` (`nome`, `grupo` de prática 1–29; o aluno só pode alterar `nome` e `grupo`)
- Recados: `recados` (`questao_id`, `user_id`, `autor` = primeiro nome, preenchido por gatilho; `tipo` `insight`/`erro`; `status` `novo`/`visto`/`corrigido`) e `recados_uteis`. Aluno lê todos, cria e apaga os seus; status só muda pelo admin (chave secreta).
- Agenda: `agenda_semanas` (segunda-feira da semana; `texto` vazio = semana criada só para as provas) e `agenda_eventos` (aulas, cancelamentos, avisos, `grupos int[]`; `fixo` = incluído à parte, como as provas da P2, e a publicação da semana não apaga)
- Visões usadas pelas telas: `questoes_do_aluno`, `progresso_aulas`, `progresso_materias`, `progresso_temas`, `progresso_tentativas` (tentativas e acerto "na 1ª vez", mostrados no Desempenho), `flashcards_do_aluno`.
  Todas escondem aulas não publicadas e questões com `substituida_por` preenchido.
- RLS: alunos leem conteúdo e só gravam o próprio progresso. Escrita de conteúdo: só pelo conector (Claude ou Antigravity) ou pelas telas de admin (chave secreta).
- Classificação individual de questões: `classificacoes_questoes` (`user_id`, `questao_id`, `classificacao`: `rever` / `se_der_tempo` / `basico`, `atualizada_em`). Uma marca por aluno e questão; RLS limita leitura e escrita ao dono. Independente de respostas e histórico, sobrevive ao refazer. A visão `questoes_do_aluno.classificacao` traz a escolha do aluno.
- Suspensão individual: `flashcards_suspensos` (`user_id`, `flashcard_id`, `suspenso_em`), separada de `revisoes` para preservar histórico e agendamento. RLS restringe leitura e escrita ao próprio aluno. `flashcards_do_aluno.suspenso` permite excluir da fila; `progresso_aulas` mantém os totais históricos e acrescenta `cards_suspensos`, `cards_suspensos_estudados` e `cards_suspensos_vencidos`, descontados apenas nas pendências.
- **Cópia da estrutura:** `supabase/estrutura-atual.sql` (copiada do banco em 02/11/2026). Depois de qualquer migração, acrescente a mudança nela ou gere tudo de novo com as consultas de `supabase/gerar-estrutura.sql` (só leem o banco).
- A pasta `supabase/migrations/` guarda só a estrutura (as migrações que só incluíam conteúdo saíram em 02/11/2026) e não reflete tudo o que foi aplicado; a verdade é o banco (`list_migrations`).

## Pasta MEDGENIUS no Google Drive

Subpastas: `1 - ENTRADA (coloque os áudios aqui)` (id `13zTV8kYtmAWZyUJA9TOo5yC0tFfw3gk-`: o Mauricio só solta o áudio da aula; o Claude descobre a aula pela data e pela Agenda, faz o resto e tira o áudio daqui), `2 - Aulas` (id `1_ND6Ao_6W11oNyhQwAKEWxwuxi8FsiQi`: uma pasta por aula, `<aula-id> · <Título>`, com áudio original, transcrição, apostila PDF/HTML e rascunhos de flashcards e questões), `3 - Provas e fontes` (id `1Eff4u0H9F15JVkfMvUN_lLTnqzIFFHLD`: provas antigas, Revalida, slides e referências)
- A aula de Angiologia (pé diabético) tem o id `angio-a1`.
