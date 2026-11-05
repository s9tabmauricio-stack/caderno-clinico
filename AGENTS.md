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
| Tabelas, visões e gatilhos do banco; subpastas do Drive | [`docs/banco.md`](docs/banco.md) |
| Visual: cores, letras, ícones, versões antigas | [`docs/visual.md`](docs/visual.md) |
| Como fazer uma apostila (mapa, slides, as cinco mudanças, imagens do GPT; o que o professor fala manda sempre) | [`docs/apostila-molde.md`](docs/apostila-molde.md) |
| Visual e regras de escrita da apostila (padrão aprovado) | skill `apostila-padrao` (`.claude/skills/apostila-padrao/SKILL.md`, desde 03/11/2026 no projeto) |
| Subir ou trocar uma apostila | skill `subir-apostila` (`.claude/skills/subir-apostila/SKILL.md`) |
| Gerar o PDF de uma apostila (CSS, `render.py`, `checar.py`, fonte Inter) | [`apostilas-fonte/ferramentas/`](apostilas-fonte/README.md): `preparar.sh <pasta>` copia tudo; nunca redigitar |
| Regras das questões e dos flashcards (formato, origem, PROVA, Revalida) | skill `questoes-e-flashcards` e os agentes em `.claude/agents/` |
| Gravar no banco os rascunhos revisados de flashcards e questões | `node scripts/gravar-rascunho.mjs <aula-id>` (precisa de `SUPABASE_SECRET_KEY` no ambiente ou em `.env.local`; sem ela, `--sql`) |
| Conferir as questões de uma aula contra a apostila | skill `conferir-questoes` (`.claude/skills/conferir-questoes/SKILL.md`) |
| Conferir os flashcards de uma aula (já no banco) contra a apostila, em blocos ao mesmo tempo | skill `conferir-flashcards` (`.claude/skills/conferir-flashcards/SKILL.md`) |
| Bula de medicamento no chat | skill `bula-padrao` (`.claude/skills/bula-padrao/SKILL.md`) |
| Lançar provas na Agenda | skill `provas-agenda` |
| Aula nova a partir do áudio | skill `aula-nova` |
| Computador Windows do Mauricio | [`docs/windows.md`](docs/windows.md) |
| Quem está mexendo em quê agora (Claude, Codex, Antigravity) | [`docs/fila.md`](docs/fila.md) |
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
| Arquivos do projeto | Pasta **MEDGENIUS** no Google Drive do Mauricio (s9tabmauricio@gmail.com), https://drive.google.com/drive/folders/1i6ftIjwzgyfExlT8PYXXOhe5bFI8vMqR. Desde 31/10/2026, tudo o que for guardado fora do Git (PDFs, rascunhos, apostilas, materiais) vai para lá. Subpastas e ids em `docs/banco.md` |
| Chave secreta | `SUPABASE_SECRET_KEY` na Vercel (servidor: alunos, agenda, conteúdo) e no ambiente de quem grava conteúdo com `scripts/gravar-rascunho.mjs` (ambiente do Claude na nuvem; `.env.local` no PC, fora do Git) |

## Tecnologia

- Next.js 16 (App Router, `proxy.ts` no lugar de middleware, `params`/`searchParams` assíncronos, tipos `PageProps<'/rota'>`).
  Rotas novas: rode `npx next build` antes do `tsc`, porque os tipos das rotas são gerados no build.
- Antes de publicar código, rode `npm test` (testes em `tests/`). Mudou um comportamento de propósito? Atualize o teste junto.
- React 19, `@supabase/ssr` com chave publicável (`lib/supabase/config.ts`). Letras: Inter no que se lê e se digita, Cinzel só em títulos e rótulos (regras em `docs/visual.md`).
- Leitura de dados: `lib/dados.ts`; agenda: `lib/agenda.ts` (leitor do cronograma) e `lib/agenda-dados.ts`; admin: `lib/admin.ts`.
- Repetição espaçada: `lib/srs.ts`. Explicação por alternativa: `lib/explicacoes.ts`.

## Login

- CPF + senha. O Supabase exige e-mail, então cada CPF vira o e-mail interno `CPF@caderno-clinico.vercel.app`
  (`DOMINIO_LOGIN` em `lib/cpf.ts`). **Nunca mude esse domínio**: as contas existentes dependem dele (é só um identificador, não o endereço do site).
