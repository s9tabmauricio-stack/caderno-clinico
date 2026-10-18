# Med Genius — Auditoria de UX (organização e navegação)

> Análise feita só pela leitura do código (ramo `main` em 18/10/2026) e de uma contagem no banco. Nenhum arquivo do app foi alterado.
> Não abri o app num tablet de verdade: o que depende de ver a tela (cores reais, como o teclado do tablet se comporta, rolagem) está marcado como **não verificado**.

**Premissas** (os campos do pedido vieram em branco, então completei com o que o `CLAUDE.md` descreve; corrija se estiver errado):
- **Usuário típico:** estudante de Medicina da turma da FAG, estudando no tablet entre as aulas e em casa, em sessões longas.
- **As 3 tarefas principais:** (1) fazer questões de prova de uma matéria; (2) revisar os flashcards do dia; (3) ler a apostila da aula (ligada à aula do dia na agenda).

**Números do banco hoje:** 6 matérias, 15 aulas publicadas, 97 questões (26 sem aula, só no banco), 11 temas (até 8 numa só matéria), 234 flashcards, 5 alunos (só 2 informaram o grupo de prática), 73 eventos de agenda.

---

## 1. Resumo executivo

1. O app é enxuto e coerente: poucas telas, mesma "moldura" em todas (`components/Pagina.tsx`), barra de baixo fixa, mensagens de erro em português claro. A base é boa.
2. O maior problema de organização é que **o conteúdo de estudo (Matérias → Aulas → Apostila) não tem lugar na barra de baixo**: só se chega pelo fim da tela Início, abaixo da revisão e da agenda.
3. Há **três caminhos diferentes para o mesmo banco de questões** e o botão "Voltar" não devolve o aluno para onde ele veio (entra pela aba Questões e volta para a tela da matéria, que acende a aba Início).
4. As telas de **acompanhamento são becos sem saída**: Desempenho mostra o tema fraco mas não deixa treiná-lo; "Por matéria" na Revisão não é clicável; a agenda não leva à apostila da aula.
5. A **Revisão de hoje mostra todos os flashcards novos de uma vez** (um aluno novo vê "234 flashcards"), o que tira o sentido do número e do selo vermelho da aba.
6. **Não existe tela de carregamento** em nenhuma rota: no tablet com internet fraca, tocar numa aba parece não fazer nada por 1–3 s.
7. Para tablet, o layout é de celular esticado: coluna de no máximo 720 px, filtros e botões pequenos (≈30–36 px de altura) e a barra de baixo ocupando espaço durante as sessões longas.
8. A proposta troca a aba "Questões" por **"Estudar"** (matérias, aulas e banco num só lugar), transforma Início em **"Hoje"**, liga Desempenho e Agenda ao conteúdo e junta as duas telas de administração de conteúdo que se repetem.
9. Várias correções são de alto impacto e baixo esforço (telas de carregamento, links nas linhas que hoje são mortas, limite de novos por dia, botão "Voltar" certo).

---

## 2. Mapa atual do app

Toques contados **a partir da tela Início** (onde o app abre). "Aba" = barra de baixo; "⚙" = engrenagem no canto superior direito.

