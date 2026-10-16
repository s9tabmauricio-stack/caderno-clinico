# Med Genius — Sugestões e Melhorias de Experiência do Usuário (UX)

Lista de melhorias planejadas para o app, focando na rotina de estudantes de medicina no celular (~390 px).
Conforme as melhorias forem implementadas, marque com `[x]`.

---

## 1. Flashcards e Repetição Espaçada (SRS)

- [x] **Botão "Desfazer" (Undo) na revisão:** Botão discreto no topo e atalho `Z` / `Ctrl+Z` para reverter avaliação acidental, restaurando o card virado na tela e preservando os intervalos originais no Supabase.
- [ ] **Animação 3D de virar o card (Flip):** Transição suave de giro ao tocar para ver a resposta, dando sensação tátil de cartão físico.
- [ ] **Gestos de arrastar no celular (Swipes):** Deslizar para cima (mostra resposta), para a esquerda (Errei) e para a direita (Bom/Fácil), facilitando o estudo com uma só mão.
- [ ] **Modo embaralhar os cards da aula:** Opção de estudar em ordem aleatória para evitar memorização por posição numérica.
- [ ] **Celebração ao concluir a fila do dia:** Microanimação sutil (confetes ou brilho do neurônio) ao zerar as revisões.

---

## 2. Banco de Questões

- [ ] **Barra de pesquisa por palavra-chave:** Busca por texto no banco de questões (ex.: "varfarina", "anúria", "GOLD") para consultas rápidas.
- [ ] **Modo Simulado vs. Modo Estudo:**
  - *Modo Estudo (atual):* Gabarito e comentários imediatos após cada questão.
  - *Modo Simulado:* Resolução de bloco fechado (ex.: 10 questões de prova) sem gabarito imediato e com cronômetro opcional, revelando o resultado completo só no final.
- [ ] **Marcar questão com estrela / bandeira (Favorito ⭐):** Salvar questões duvidosas para revisar depois com calma ou tirar dúvida em aula.
- [ ] **Toque longo para cortar alternativa:** No celular, segurar o dedo na alternativa para riscar sem precisar acertar o botão lateral da tesoura.

---

## 3. Leitura das Apostilas no Celular

- [ ] **Zoom nas imagens da apostila (Lightbox / Pinch-to-zoom):** Toque na página para abrir em tela cheia e dar zoom em tabelas de doses e fluxogramas.
- [ ] **Mini-índice flutuante de páginas:** Indicador no rodapé ("Pág. 4 de 19") permitindo saltar direto para uma página específica.
- [ ] **Modo slide horizontal opcional:** Alternativa ao scroll vertical longo, folheando as páginas para os lados como um leitor digital.

---

## 4. Agenda e Rotina da Semana

- [ ] **Destaque "Acontecendo Agora":** Brilho neon e contagem regressiva para a próxima aula quando o aluno abre o app no horário de aula.
- [ ] **Exportar para calendário (.ics):** Botão para adicionar a grade da semana ao Google Agenda ou Apple Calendar do celular com alertas.
- [ ] **Seletor de grupo visível na Agenda:** Atalho direto na aba de Agenda para escolher/alterar o grupo de prática sem precisar ir até Configurações.

---

## 5. Engajamento, Hábitos e Desempenho

- [ ] **Sequência de dias seguidos (Streak 🔥):** Contador no topo da tela inicial ("🔥 4 dias seguidos de estudo") para estimular a consistência.
- [ ] **Diagnóstico de pontos fracos no Desempenho:** Quadro destacando os temas com menor porcentagem de acerto com botão direto "Treinar este tema agora".
- [ ] **Previsão de revisões futuras:** Mini-calendário prevendo o volume de cards para amanhã e os próximos dias.

---

## 6. Sensação de App Nativo (Mobile & PWA)

- [ ] **Feedback tátil (vibração sutil):** Vibração suave (`navigator.vibrate`) no celular ao acertar questões, virar cards ou concluir a fila.
- [ ] **Esqueletos de carregamento (Skeleton screens):** Animação de carregamento pulsante no formato dos cartões para conexões lentas de 4G.

---

## 7. Conversa da Turma

- [ ] **Filtro de Dicas vs. Erros:** Separar na discussão o que é insight/mnemônico do que é aviso de erro na questão.
- [ ] **Aviso de correção:** Notificar ou destacar para o autor quando um erro reportado for corrigido pelo administrador.
