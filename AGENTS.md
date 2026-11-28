<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

# Med Genius — manual do projeto

App de estudos da turma de Medicina (FAG) do Mauricio: apostilas de cada aula, banco de questões, flashcards com repetição espaçada, agenda da semana e desempenho.
Tudo em português do Brasil. O dono do projeto não é programador: explique em linguagem simples.

Este manual tem só as regras de sempre. Os detalhes ficam onde são usados; leia o arquivo antes de mexer naquele assunto:

| Assunto | Onde |
|---|---|
| Como cada tela funciona (Início, Revisão, Banco, Aula, Admin, tablet deitado, Agenda) | [`docs/telas.md`](docs/telas.md) |
| Tabelas, visões e gatilhos do banco | [`docs/banco.md`](docs/banco.md) |
| Visual: cores, letras, ícones, versões antigas | [`docs/visual.md`](docs/visual.md) |
| Fonte da aula (transcrição e slides num arquivo só, base de tudo): guardar e ler um pedaço | `python3 -I scripts/fonte-aula.py guardar <aula-id> --transcricao <arq> --slides <arq>` e `… trecho <aula-id> --minutos 10-35`; detalhes em [`apostilas-fonte/README.md`](apostilas-fonte/README.md) |
| Material de trabalho das aulas (fonte, mapa, HTML da apostila, figuras, compilados e provas em `apostilas-fonte/`): fica no Supabase, não no Git | `node scripts/material.mjs baixar <aula-id\|matéria\|provas>` antes de ler; `… enviar <aula-id\|provas>` depois de mudar; `… listar` |
| Como fazer uma apostila (mapa, slides, as cinco mudanças, imagens do GPT; o que o professor fala manda sempre) | [`docs/apostila-molde.md`](docs/apostila-molde.md) |
| Visual e regras de escrita da apostila (padrão aprovado) | skill `apostila-padrao` (`.claude/skills/apostila-padrao/SKILL.md`, desde 03/11/2026 no projeto) |
| Subir ou trocar uma apostila | skill `subir-apostila` (`.claude/skills/subir-apostila/SKILL.md`) |
| Gerar o PDF de uma apostila (CSS, `render.py`, `checar.py`, fonte Inter) | [`apostilas-fonte/ferramentas/`](apostilas-fonte/README.md): `preparar.sh <pasta>` copia tudo; nunca redigitar |
| Regras das questões e dos flashcards (formato, origem, PROVA, Revalida) | skill `questoes-e-flashcards` e os agentes em `.claude/agents/` |
| FastCardsGenius, antes "Flashcards Dia D" (nome na tela desde 17/11/2026; no código e no banco continua `dia_d`/`diad`) (4ª aba da aula e botão no cartão da aula na matéria: baralho de véspera para resolver as questões das Provas da FAG; fora da Revisão) | [`docs/dia-d.md`](docs/dia-d.md); gravar com `node scripts/dia-d.mjs gravar <aula-id>` |
| Gravar no banco os rascunhos revisados de flashcards e questões | `node scripts/gravar-rascunho.mjs <aula-id>` (precisa de `SUPABASE_SECRET_KEY` no ambiente ou em `.env.local`; sem ela, `--sql`) |
| Limpar as versões antigas de questões corrigidas (o mesmo que o botão Limpeza) | `node scripts/limpar-versoes.mjs` mostra o que sai; `--apagar` apaga, só quando o Mauricio pedir (precisa de `SUPABASE_SECRET_KEY`) |
| Conferir a apostila de uma aula contra a fonte da aula | skill `conferir-apostila` (`.claude/skills/conferir-apostila/SKILL.md`) |
| Conferir as questões de uma aula contra a fonte da aula | skill `conferir-questoes` (`.claude/skills/conferir-questoes/SKILL.md`) |
| Conferir os flashcards de uma aula (já no banco) contra a fonte da aula, em blocos ao mesmo tempo | skill `conferir-flashcards` (`.claude/skills/conferir-flashcards/SKILL.md`) |
| Bula de medicamento no chat | skill `bula-padrao` (`.claude/skills/bula-padrao/SKILL.md`) |
| Lançar provas na Agenda | skill `provas-agenda` |
| Publicar o cronograma da semana colado na conversa | `node scripts/publicar-agenda.mjs <arquivo>` (`--conferir` só mostra; precisa de `SUPABASE_SECRET_KEY`; sem ela, o Mauricio cola em `/admin/agenda`) |
| Aula nova a partir do áudio | skill `aula-nova` |
| Computador Windows do Mauricio | [`docs/windows.md`](docs/windows.md) |
| Codex com acesso ao banco (`scripts/sql.mjs`, como configurar o ambiente) | [`docs/codex.md`](docs/codex.md) |
| Como publicar (ramos, PR, exceções) | [`docs/publicar.md`](docs/publicar.md) |
| Quadros de desenho das telas (cópias do claude.ai) | [`docs/quadros/`](docs/quadros/README.md) |