- Contas são criadas pelo administrador em Configurações → Alunos (`/admin`). Cadastro aberto deve ficar desligado no Supabase.
- Nunca digite senhas ou chaves em sites; quem cria contas e configura chaves é o Mauricio.
- Proteção contra senhas vazadas do Supabase está desligada (recurso do plano pago).

## Telas

- Nomes na tela (manter): **Configurações** (nunca "Perfil"; só o endereço `/perfil` e o código usam esse nome), **Revisão** = fila de flashcards do dia, **Flashcards** = os cards de uma aula (ou, na aba da matéria, de todas as aulas dela), **Estudar** = a aba das matérias (aulas e banco), **Questões** = as de uma aula, **Banco de questões** = todas as questões de uma matéria.
- Barra de baixo: Início, Agenda, Matérias, Revisão, Desempenho; engrenagem no canto (Configurações); para o administrador, atalhos de Administração e Recados.
- O resto (cada tela, tablet deitado, Administração) está em `docs/telas.md`.

## Banco de dados

- Conteúdo: `materias` (`nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`…), `aulas` (id `<materia>-a<N>`, `publicada`), `questoes`, `flashcards`. Progresso do aluno: `respostas`, `revisoes` e os históricos. Também `perfis`, `recados` e a agenda. Detalhes em `docs/banco.md`.
- As visões das telas escondem aulas não publicadas e questões com `substituida_por` preenchido.
- RLS: alunos leem conteúdo e só gravam o próprio progresso. Escrita de conteúdo: só pelo conector (Claude ou Antigravity), pelo `scripts/gravar-rascunho.mjs` ou pelas telas de admin (os dois com a chave secreta).
- A estrutura completa do banco (tabelas, visões, funções, gatilhos, regras de acesso) está copiada em `supabase/estrutura-atual.sql`: leia ali antes de consultar o banco. A pasta `supabase/migrations/` não reflete tudo o que foi aplicado. Mudou a estrutura? Atualize a cópia no mesmo trabalho (como em `docs/banco.md`).

### Limite do conector do Supabase (importante)

Pelo conector, **incluir dados e alterações curtas funcionam**; **apagar e reescrever textos longos são cancelados** (trava de confirmação que a sessão não consegue mostrar). Não tente contornar.
- Corrigir uma questão: inclua uma versão nova (`<id>-v2`, mesma ordem) e marque a antiga com `update ... set substituida_por = '<id>-v2'`. Leve os recados junto: `update public.recados set questao_id = '<id>-v2' where questao_id = '<id>'`. Depois o Mauricio limpa em Conteúdo → Limpeza (a limpeza também move os recados que sobrarem para a versão nova).
- Apagar ou ajustar texto: o Mauricio faz em Conteúdo.
- Autorização (regra do Mauricio, 05/11/2026): o `.claude/settings.json` libera o `execute_sql` e o `apply_migration` (estrutura do banco) do conector sem perguntar, em toda conversa do Claude neste projeto.

## Conteúdo (apostilas, questões, flashcards)

- Toda apostila nova ou refeita guarda o HTML de origem em [`apostilas-fonte/<aula-id>/`](apostilas-fonte/README.md). Como publicar: skill `subir-apostila`.
- Questões e flashcards da aula saem dos agentes `questoes`, `flashcards` ou `conteudo`, passam pelo `revisor` e vão para o banco pelo `scripts/gravar-rascunho.mjs` (sem agente). Regras: skill `questoes-e-flashcards`.
- Os agentes de conteúdo (`apostila`, `conteudo`, `flashcards`, `questoes`, `revisor`) rodam sempre no Opus com esforço extra-alto (regra do Mauricio: não abrir mão de qualidade; está no topo de cada arquivo em `.claude/agents/`). Etapas mecânicas não usam agente.
- **Aula nova** (regra do Mauricio, 31/10/2026): ele manda o áudio da aula na conversa ("aula nova") e não encosta em mais nada até publicar. Siga a skill `aula-nova`: transcrição, apostila, flashcards e questões, revisão e publicação, sem perguntar nada.

## Visual

**"Vidro líquido em titânio, dia e noite"** (`visual-v6`, no ar desde 21/10/2026): o aluno escolhe Auto | Dia | Noite; o dia usa `:root[data-tema="dia"]`, nunca `@media (prefers-color-scheme)`. Cada cor tem um só trabalho: titânio (prata fria, nunca dourado) = ação principal, títulos e números grandes; azul = toque, seleção e progresso; verde = certo; coral = errado; âmbar = aviso. Tokens no fim de `app/globals.css`.