```
/login  (CPF + senha; sem barra de baixo)
│
├─ [Aba] Início  /                                        0 toques
│   ├─ Revisão de hoje → "Começar revisão" → /revisao      1 (+1 para começar a sessão)
│   ├─ Suas aulas hoje (só leitura) → "Semana →" /agenda   1
│   ├─ "Informe seu grupo…" → /perfil                      1  (só se não tem grupo)
│   ├─ Continuar → /aula/[id] (última aula mexida)         1
│   ├─ Matérias (blocos) → /materia/[id]                   1
│   │    ├─ Banco de questões → /materia/[id]/questoes     2
│   │    └─ Aulas → /aula/[id]                             2
│   │         ├─ aba Apostila (padrão)                     2
│   │         │    └─ "Fazer as N questões" / "Estudar os flashcards" (troca de aba)
│   │         ├─ aba Questões                              3
│   │         │    └─ "Ver as N questões do banco da matéria" → /materia/[id]/questoes
│   │         └─ aba Flashcards → "Estudar N cards"        3 (+1)
│   └─ Seu progresso (3 números, não clicáveis)
│
├─ [Aba] Agenda  /agenda                                   1
│   ├─ Dias da semana (Seg…Sex) + filtro Meu grupo / Todas
│   ├─ Lista de aulas do dia (não clicável)
│   └─ "Informe seu grupo…" → /perfil                      2
│
├─ [Aba] Questões  /questoes                               1
│   └─ Lista de matérias → /materia/[id]/questoes          2
│        ├─ números (Respondidas / Acerto / Para rever)
│        ├─ filtros: Mostrar · Tema · Prova
│        └─ questão → Conversa da turma (depois de responder)
│             └─ (admin) "Editar" abre o editor ali mesmo
│        "← Matéria" leva para /materia/[id] (não volta para /questoes)
│
├─ [Aba] Revisão  /revisao  (selo com o nº pendente)       1
│   ├─ "Revisar N cards" → sessão                          2
│   └─ Por matéria (linhas não clicáveis)
│
├─ [Aba] Desempenho  /desempenho                           1
│   └─ por matéria → por tema (nada é clicável)
│
└─ [⚙] Configurações  /perfil   (nenhuma aba fica acesa)   1
    ├─ Nome e grupo → "Editar" → Salvar                    2–3
    ├─ Segurança (trocar senha) → "Editar"                 2–3
    ├─ Apagar progresso → "Escolher" → selects → Apagar → confirmar   4–6
    ├─ Administração (só admin)
    │   ├─ Recados da turma  /admin/recados                2
    │   │    └─ "Abrir questão" → /admin/conteudo/questoes/[materia]?q=…   3
    │   ├─ Painel do conteúdo  /admin/painel               2
    │   │    └─ aula → /admin/conteudo/aula/[id]           3
    │   ├─ Alunos  /admin                                  2
    │   ├─ Conteúdo  /admin/conteudo                       2
    │   │    ├─ Banco de questões → /admin/conteudo/questoes/[materia]  3
    │   │    └─ aula → /admin/conteudo/aula/[id]           3
    │   │         └─ "Editar as N →" questões da aula      4
    │   └─ Agenda da semana  /admin/agenda                 2
    ├─ Instalar no celular (instruções)
    └─ Sair

Telas avulsas: /auth/erro ("link inválido"), app/error.tsx, app/not-found.tsx
```

**Observação:** o `CLAUDE.md` diz que a barra de baixo tem 4 itens (Início, Agenda, Revisão, Desempenho) e que a engrenagem leva ao "Perfil". O código tem **5 itens** (inclui Questões, `components/TabBar.tsx:7-13`) e a tela se chama **"Configurações"** (`app/perfil/page.tsx:24`). Também há uma tela de admin a mais que o manual não cita (`/admin/painel`).

### Toques das tarefas principais hoje

| Tarefa | Caminho mais curto hoje | Toques até começar |
|---|---|---|
| 1. Fazer questões de uma matéria | Aba Questões → matéria | **2** |
| 1b. Refazer só as que errei | Aba Questões → matéria → "Só as que errei" | **3** |
| 1c. Treinar o tema em que vou pior | Desempenho (ver o tema) → Aba Questões → matéria → rolar até "Tema" → tema | **4** + rolagem |
| 2. Revisar os flashcards do dia | "Começar revisão" (Início) → "Revisar N cards" | **2** |
| 3. Ler a apostila da aula de hoje | Início → bloco da matéria (rolar até "Matérias") → aula | **2** + rolagem (1 se for a do "Continuar") |
| 4. Informar o grupo de prática | ⚙ → Editar → digitar → Salvar → voltar à Agenda | **4** |

---

## 3. Problemas encontrados

Legenda: **Impacto** no usuário / **Esforço** para corrigir (alto, médio, baixo).

### A. Organização e navegação