## Onde fica cada coisa

| | |
|---|---|
| Site | https://medgenius.vercel.app (o endereço antigo caderno-clinico.vercel.app não existe mais) |
| Código | GitHub `s9tabmauricio-stack/caderno-clinico`, ramo `main` |
| Publicação | A Vercel publica sozinha a cada mudança no `main` (1–2 min); ramos de assistente não geram prévia (limite de 10 GB do "Deployment Storage"). Como publicar: [`docs/publicar.md`](docs/publicar.md) |
| Banco | Supabase, projeto `xtlpmtylifbalzxnfkib` (São Paulo), plano gratuito |
| Administrador | CPF 086.994.266-23 (variável `ADMIN_CPFS` na Vercel; padrão no código) |
| Chave secreta | `SUPABASE_SECRET_KEY` na Vercel (servidor: alunos, agenda, conteúdo) e no ambiente de quem grava conteúdo com `scripts/gravar-rascunho.mjs` (ambiente do Claude na nuvem; `.env.local` no PC, fora do Git) |

## Tecnologia

- Next.js 16 (App Router, `proxy.ts` no lugar de middleware, `params`/`searchParams` assíncronos, tipos `PageProps<'/rota'>`).
  Rotas novas: rode `npx next build` antes do `tsc`, porque os tipos das rotas são gerados no build.
- Antes de publicar código, rode `npm test` (testes em `tests/`). Mudou um comportamento de propósito? Atualize o teste junto.
- React 19, `@supabase/ssr` com chave publicável (`lib/supabase/config.ts`). Letras: Inter em todo o app, incluindo títulos e rótulos (regras em `docs/visual.md`).
- Leitura de dados: `lib/dados.ts`; agenda: `lib/agenda.ts` (leitor do cronograma) e `lib/agenda-dados.ts`; admin: `lib/admin.ts`.
- Repetição espaçada: `lib/srs.ts`. Explicação por alternativa: `lib/explicacoes.ts`.

## Login

- CPF ou e-mail + senha (o e-mail é só nome de usuário: a conta já nasce confirmada e o app nunca escreve para ele; `loginParaEmail` em `lib/cpf.ts`). O Supabase exige e-mail, então cada CPF vira o e-mail interno `CPF@caderno-clinico.vercel.app`
  (`DOMINIO_LOGIN` em `lib/cpf.ts`). **Nunca mude esse domínio**: as contas existentes dependem dele (é só um identificador, não o endereço do site).
