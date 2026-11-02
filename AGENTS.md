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
| Subir ou trocar uma apostila | skill `subir-apostila` (`.claude/skills/subir-apostila/SKILL.md`) |
| Regras das questões e dos flashcards (formato, origem, PROVA, Revalida) | skill `questoes-e-flashcards` e os agentes em `.claude/agents/` |
| Lançar provas na Agenda | skill `provas-agenda` |
| Aula nova a partir do áudio | skill `aula-nova` |
| Computador Windows do Mauricio | [`docs/windows.md`](docs/windows.md) |
| Ideias de experiência do usuário (UX) | [`MELHORIAS-UX.md`](MELHORIAS-UX.md) |

## Onde fica cada coisa

| | |
|---|---|
| Site | https://medgenius.vercel.app (o endereço antigo caderno-clinico.vercel.app não existe mais) |
| Código | GitHub `s9tabmauricio-stack/caderno-clinico`, ramo `main` |
| Publicação | A Vercel publica sozinha a cada `git push origin main` (1–2 min). Ramos `claude/**` não geram publicação de prévia (`vercel.json`), para não encher o "Deployment Storage" (limite de 10 GB no plano gratuito) |
| Banco | Supabase, projeto `xtlpmtylifbalzxnfkib` (São Paulo), plano gratuito |
| Administrador | CPF 086.994.266-23 (variável `ADMIN_CPFS` na Vercel; padrão no código) |
| Arquivos do projeto | Pasta **MEDGENIUS** no Google Drive do Mauricio (s9tabmauricio@gmail.com), https://drive.google.com/drive/folders/1i6ftIjwzgyfExlT8PYXXOhe5bFI8vMqR. Desde 31/10/2026, tudo o que for guardado fora do Git (PDFs, rascunhos, apostilas, materiais) vai para lá. Subpastas e ids em `docs/banco.md` |
| Chave secreta | `SUPABASE_SECRET_KEY` na Vercel (usada só no servidor: alunos, agenda, conteúdo) |

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
- RLS: alunos leem conteúdo e só gravam o próprio progresso. Escrita de conteúdo: só pelo conector (Claude) ou pelas telas de admin (chave secreta).
- A estrutura completa do banco (tabelas, visões, funções, gatilhos, regras de acesso) está copiada em `supabase/estrutura-atual.sql`: leia ali antes de consultar o banco. A pasta `supabase/migrations/` não reflete tudo o que foi aplicado. Mudou a estrutura? Atualize a cópia no mesmo trabalho (como em `docs/banco.md`).

### Limite do conector do Supabase (importante)

Pelo conector, **incluir dados e alterações curtas funcionam**; **apagar e reescrever textos longos são cancelados** (trava de confirmação que a sessão não consegue mostrar). Não tente contornar.
- Corrigir uma questão: inclua uma versão nova (`<id>-v2`, mesma ordem) e marque a antiga com `update ... set substituida_por = '<id>-v2'`. Leve os recados junto: `update public.recados set questao_id = '<id>-v2' where questao_id = '<id>'`. Depois o Mauricio limpa em Conteúdo → Limpeza (a limpeza também move os recados que sobrarem para a versão nova).
- Apagar ou ajustar texto: o Mauricio faz em Conteúdo.

## Conteúdo (apostilas, questões, flashcards)

- Toda apostila nova ou refeita guarda o HTML de origem em [`apostilas-fonte/<aula-id>/`](apostilas-fonte/README.md). Como publicar: skill `subir-apostila`.
- Questões e flashcards da aula saem dos agentes `questoes`, `flashcards` ou `conteudo` e passam pelo `revisor`. Regras: skill `questoes-e-flashcards`.
- Todos os agentes de conteúdo (`apostila`, `conteudo`, `flashcards`, `questoes`, `revisor`) rodam sempre no modelo Opus com esforço extra-alto (regra do Mauricio: não abrir mão de qualidade). Está no topo de cada arquivo em `.claude/agents/`.
- **Aula nova** (regra do Mauricio, 31/10/2026): ele manda o áudio da aula na conversa ("aula nova") e não encosta em mais nada até publicar. Siga a skill `aula-nova`: transcrição, apostila, flashcards e questões, revisão e publicação, sem perguntar nada.

