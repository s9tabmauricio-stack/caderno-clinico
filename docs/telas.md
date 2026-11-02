# Telas do Med Genius: detalhes

O manual (`AGENTS.md`) tem só os nomes das telas. Aqui fica como cada tela funciona. Leia antes de mexer numa tela.

## Telas

- **Tablet deitado** (tela de pelo menos 900 × 560 px): a barra de abas vira uma coluna de vidro à esquerda e as telas de estudo (Início, Estudar, Matéria, Banco, Aula, Desempenho) usam mais largura (`<Pagina larga>`). Início com a agenda na coluna da esquerda e cards, questões e matérias à direita; a questão fica como no celular (enunciado em cima, alternativas embaixo, na largura toda da coluna, alinhada com o resto da tela); as barras de abas (da matéria e da aula), a apostila e os flashcards também usam a largura toda da coluna; Desempenho em duas colunas. Em pé ou no celular nada muda. O CSS está no fim de `app/globals.css`.
- Início (proposta E do quadro https://claude.ai/artifact/BjQhu55DNueYG5a7zFWucg): saudação, cartões **Cards** e **Questões**, **Agenda de hoje**, **Próximas provas** (contagem regressiva em `components/ContagemProva.tsx`; "Todas →" abre `/agenda#provas`) e **Matérias** (a da última aula estudada tem "Continuar").
- **Revisão** (`/revisao`): fila do dia com todos os cards (lidos de 1000 em 1000 por `lerTudo` em `lib/dados.ts`, porque cada leitura do Supabase para em 1000). Os botões de matéria no topo (e a lista "Por matéria") abrem `/revisao?materia=<id>`, que revisa só os cards daquela matéria.
- **Estudar** (`/estudar`): uma carta por matéria (aulas, progresso) com o atalho do Banco de questões embaixo. `/questoes` só redireciona para cá.
- Barra de baixo: Início, Agenda, Matérias, Revisão, Desempenho. A tela "Configurações" (`/perfil`) fica na engrenagem do canto superior direito (todas as telas); a engrenagem sempre abre Configurações. Para o administrador, há atalhos próprios de Administração e Recados com contador no topo.
- Início: as aulas de hoje e as matérias abrem a matéria; "Refazer as erradas" abre o banco filtrado (erradas numa matéria só) ou o Desempenho. Desempenho: cada tema abre o banco já filtrado e cada matéria tem "Refazer as erradas".
- Banco de questões: os filtros ficam recolhidos no botão "Filtrar"; tema, prova e situação ficam na URL e lembrados no cookie `mgf_<matéria>`. O botão Voltar aceita `?retorno=` apenas para rotas internas de estudo e mantém compatibilidade com `?de=` (desempenho ou `aula:<id>`). No Desempenho, retorna à seção da matéria; nas aulas, preserva a aba e a origem da busca.
- Aula: abas Apostila / Questões / Flashcards. Matéria: abas **Aulas | Banco de questões | Flashcards** (as três telas mostram as mesmas abas, na largura toda, alinhadas com o que vem embaixo; no celular o número de cada aba fica embaixo do nome; o Banco tem filtros por tema e prova; Flashcards, `/materia/<id>/flashcards`, estuda os cards de todas as aulas da matéria e lista os cards por aula).
- Questões: antes de responder, cada alternativa tem a faixa "Cortar" (tesoura; Shift + letra), que vale só enquanto o aluno está na questão. Depois de responder, certa em verde, erradas em vermelho, a marcada em destaque; comentário embaixo da certa e o motivo embaixo de cada errada. No topo do cartão, o botão **Copiar** (todos os alunos) copia só o enunciado e as alternativas (A) …, B) …), sem gabarito nem comentário, para o aluno conferir na IA dele. Para o administrador, cada questão tem o botão **Editar** (no canto do cartão) que abre o mesmo editor de Conteúdo ali mesmo.
- **Conversa da turma** (embaixo da questão, só depois de responder): o aluno deixa "💡 Insight para os colegas" ou "⚠️ Erro na questão"; aparece como "Augusto deixou uma dica" / "Augusto achou um erro" (sem artigo, vale para qualquer nome). Colegas marcam dica como 👍 Útil; o autor apaga o próprio recado.
- Administração (atalho próprio no topo → Central, com menu persistente entre as seções): **Central** (`/admin/central`, desenho em https://claude.ai/artifact/4hnQkbH11HogQ5NMYGAhq6: avisos, uso da turma, alunos, conteúdo, questões mais erradas e espaço do banco; números da função `central_resumo()` do banco, só pela chave secreta; código em `lib/central.ts` e `components/admin/Central.tsx`), **Recados da turma** (`/admin/recados`: contador no atalho Recados com os novos; marcar visto/corrigido, abrir a questão, apagar), **Alunos** (`/admin`), **Conteúdo** (`/admin/conteudo`: resumo do que está no ar, editar/apagar aulas, questões, flashcards (na aula, "Apagar os N flashcards" apaga todos de uma vez, para refazer no padrão novo) e limpar versões antigas; `/admin/painel` só redireciona para cá), **Agenda da semana** (`/admin/agenda`: colar o cronograma do WhatsApp).

## Agenda (a tela)

- O Mauricio cola o cronograma do WhatsApp em `/admin/agenda`; `lib/agenda.ts` separa dias, horários, matéria (emoji ou palavra), professor, local, grupos, cancelamentos (❌) e avisos. Grupos por letra (A = práticas 1 a 7…) viram números.
- Teóricas valem para todos; práticas, só para os grupos listados. O aluno informa o grupo na própria Agenda (seletor ao lado dos filtros) ou em Configurações. Tocar numa aula abre a matéria dela.

## Encontrar conteúdo e voltar

- A tela Matérias não tem busca (retirada a pedido do Mauricio em 31/10/2026).
- Flashcards de aula/matéria permitem estudar livremente; Revisão reúne cards novos e pendentes para hoje. As telas explicam a diferença e oferecem atalhos entre elas.