- **Duas turmas, T28 e T29** (28/11/2026): cada aluno tem uma turma e só vê as matérias e a agenda dela (Laura é da T28, com Neurologia; o resto, T29; o administrador vê tudo). Cada matéria é de um período do curso e cada turma tem um período atual (T29 no 6º, T28 no 7º); a aba Matérias abre no atual. Matéria nova: preencha `turmas` e `periodo`. Detalhes em `docs/banco.md` (Turmas e Períodos).
- Contas são criadas pelo administrador em Configurações → Alunos (`/admin`), com CPF ou com e-mail (uma coisa ou outra por conta). O administrador do app é sempre por CPF. Cadastro aberto deve ficar desligado no Supabase.
- Também nascem sozinhas pelo **robô do Gmail** (12/11/2026): quem manda e-mail de `@minha.fag.edu.br` com assunto "Acesso Med Genius" e uma senha de 6 números ganha conta com esse e-mail. Como funciona e como instalar: [`docs/robo-gmail/`](docs/robo-gmail/README.md).
- **Um aparelho por conta** (regra do Mauricio, 12/11/2026): conta nova fica aberta em 1 aparelho; as de antes dessa data, em 2; o administrador, sem limite. Quem entra num aparelho novo tira a conta do usado há mais tempo, que volta à entrada com aviso. Muda-se por aluno em Alunos → Aparelhos por aluno (`perfis.max_aparelhos`; detalhes em `docs/banco.md`).
- Nunca digite senhas ou chaves em sites; quem cria contas e configura chaves é o Mauricio.
- Proteção contra senhas vazadas do Supabase está desligada (recurso do plano pago).

## Telas

- Nomes na tela (manter): **Configurações** (nunca "Perfil"; só o endereço `/perfil` e o código usam esse nome), **Revisão** = fila de flashcards do dia, **Flashcards** = os cards de uma aula (ou, na aba da matéria, de todas as aulas dela), **Estudar** = a aba das matérias (aulas e banco), **Questões** = as de uma aula, **Banco de questões** = todas as questões de uma matéria.
- Barra de baixo: Início, Agenda, Matérias, Revisão, Desempenho; engrenagem no canto (Configurações); para o administrador, atalhos de Administração e Recados.
- O resto (cada tela, tablet deitado, Administração) está em `docs/telas.md`.

## Banco de dados

- Conteúdo: `materias` (`nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`…), `aulas` (id `<materia>-a<N>`, `publicada`), `questoes`, `flashcards`. Progresso do aluno: `respostas`, `revisoes` e os históricos. Também `perfis`, `recados` e a agenda. Detalhes em `docs/banco.md`.
- **Aulas em ordem de data** (regra do Mauricio, 28/11/2026): o número na tela ("Aula 5", "Pneumo 5", e o da capa da apostila) é `aulas.ordem`, contado pela `data_aula`; o N do id não muda e não é o número da aula. Quando ele falar "Pneumo 7", ache o id com `select id from aulas where materia_id = 'pneumo' and ordem = 7`. Aula que entra com data no meio: renumere as seguintes e refaça a capa das apostilas delas (troque o número no HTML, gere o PDF com o `render.py` e publique).
- As visões das telas escondem aulas não publicadas e questões com `substituida_por` preenchido.
- RLS: alunos leem conteúdo e só gravam o próprio progresso. Escrita de conteúdo: só pelo conector (Claude ou Antigravity), pelo `scripts/sql.mjs` (Codex), pelo `scripts/gravar-rascunho.mjs` ou pelas telas de admin (os dois com a chave secreta).
- A estrutura completa do banco (tabelas, visões, funções, gatilhos, regras de acesso) está copiada em `supabase/estrutura-atual.sql`: leia ali antes de consultar o banco. A pasta `supabase/migrations/` não reflete tudo o que foi aplicado. Mudou a estrutura? Atualize a cópia no mesmo trabalho (como em `docs/banco.md`).

### Limite do conector do Supabase (importante)