| # | Onde | Problema | Impacto | Esforço |
|---|---|---|---|---|
| A1 | `components/TabBar.tsx`, `app/page.tsx:143-176` | **Matérias e apostilas não têm aba.** O coração do app (ler a apostila da aula) só aparece no fim da tela Início, depois de Revisão, Agenda e Continuar. No tablet em pé, os blocos de matéria ficam abaixo da dobra. | Alto | Médio |
| A2 | `/questoes`, `/materia/[id]` (bloco "Banco de questões"), `components/AulaAbas.tsx:93-97` | **Três portas para o mesmo banco de questões**, com nomes diferentes ("Questões", "Banco de questões", "Ver as N questões do banco da matéria"). A aba Questões é só uma lista de matérias que repete a lista do Início. | Médio | Médio |
| A3 | `app/materia/[id]/questoes/page.tsx:34`, `components/TabBar.tsx:17-26` | **"Voltar" não volta.** Quem entra pela aba Questões e toca "← Nefrologia" cai na tela da matéria, e a aba acesa muda de Questões para Início. O aluno perde a referência de onde está. | Médio | Baixo |
| A4 | `app/desempenho/page.tsx:96-105` | **Desempenho é beco sem saída.** Mostra "2 de 6 certas" no tema, mas o tema não é clicável. Para treinar, o aluno precisa sair, ir a Questões, achar a matéria e o filtro de tema (4 toques + rolagem). | Alto | Baixo |
| A5 | `app/revisao/page.tsx:52-68` | **"Por matéria" na Revisão não é clicável** (linhas `row static`). Não dá para revisar só Nefro na véspera da prova de Nefro. | Médio | Médio |
| A6 | `components/AgendaLista.tsx:26` | **A agenda não leva ao conteúdo.** "Suas aulas hoje" mostra "Nefro · Prof. X" mas não abre a apostila daquela aula. *Não dá para concluir pelo código se cada evento da agenda corresponde a uma aula do app:* `agenda_eventos` guarda a matéria, mas não o id da aula. Ligar à **matéria** é possível já. | Médio | Baixo (matéria) / Alto (aula exata) |
| A7 | `app/page.tsx:178-202` × `app/desempenho/page.tsx:39-57` | **Duplicação:** "Seu progresso" no Início repete exatamente os 3 números do topo de Desempenho (Questões, Acerto, Cards), sem link. Ocupa o fim do Início sem levar a lugar nenhum. | Baixo | Baixo |
| A8 | `app/perfil/page.tsx:47-76` | **Administração com duas telas que se sobrepõem:** "Painel do conteúdo" e "Conteúdo" listam as mesmas aulas por matéria e abrem o mesmo editor (`/admin/conteudo/aula/[id]`). O admin precisa lembrar qual usar. | Médio (só admin) | Baixo |
| A9 | `app/perfil/page.tsx` e `/admin/*` | **Tudo de admin mora dentro de "Configurações" do aluno**, misturado com nome, senha e "Apagar progresso". Quando há recados novos, a bolinha rosa fica na engrenagem, mas o caminho é ⚙ → rolar → Recados. | Baixo | Baixo |
| A10 | `app/agenda/page.tsx:44-48`, `components/AgendaSemana.tsx:70-72` | **Grupo de prática longe de onde é usado.** O filtro "Meu grupo" aparece desativado e manda para Configurações (4 toques e sem volta automática para a Agenda). Só 2 de 5 alunos informaram o grupo. (Já está no `MELHORIAS-UX.md`, seção 4.) | Médio | Baixo |
| A11 | Nomes | **Nomes inconsistentes:** "Perfil" (manual) × "Configurações" (tela e botões Voltar); "Revisão" (aba) × "Flashcards" (aba da aula e eyebrow da tela); "Questões" (aba) × "Banco de questões" (tela). | Baixo | Baixo |
| A12 | Telas `/admin/*` (`pendentes={0}`) | O selo vermelho da aba Revisão **some** nas telas de administração e volta nas outras. Parece que a revisão foi feita. | Baixo | Baixo |

### B. Becos sem saída e próximos passos