**Antes de mexer no visual, leia [`docs/visual.md`](docs/visual.md)**: cores das matérias, letras, flashcards, ícones e logo, tela de entrada e as versões antigas guardadas nos ramos `visual-v1` a `visual-v6` (não apague esses ramos).

## Claude, Codex e Antigravity (três assistentes no mesmo projeto)

- Este manual vale para os três. O `CLAUDE.md` só aponta para cá, e o Antigravity (versão 2.28 em diante) lê a regra `.agents/rules/medgenius.md` (com "s"; a pasta antiga `.agent/` não é mais lida), que também aponta para cá: mudanças no manual vão neste arquivo.
- **Qualquer um faz qualquer trabalho, mas passa pela fila** ([`docs/fila.md`](docs/fila.md)): antes de começar, leia a fila no `main` e anote o assunto e onde vai mexer; se outro já está na mesma tela, aula ou arquivo, não comece e avise o Mauricio. Ao publicar, o PR apaga a linha. As regras estão no topo do arquivo.

| | Código e telas | Conteúdo (aulas, apostilas, questões, flashcards, provas) e banco |
|---|---|---|
| **Claude** (nuvem e PC do Mauricio) | sim | sim, pelo conector do Supabase |
| **Antigravity** (PC do Mauricio) | sim | sim, pelo conector do Supabase |
| **Codex** | sim | não: não tem o conector; não tente gravar no banco |

- **Conteúdo segue as mesmas regras, venha de quem vier.** As skills e os agentes em `.claude/` são o manual de cada assunto e valem para os três: quem não é o Claude lê o arquivo e segue os passos (onde a receita cita uma ferramenta só do Claude, ela diz o que fazer no lugar).
- O conector (Claude e Antigravity; o do Antigravity fica em `~/.gemini/config/mcp_config.json`, preso ao projeto `xtlpmtylifbalzxnfkib`) segue a seção "Limite do conector do Supabase". Mudança na estrutura do banco não precisa mais do "pode" do Mauricio (regra dele, 05/11/2026): leia `supabase/estrutura-atual.sql` antes, atualize a cópia depois e conte a ele em uma frase o que mudou.
- **Publicar:** ramo `claude/…`, `codex/…` ou `antigravity/…` saído do `main` atualizado, `npm test` e `npx next build`, PR para o `main` (o GitHub junta sozinho se passar; rascunho não é juntado). Nunca empurre direto para o `main`, salvo a fila e as exceções. Passo a passo de cada assistente e exceções: [`docs/publicar.md`](docs/publicar.md).
- **Tudo fica no projeto** (regra do Mauricio, 04/11/2026): o que o app precisa mora neste repositório ou na pasta MEDGENIUS do Drive, nunca só na conta de um assistente (skills da conta do Claude, quadros no claude.ai, memória, instruções de projeto). Se a conta do Claude sumir, Antigravity e Codex seguem como se nada tivesse acontecido. Fez algo fora? Copie para cá no mesmo trabalho (quadros de desenho vão em [`docs/quadros/`](docs/quadros/README.md)).

## Como trabalhar com o Mauricio

- Ele é sensível a custo: prefira o caminho barato (converter arquivos em vez de reescrever conteúdo; não reenviar textos grandes à toa). Trabalho mecânico (gravar rascunhos no banco, converter, cortar texto, contar) vai por programa em `scripts/`, sem agente e sem o modelo reescrever o texto; agente Opus só para escrever, conferir e revisar conteúdo.
- Mostre o conteúdo (a questão, a tela) antes de pedir uma decisão; um assunto por vez, anotado na fila.
- Publique e diga em uma ou duas frases o que mudou; diga claramente o que não foi testado.
- Não deixe lixo: o que for substituído deve poder ser limpo (Conteúdo → Limpeza).
- Pedido vago ou `/melhorar <pedido>`: skill `melhorar` (melhora o pedido, recomenda modelo e esforço, faz na hora o que é pequeno).
- Não anote contagens neste manual (quantos cards ou questões cada aula tem): conte no banco ou veja a Central. Várias aulas ainda não têm questões.