Pelo conector, **incluir dados, alterações curtas e apagar funcionam** (apagar funcionou em 19/11/2026); **reescrever textos longos é cancelado** (trava de confirmação que a sessão não consegue mostrar). Não tente contornar.
- Corrigir uma questão: inclua uma versão nova (`<id>-v2`, mesma ordem) e marque a antiga com `update ... set substituida_por = '<id>-v2'`. Leve os recados junto: `update public.recados set questao_id = '<id>-v2' where questao_id = '<id>'`. Depois a versão antiga é limpa: o Mauricio pelo botão em Administração → Conteúdo → Limpeza, ou o assistente com `node scripts/limpar-versoes.mjs --apagar` quando ele pedir (a limpeza move os recados que sobrarem para a versão nova e apaga as respostas dadas na antiga).
- Apagar card ou questão: o assistente apaga pelo conector **quando o Mauricio pedir** (regra dele, 19/11/2026); mostre antes o que vai sair. O progresso dos alunos naquele card sai junto. Limpar versões antigas de questões continua pelo `scripts/limpar-versoes.mjs` (regra do Mauricio, 08/11/2026).
- Ajustar texto longo: o Mauricio faz em Conteúdo.
- Autorização (regra do Mauricio, 05/11/2026): o `.claude/settings.json` libera o `execute_sql`, o `apply_migration` (estrutura do banco) e as consultas do conector (listar tabelas, registros, avisos) sem perguntar, em toda conversa do Claude neste projeto, com todos os nomes que o conector já teve (nuvem, PC, plugin); também liberados os programas `node scripts/…` que gravam no banco (menos `limpar-versoes.mjs --apagar`). Criar, pausar ou apagar projeto, ramo e função continuam pedindo autorização.

## Conteúdo (apostilas, questões, flashcards)

- **Fonte da aula** (regra do Mauricio, 09/11/2026): cada aula tem um arquivo fonte, `apostilas-fonte/<aula-id>/fonte.md`, com a transcrição e o texto dos slides como vieram. Quando ele mandar a transcrição ou os slides de uma aula, a primeira coisa é guardar: `python3 -I scripts/fonte-aula.py guardar <aula-id> --transcricao <arq> --slides <arq>` (texto colado na conversa: salve num arquivo antes) (o programa envia sozinho para o Supabase). Material que chega depois entra com `--acrescentar`.
  - **Dado de aula não mora no Git** (regra do Mauricio, 24/11/2026): a pasta `apostilas-fonte/` (menos `README.md`, `apostila.css` e `ferramentas/`) fica no espaço privado `material` do Supabase Storage; no computador é só cópia de trabalho, ignorada pelo Git. Antes de ler, `node scripts/material.mjs baixar <aula-id>` (ou `provas`, ou a matéria); depois de criar ou mudar algo ali, `node scripts/material.mjs enviar <aula-id>` no mesmo trabalho. Nunca apague nada de lá: o plano gratuito não tem cópia de segurança. Questões, flashcards e compilados não passam pelo Git; a aula nova só leva para o Git as imagens da apostila (`public/apostilas/`).
  - A apostila, as questões e os flashcards são feitos **a partir da fonte, e só dela**, e as conferências (da apostila, das questões e dos flashcards) também são feitas **contra a fonte, e só contra ela**. **A apostila não é guia de nada** (regra do Mauricio, 10/11/2026): ela é produto da fonte e pode ter erros; questões, flashcards e conferências não a leem, nem para achar página, termo ou selo PROVA. A única receita que abre a apostila é a `conferir-apostila` (para corrigi-la pela fonte). Dentro da fonte, a fala manda sobre o slide.
  - Termo que a transcrição automática errou: use o texto dos slides na fonte ou o termo médico correto; nunca a apostila.
  - **Gabarito de prova antiga sai da aula** (regra do Mauricio, 23/11/2026: "gabarito da turma não vale nada"): em compilado, transcrição ou foto de prova, o que a turma marcou ou anotou não é gabarito e nunca é citado no comentário. A resposta é a da fonte da aula; se ela não trata do ponto, procure nas fontes das outras aulas da matéria (e nas correções de prova do professor) e cite de qual aula veio. Achou a resposta numa fonte: decida, sem perguntar. **Só discuta com o Mauricio quando nenhuma fonte tiver a resposta** (regra dele, 23/11/2026): uma questão por vez, com o texto completo; até ele decidir, ela não entra. Nunca use o "consenso médico" por conta própria.
  - Aula sem fonte (as antigas): não faça questões, flashcards nem conferência; peça a transcrição ao Mauricio e guarde-a primeiro.