| # | Onde | Problema | Impacto | Esforço |
|---|---|---|---|---|
| B1 | `components/Questoes.tsx:169-216` (Resultado) | No fim das questões da aula só há "Refazer". **Não há "Estudar os flashcards desta aula"** nem "Próxima aula", ao contrário da apostila, que tem esses botões (`AulaAbas.tsx:72-83`). | Médio | Baixo |
| B2 | `components/Flashcards.tsx:226-249` | Ao terminar a revisão do dia, "Concluir" só recarrega a mesma tela. Ao terminar os cards da aula, não há caminho para as questões. | Baixo | Baixo |
| B3 | `app/error.tsx` | A tela de erro **não tem barra de baixo nem "Voltar ao início"**, só "Tentar de novo". Sem internet, o aluno fica preso (no app instalado não há botão Voltar do navegador). | Médio | Baixo |
| B4 | `app/auth/erro/page.tsx` | Texto fala de "link por e-mail" e botão "Pedir um link novo", mas o login é por CPF e senha. Sobra de um login antigo; confunde se aparecer. | Baixo | Baixo |

### C. Revisão de flashcards (lógica que afeta a organização da tela Início)

| # | Onde | Problema | Impacto | Esforço |
|---|---|---|---|---|
| C1 | `lib/dados.ts:217-221`, `app/revisao/page.tsx:13-30` | **"Revisão de hoje" soma todos os cards novos de todas as aulas, sem limite.** Um aluno que acabou de entrar vê **234 flashcards** no Início e no selo da aba, incluindo aulas que ele ainda nem teve. O número deixa de dizer "o que fazer hoje" e vira culpa. | Alto | Baixo (limite de novos/dia) a Médio (só aulas já dadas) |

### D. Tablet, toque e sessões longas

| # | Onde | Problema | Impacto | Esforço |
|---|---|---|---|---|
| D1 | todas as rotas (não existe nenhum `loading.tsx`) | **Sem tela de carregamento.** Todas as telas buscam vários dados no servidor antes de aparecer; ao tocar numa aba nada muda até a nova tela chegar. Com 4G fraco, o aluno toca de novo ou acha que travou. | Alto | Baixo |
| D2 | `app/globals.css:14` (`.wrap{max-width:720px}`) | **Layout de celular no tablet.** Tudo numa coluna de 720 px; no tablet deitado (≈1180 px) sobra uma faixa vazia de cada lado. Questão + explicação + Conversa da turma ficam empilhadas e exigem muita rolagem. | Médio | Médio |
| D3 | `app/globals.css:420` (`.pill`), `:156` (`.qd` 30×30), `:103` (`.segm` ≈38 px), `.btn.sm` ≈36 px, `.back` ≈36 px | **Alvos de toque abaixo de 44 px** (estimado pelo CSS): filtros de tema/prova, quadradinhos das questões, abas Apostila/Questões/Flashcards, "Encerrar"/"Desfazer" na sessão de cards. | Médio | Baixo |
| D4 | `app/globals.css:641` (`.elim`) | O rótulo "Cortar" da tesoura tem **9,5 px**, ilegível no tablet a um braço de distância. | Baixo | Baixo |
| D5 | `components/BancoQuestoes.tsx:70-123` | **Tela do banco sobrecarregada antes da 1ª questão:** 3 números + até 3 linhas de filtros (Nefro tem até 8 temas) + contador. Em pé, a questão começa no meio da tela. Os filtros também se perdem ao sair e voltar (ficam só na memória). | Médio | Baixo/Médio |
| D6 | `components/TabBar.tsx`, `components/Flashcards.tsx`, `components/Questoes.tsx` | **Sessões longas sem "modo foco":** a barra de baixo e a engrenagem continuam na tela durante a sessão de cards e as questões, convidando a sair. Sair de uma sessão de cards perde a fila e o "Desfazer" (cada nota já foi salva, mas a sessão some sem aviso). | Médio | Médio |
| D7 | `components/Flashcards.tsx:323`, `Questoes.tsx:122` | Os atalhos de teclado são ótimos, mas a dica some em telas de toque (`@media (hover:none)`). **No tablet com teclado o aluno nunca descobre os atalhos.** *Não verificado:* como cada tablet informa `hover`. | Baixo | Baixo |

### E. Feedback, estados e acessibilidade