## Visual

**"Vidro líquido em titânio, dia e noite"** (`visual-v6`, no ar desde 21/10/2026). Noite (padrão) e dia: o aluno escolhe Auto | Dia | Noite (`components/TemaEscolha.tsx`, salvo em `localStorage` `mg-tema`); `lib/tema.ts` põe `data-tema` no `<html>` antes de pintar e o CSS do dia usa `:root[data-tema="dia"]`, nunca `@media (prefers-color-scheme)`. Cada cor tem um só trabalho: titânio (prata fria, nunca dourado) = ação principal, títulos e números grandes; azul = toque, seleção, aba ativa e progresso; verde = certo; coral = errado; âmbar = aviso e aula cancelada. Tokens e regras no fim de `app/globals.css`; cor clara de cada matéria em `COR_MATERIA` (`lib/agenda.ts`).

**Antes de mexer no visual, leia [`docs/visual.md`](docs/visual.md)**: cores das matérias, letras, flashcards, ícones e logo, tela de entrada e as versões antigas guardadas nos ramos `visual-v1` a `visual-v6` (não apague esses ramos).

## Claude, Codex e Antigravity (três assistentes no mesmo projeto)

- Este manual vale para os três. O `CLAUDE.md` só aponta para cá, e o Antigravity lê a regra `.agent/rules/medgenius.md`, que também aponta para cá: mudanças no manual vão neste arquivo.
- Cada um trabalha sozinho, no seu ramo (`claude/...`, `codex/...` ou `antigravity/...`); nenhum desses ramos gera prévia na Vercel (`vercel.json`). O Codex e o Antigravity entregam por PR do seu ramo, e o GitHub junta sozinho ao `main` se o site compilar (`.github/workflows/codex-automerge.yml`); se não compilar, o PR fica aberto e nada vai para o ar. Nunca empurre direto para o `main` nem use ramos com outro nome.
- **Antigravity** (Google, no PC Windows do Mauricio, na pasta do projeto): comece cada trabalho de um `main` atualizado (`git fetch origin main && git checkout -B antigravity/<assunto> origin/main`), rode `npm test` e `npx next build`, faça o commit, `git push -u origin antigravity/<assunto>` e abra o PR com `gh pr create --fill --base main`.
- Como o Claude publica (pôr no `main`):
  - **Conversa pela nuvem** (claude.ai/code, app do celular): trabalha no ramo `claude/...` da sessão, abre um PR e, com o trabalho pronto e conferido, junta ao `main` (squash) pelo GitHub. Se o Mauricio pediu para ver antes, espera o "pode publicar". Depois de juntado, o PR não recebe mais nada: o trabalho seguinte começa de novo do `main`, num PR novo.
  - **Computador do Mauricio e aula nova** (que não espera aprovação): publica direto com `git fetch origin main && git rebase origin/main && git push origin HEAD:main` e empurra também o ramo da sessão.
- Só o Claude tem o conector do Supabase. Sem ele (Codex, Antigravity), não tente gravar no banco: mexa só no código e deixe questões, flashcards, aulas, apostilas e provas para o Claude.
- Um assunto por vez para cada um, para as mudanças não baterem na mesma tela.

## Como trabalhar com o Mauricio

- Ele é sensível a custo: prefira o caminho barato (converter arquivos em vez de reescrever conteúdo; não reenviar textos grandes à toa).
- Mostre o conteúdo (a questão, a tela) antes de pedir uma decisão; um assunto por vez.
- Publique e diga em uma ou duas frases o que mudou; diga claramente o que não foi testado.
- Não deixe lixo: o que for substituído deve poder ser limpo (Conteúdo → Limpeza).
- Pedido vago ou `/melhorar <pedido>`: skill `melhorar` (melhora o pedido, recomenda modelo e esforço, faz na hora o que é pequeno).
- Não anote contagens neste manual (quantos cards ou questões cada aula tem): conte no banco ou veja a Central. Várias aulas ainda não têm questões.