- Toda apostila nova ou refeita guarda o HTML de origem em [`apostilas-fonte/<aula-id>/`](apostilas-fonte/README.md) e envia para o Supabase. Como publicar: skill `subir-apostila`.
- Questões e flashcards da aula saem dos agentes `questoes`, `flashcards` ou `conteudo`, passam pelo `revisor` e vão para o banco pelo `scripts/gravar-rascunho.mjs` (sem agente). Regras: skill `questoes-e-flashcards`.
- **Questão que o Mauricio manda ou pede na conversa vai sempre para Provas da FAG** (regra dele, 19/11/2026: "tudo que eu mandar"), venha de prova antiga, de algo que o professor disse que cai ou de um pedido como "faça questões desses pontos" (feitas pelo agente `questoes`: cada questão do rascunho leva a linha `**Fonte:** Material da turma · <professor> frisou na aula`). Fica de fora só a produção automática da aula nova: de prova, `prova` preenchido (`p2-tNN`…); sem prova definida, `prova` vazio e `fonte` começando com "Material da turma" (ex.: `Material da turma · Dr. Flávio disse que cai`). Nunca "Montada (aula …)", que a joga em Falas do professor. Detalhes: skill `questoes-e-flashcards`.
- Os agentes de conteúdo (`apostila`, `conteudo`, `flashcards`, `questoes`, `revisor`) rodam sempre no Opus com esforço extra-alto (regra do Mauricio: não abrir mão de qualidade; está no topo de cada arquivo em `.claude/agents/`). Etapas mecânicas não usam agente.
- **Cronograma da semana** (regra do Mauricio, 08/11/2026): quando ele colar na conversa o cronograma do WhatsApp ("CRONOGRAMA SEMANAL", dias e horários), publique na hora, sem perguntar: salve o texto num arquivo (fora do Git) e rode `node scripts/publicar-agenda.mjs <arquivo>`. Depois mostre o resumo e aponte o que o leitor pode ter lido errado (prova marcada como aula, professor com texto grudado). Se algo saiu errado, corrija o leitor (`lib/agenda.ts`) e publique de novo.
- **Aula nova** (regra do Mauricio, 31/10/2026): ele manda o áudio da aula na conversa ("aula nova"), ou a transcrição e os slides pedindo para fazer a aula, e não encosta em mais nada até publicar. Siga a skill `aula-nova`: transcrição, fonte da aula, apostila, flashcards e questões, revisão e publicação, sem perguntar nada.

## Visual

**"Vidro líquido em titânio, dia e noite"** (`visual-v6`, no ar desde 21/10/2026): o aluno escolhe Auto | Dia | Noite; o dia usa `:root[data-tema="dia"]`, nunca `@media (prefers-color-scheme)`. Cada cor tem um só trabalho: titânio (prata fria, nunca dourado) = ação principal, títulos e números grandes; azul = toque, seleção e progresso; verde = certo; coral = errado; âmbar = aviso. Tokens no fim de `app/globals.css`.

**Antes de mexer no visual, leia [`docs/visual.md`](docs/visual.md)**: cores das matérias, letras, flashcards, ícones e logo, tela de entrada e as versões antigas guardadas nos ramos `visual-v1` a `visual-v6` (não apague esses ramos).

## Claude, Codex e Antigravity (três assistentes no mesmo projeto)

- Este manual vale para os três e é o único: o Codex lê este arquivo direto; o `CLAUDE.md` só tem `@AGENTS.md`; o Antigravity (versão 2.28 em diante) lê a regra `.agents/rules/medgenius.md` (com "s"; a pasta antiga `.agent/` não é mais lida), que só manda ler este arquivo. Regra nova ou mudada vai aqui, nunca no `CLAUDE.md` nem na regra do Antigravity. O `npm test` (`tests/manual-assistentes.test.mjs`) confere essa ligação e o tamanho deste arquivo (até 32 KB, o que o Codex lê).
- **Qualquer um faz qualquer trabalho, e sem fila** (regra do Mauricio, 23/11/2026: ele mexe em uma coisa de cada vez): não há anotação de "quem está mexendo em quê"; comece direto, sem commit nenhum antes do trabalho.