| # | Onde | Problema | Impacto | Esforço |
|---|---|---|---|---|
| E1 | `components/Questoes.tsx:91-98` | "Refazer as erradas" e "Refazer todas" **apagam as respostas antigas**, então o acerto em Desempenho passa a mostrar só a última tentativa e não avisa isso. | Médio | Médio |
| E2 | `components/Questoes.tsx:239-251` | O botão "Editar" do admin fica na mesma linha das etiquetas da questão; em tela estreita pode quebrar linha. *Não verificado visualmente.* | Baixo | Baixo |
| E3 | Contraste | Texto secundário `#97A0B8` sobre fundo `#05060E` dá cerca de 7,6:1 (bom). **Não dá para concluir pelo código** o contraste do texto branco sobre os blocos coloridos de cada matéria (cores vêm do banco). | — | — |
| E4 | Rótulos | Pontos positivos: abas com `aria-current`, tablist na aula, `aria-label` na tesoura, nos quadradinhos e no selo. Falta rótulo acessível nas linhas da agenda (cor da matéria só por faixa colorida, `AgendaLista.tsx:34`). | Baixo | Baixo |

**O que já está bom e deve ser mantido:** moldura única (`Pagina.tsx`), mensagens de falha ao salvar com orientação ("Confira a internet…"), estados vazios explicados em todas as listas, retomada automática na primeira questão não respondida, "Desfazer" nos flashcards, confirmação antes de apagar progresso, Conversa da turma só depois de responder.

---

## 4. Mapa proposto

Ideia central: **4 abas por intenção** (o que faço agora / o que estudo / o que reviso / como estou), com a agenda dentro de "Hoje", e todas as telas de acompanhamento levando direto ao conteúdo.

```
[Aba] Hoje  /                         ← Início renomeado: "o que fazer agora"
  ├─ Revisão de hoje (limite de novos/dia) → "Começar" abre a sessão direto
  ├─ Suas aulas hoje → cada aula abre a matéria (ou a aula, se ligada)  ← A6
  │    └─ "Semana →" /agenda  (com seletor de grupo ali mesmo)          ← A10
  ├─ Continuar: última aula E último banco de questões                  ← 1 toque
  └─ (sai "Seu progresso", que já está em Desempenho)                   ← A7

[Aba] Estudar  /estudar               ← substitui a aba "Questões"     ← A1, A2
  └─ Matérias (blocos)
       └─ Matéria /materia/[id]   abas: Aulas | Banco de questões
            ├─ Aulas → Aula: Apostila | Questões | Flashcards
            │     └─ fim de cada aba: "Próximo passo" (questões → cards → próxima aula)  ← B1
            └─ Banco de questões (filtros recolhidos num botão "Filtrar", lembrados) ← D5
               "Voltar" volta para a Matéria e a aba Estudar continua acesa         ← A3

[Aba] Revisão  /revisao
  ├─ Fila do dia (todas as matérias)
  └─ Por matéria → toque revisa só aquela matéria                       ← A5

[Aba] Desempenho  /desempenho
  └─ Matéria → Tema → "Treinar este tema" abre o banco já filtrado      ← A4
       + "Refazer as que errei" por matéria

[⚙] Perfil  /perfil                   ← um nome só: "Perfil"           ← A11
  ├─ Nome e grupo · Senha · Apagar progresso · Instalar · Sair
  └─ Administração (só admin) → /admin  (hub próprio)                   ← A9
        ├─ Recados da turma  (a bolinha rosa da ⚙ abre direto aqui)
        ├─ Conteúdo  (Painel + Conteúdo juntos: resumo no topo, lista embaixo) ← A8
        ├─ Alunos
        └─ Agenda da semana
```

**Por que Agenda deixa de ser aba?** Ela já aparece no Hoje ("Suas aulas hoje") e o aluno consulta a semana poucas vezes; a vaga na barra vai para "Estudar", que é usada em toda sessão. *Alternativa*, se a turma usa muito a semana: manter 5 abas (Hoje, Estudar, Revisão, Agenda, Desempenho) — o ganho principal (A1/A2) continua.

**No tablet deitado** (≥ 900 px de largura), a barra de baixo pode virar uma coluna lateral fixa à esquerda e o conteúdo usar até ~1000 px; na questão, alternativas à esquerda e explicação/Conversa da turma à direita (D2). Durante sessões de cards/questões, a barra some e aparece só um "✕ Sair da sessão" (D6).

### Toques antes × depois

| Tarefa | Hoje | Proposto | Como |
|---|---|---|---|
| 1. Fazer questões de uma matéria | 2 | **2** (ou **1** pelo "Continuar") | Estudar → matéria → aba Banco já aberta se veio do banco; Continuar lembra o último banco |
| 1b. Refazer as que errei | 3 | **2** | Desempenho → "Refazer as que errei" da matéria |
| 1c. Treinar o tema fraco | 4 + rolagem | **2** | Desempenho → tema |
| 2. Revisar flashcards do dia | 2 | **1** | "Começar revisão" no Hoje já inicia a sessão |
| 2b. Revisar só uma matéria | impossível | **2** | Revisão → matéria |
| 3. Ler a apostila da aula de hoje | 2 + rolagem | **1–2** | Hoje → toque na aula da agenda (1 se ligada à aula, 2 se à matéria) |
| 4. Informar o grupo | 4 | **2** | Agenda → seletor de grupo → escolher |
| Admin: ler recados novos | 2 + rolagem | **1** | Bolinha rosa da ⚙ abre os recados |

---

## 5. Lista priorizada de mudanças

Ordem: primeiro **alto impacto + baixo esforço**, depois o resto. Cada item cita os problemas que resolve.

**Prioridade 1 — alto impacto, baixo esforço**
1. **Telas de carregamento** (`loading.tsx` com esqueleto no formato dos cartões) nas rotas principais. → D1
2. **Limite de flashcards novos por dia** (ex.: 20) no número do Início, no selo e na fila da Revisão. → C1
3. **Temas clicáveis em Desempenho** abrindo o banco já filtrado (`/materia/[id]/questoes?tema=…`), mais "Refazer as que errei" por matéria. → A4
4. **Tela de erro com "Voltar ao início"** e a barra de baixo. → B3

**Prioridade 2 — médio impacto, baixo esforço**
5. "Voltar" do banco de questões respeitar de onde o aluno veio e manter a aba Questões acesa. → A3
6. Agenda: linhas de aula levam à matéria; seletor de grupo direto na Agenda. → A6 (parte), A10
7. Próximo passo no fim das questões e dos cards da aula. → B1, B2
8. Alvos de toque ≥ 44 px (filtros, quadradinhos, abas da aula, botões pequenos) e rótulo "Cortar" maior. → D3, D4
9. Filtros do banco recolhidos num botão "Filtrar" e lembrados entre visitas. → D5
10. Juntar "Painel do conteúdo" e "Conteúdo" numa tela só; bolinha rosa abre os Recados. → A8, A9
11. Tirar "Seu progresso" do Início (ou torná-lo um atalho para Desempenho); manter o selo da Revisão também nas telas de admin. → A7, A12

**Prioridade 3 — limpeza de nomes (baixo impacto, baixo esforço)**
12. Um nome só: "Perfil" ou "Configurações" (tela, botões Voltar e manual); revisar "Revisão"/"Flashcards" e "Questões"/"Banco". Corrigir o texto de `/auth/erro` e atualizar o `CLAUDE.md` (5 abas, tela Painel). → A11, B4

**Prioridade 4 — alto/médio impacto, esforço médio ou alto (a reorganização em si)**
13. **Aba "Estudar"** no lugar de "Questões" (matérias + aulas + banco, com abas na tela da matéria) e Início renomeado para "Hoje". → A1, A2
14. Revisão por matéria (fila filtrada). → A5
15. Modo foco nas sessões (esconder a barra, avisar antes de sair de uma sessão de cards). → D6
16. Layout para tablet deitado (coluna lateral, conteúdo mais largo, questão em duas colunas). → D2
17. Guardar histórico de tentativas em vez de apagar ao refazer (o acerto em Desempenho passa a ser honesto). → E1
18. Ligar cada evento da agenda à aula exata (precisa de um campo novo em `agenda_eventos` e de ajuste no leitor do cronograma). → A6 (completo)

Itens do `MELHORIAS-UX.md` que se encaixam aqui: esqueletos de carregamento (seção 6) = item 1; seletor de grupo na Agenda (seção 4) = item 6; diagnóstico de pontos fracos (seção 5) = item 3.