| | Código e telas | Conteúdo (aulas, apostilas, questões, flashcards, provas) e banco |
|---|---|---|
| **Claude** (nuvem e PC do Mauricio) | sim | sim, pelo conector do Supabase |
| **Antigravity** (PC do Mauricio) | sim | sim, pelo conector do Supabase |
| **Codex** (site do ChatGPT) | sim | sim, pelo `node scripts/sql.mjs "<SQL>"` no lugar do conector ([`docs/codex.md`](docs/codex.md)) |

- **Conteúdo segue as mesmas regras, venha de quem vier.** As skills e os agentes em `.claude/` são o manual de cada assunto e valem para os três: quem não é o Claude lê o arquivo e segue os passos (onde a receita cita uma ferramenta só do Claude, ela diz o que fazer no lugar). As skills têm uma cópia em `.agents/skills/`, onde o Codex e o Antigravity as acham sozinhos: edite sempre em `.claude/skills/` e rode `node scripts/sincronizar-skills.mjs` (o `npm test` avisa se esquecer). Os agentes de `.claude/agents/` não têm cópia: os outros dois leem o arquivo.
- O Codex não tem o conector: onde as receitas mandam usar o `execute_sql`, ele roda o mesmo SQL com `node scripts/sql.mjs` (token `SUPABASE_ACCESS_TOKEN` no ambiente do Codex, configurado pelo Mauricio; ver [`docs/codex.md`](docs/codex.md)). Valem as mesmas regras do banco.
- O conector (Claude e Antigravity; o do Antigravity fica em `~/.gemini/config/mcp_config.json`, preso ao projeto `xtlpmtylifbalzxnfkib`) segue a seção "Limite do conector do Supabase". Mudança na estrutura do banco não precisa mais do "pode" do Mauricio (regra dele, 05/11/2026): leia `supabase/estrutura-atual.sql` antes, atualize a cópia depois e conte a ele em uma frase o que mudou.
- **Publicar:** ramo `claude/…`, `codex/…` ou `antigravity/…` saído do `main` atualizado, `npm test` e `npx next build`, PR para o `main` (o GitHub junta sozinho se passar; rascunho não é juntado). Nunca empurre direto para o `main`, salvo as exceções. Passo a passo de cada assistente e exceções: [`docs/publicar.md`](docs/publicar.md).
- **Tudo fica no projeto** (regra do Mauricio, 04/11/2026): o que o app precisa mora neste repositório (o material de trabalho das aulas, no Supabase do projeto), nunca só na conta de um assistente (skills da conta do Claude, quadros no claude.ai, memória, instruções de projeto). Se a conta do Claude sumir, Antigravity e Codex seguem como se nada tivesse acontecido. Fez algo fora? Copie para cá no mesmo trabalho (quadros de desenho vão em [`docs/quadros/`](docs/quadros/README.md)).

## Como trabalhar com o Mauricio

- Ele é sensível a custo: prefira o caminho barato (converter arquivos em vez de reescrever conteúdo; não reenviar textos grandes à toa). Trabalho mecânico (gravar rascunhos no banco, converter, cortar texto, contar) vai por programa em `scripts/`, sem agente e sem o modelo reescrever o texto; agente Opus só para escrever, conferir e revisar conteúdo.
- Mostre o conteúdo (a questão, a tela) antes de pedir uma decisão; um assunto por vez.
- Publique e diga em uma ou duas frases o que mudou; diga claramente o que não foi testado.
- Não deixe lixo: o que for substituído deve poder ser limpo (Conteúdo → Limpeza).
- Pedido vago ou `/melhorar <pedido>`: skill `melhorar` (melhora o pedido, recomenda modelo e esforço, faz na hora o que é pequeno).
- Não anote contagens neste manual (quantos cards ou questões cada aula tem): conte no banco ou veja a Central. Várias aulas ainda não têm questões.
