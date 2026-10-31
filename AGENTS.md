<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` (resolved from this file's directory; in monorepos the `next` package may not be visible from the repo root) before writing any code. Heed deprecation notices.

This block is written and re-added by `next dev` — verify at `node_modules/next/dist/server/lib/generate-agent-files.js`. Removing it from a diff only re-creates the uncommitted change; committing it with your work keeps the tree clean.

<!-- END:nextjs-agent-rules -->

# Med Genius — manual do projeto

App de estudos da turma de Medicina (FAG) do Mauricio: apostilas de cada aula, banco de questões, flashcards com repetição espaçada, agenda da semana e desempenho.
Tudo em português do Brasil. O dono do projeto não é programador: explique em linguagem simples.

## Onde fica cada coisa

| | |
|---|---|
| Site | https://medgenius.vercel.app (o endereço antigo caderno-clinico.vercel.app não existe mais) |
| Código | GitHub `s9tabmauricio-stack/caderno-clinico`, ramo `main` |
| Publicação | A Vercel publica sozinha a cada `git push origin main` (1–2 min). Ramos `claude/**` não geram publicação de prévia (`vercel.json`), para não encher o "Deployment Storage" (limite de 10 GB no plano gratuito) |
| Banco | Supabase, projeto `xtlpmtylifbalzxnfkib` (São Paulo), plano gratuito |
| Administrador | CPF 086.994.266-23 (variável `ADMIN_CPFS` na Vercel; padrão no código) |
| Arquivos do projeto | Pasta **MEDGENIUS** no Google Drive do Mauricio (s9tabmauricio@gmail.com), https://drive.google.com/drive/folders/1i6ftIjwzgyfExlT8PYXXOhe5bFI8vMqR. Desde 31/10/2026, tudo o que for guardado fora do Git (PDFs, rascunhos, apostilas, materiais) vai para lá |
| Chave secreta | `SUPABASE_SECRET_KEY` na Vercel (usada só no servidor: alunos, agenda, conteúdo) |

## Tecnologia

- Next.js 16 (App Router, `proxy.ts` no lugar de middleware, `params`/`searchParams` assíncronos, tipos `PageProps<'/rota'>`).
  Rotas novas: rode `npx next build` antes do `tsc`, porque os tipos das rotas são gerados no build.
- React 19, `@supabase/ssr` com chave publicável (`lib/supabase/config.ts`). Letras: Inter (`--font-texto`) em tudo o que se lê e se digita (enunciado, alternativas, flashcards, recados, campos, números); Cinzel (`--font-marca`) só nos títulos das telas, nomes das matérias, rótulos em maiúsculas, números grandes isolados e na tela de entrada (MED GENIUS, ENTRAR). A Cinzel não tem minúsculas de verdade (mg e Mg ficam quase iguais), nem algarismos de largura fixa, nem símbolos como β, ≥ e →. A lista fica no bloco "Letras" no fim de `app/globals.css`.
- Leitura de dados: `lib/dados.ts`; agenda: `lib/agenda.ts` (leitor do cronograma) e `lib/agenda-dados.ts`; admin: `lib/admin.ts`.
- Repetição espaçada: `lib/srs.ts`. Explicação por alternativa: `lib/explicacoes.ts`.

## Login

- CPF + senha. O Supabase exige e-mail, então cada CPF vira o e-mail interno `CPF@caderno-clinico.vercel.app`
  (`DOMINIO_LOGIN` em `lib/cpf.ts`). **Nunca mude esse domínio**: as contas existentes dependem dele (é só um identificador, não o endereço do site).
- Contas são criadas pelo administrador em Configurações → Alunos (`/admin`). Cadastro aberto deve ficar desligado no Supabase.
- Nunca digite senhas ou chaves em sites; quem cria contas e configura chaves é o Mauricio.

## Telas

- Nomes na tela (manter): **Configurações** (nunca "Perfil"; só o endereço `/perfil` e o código usam esse nome), **Revisão** = fila de flashcards do dia, **Flashcards** = os cards de uma aula (ou, na aba da matéria, de todas as aulas dela), **Estudar** = a aba das matérias (aulas e banco), **Questões** = as de uma aula, **Banco de questões** = todas as questões de uma matéria.
- **Tablet deitado** (tela de pelo menos 900 × 560 px): a barra de abas vira uma coluna de vidro à esquerda e as telas de estudo (Início, Estudar, Matéria, Banco, Aula, Desempenho) usam mais largura (`<Pagina larga>`). Início com a agenda na coluna da esquerda e cards, questões e matérias à direita; a questão fica como no celular (enunciado em cima, alternativas embaixo, na largura toda da coluna, alinhada com o resto da tela); as barras de abas (da matéria e da aula), a apostila e os flashcards também usam a largura toda da coluna; Desempenho em duas colunas. Em pé ou no celular nada muda. O CSS está no fim de `app/globals.css`.
- Início (proposta E do quadro https://claude.ai/artifact/BjQhu55DNueYG5a7zFWucg): saudação (só o primeiro nome); cartões **Cards** (para revisar hoje, novos, a revisar, em dia e o botão da Revisão) e **Questões** (respondidas, acerto, certas/erradas/a fazer e "Refazer as erradas"); **Agenda de hoje** inteira (as aulas que já passaram ficam apagadas, a de agora e a próxima marcadas, e a primeira aula de amanhã no pé); **Próximas provas** logo abaixo da agenda (no tablet, na mesma coluna): a próxima prova que ainda não começou num cartão com a contagem regressiva em dias, horas e minutos (`components/ContagemProva.tsx`, atualiza sozinha; na hora da prova vira "Boa prova!") e o botão "Estudar para a prova", e as três seguintes em lista; "Todas →" abre a lista na Agenda (`/agenda#provas`); **Matérias** em cartões com a gema e o progresso (a da última aula estudada tem "Continuar").
- **Revisão** (`/revisao`): fila do dia com todos os cards (lidos de 1000 em 1000 por `lerTudo` em `lib/dados.ts`, porque cada leitura do Supabase para em 1000). Os botões de matéria no topo (e a lista "Por matéria") abrem `/revisao?materia=<id>`, que revisa só os cards daquela matéria.
- **Estudar** (`/estudar`): uma carta por matéria (aulas, progresso) com o atalho do Banco de questões embaixo. `/questoes` só redireciona para cá.
- Barra de baixo: Início, Agenda, Matérias, Revisão, Desempenho. A tela "Configurações" (`/perfil`) fica na engrenagem do canto superior direito (todas as telas); a engrenagem sempre abre Configurações. Para o administrador, há atalhos próprios de Administração e Recados com contador no topo.
- Início: as aulas de hoje e as matérias abrem a matéria; "Refazer as erradas" abre o banco filtrado (erradas numa matéria só) ou o Desempenho. Desempenho: cada tema abre o banco já filtrado e cada matéria tem "Refazer as erradas".
- Banco de questões: os filtros ficam recolhidos no botão "Filtrar"; tema, prova e situação ficam na URL e lembrados no cookie `mgf_<matéria>`. O botão Voltar aceita `?retorno=` apenas para rotas internas de estudo e mantém compatibilidade com `?de=` (desempenho ou `aula:<id>`). No Desempenho, retorna à seção da matéria; nas aulas, preserva a aba e a origem da busca.
- Aula: abas Apostila / Questões / Flashcards. Matéria: abas **Aulas | Banco de questões | Flashcards** (as três telas mostram as mesmas abas, na largura toda, alinhadas com o que vem embaixo; no celular o número de cada aba fica embaixo do nome; o Banco tem filtros por tema e prova; Flashcards, `/materia/<id>/flashcards`, estuda os cards de todas as aulas da matéria e lista os cards por aula).
- Questões: antes de responder, cada alternativa tem a faixa "Cortar" (tesoura; Shift + letra), que vale só enquanto o aluno está na questão. Depois de responder, certa em verde, erradas em vermelho, a marcada em destaque; comentário embaixo da certa e o motivo embaixo de cada errada. No topo do cartão, o botão **Copiar** (todos os alunos) copia só o enunciado e as alternativas (A) …, B) …), sem gabarito nem comentário, para o aluno conferir na IA dele. Para o administrador, cada questão tem o botão **Editar** (no canto do cartão) que abre o mesmo editor de Conteúdo ali mesmo.
- **Conversa da turma** (embaixo da questão, só depois de responder): o aluno deixa "💡 Insight para os colegas" ou "⚠️ Erro na questão"; aparece como "Augusto deixou uma dica" / "Augusto achou um erro" (sem artigo, vale para qualquer nome). Colegas marcam dica como 👍 Útil; o autor apaga o próprio recado.
- Administração (atalho próprio no topo → Central, com menu persistente entre as seções): **Central** (`/admin/central`, desenho em https://claude.ai/artifact/4hnQkbH11HogQ5NMYGAhq6: "Precisa de você" com os avisos (aulas sem questões, alunos sem entrar há 7 dias ou mais, agenda da semana não publicada, recados), uso da turma com gráfico de 14 dias de questões e cards, alunos com último acesso, conteúdo por matéria, questões que a turma mais erra, próxima prova e espaço do banco; os números vêm da função `central_resumo()` do banco, que só a chave secreta chama; código em `lib/central.ts` e `components/admin/Central.tsx`), **Recados da turma** (`/admin/recados`: contador no atalho Recados com os novos; marcar visto/corrigido, abrir a questão, apagar), **Alunos** (`/admin`), **Conteúdo** (`/admin/conteudo`: resumo do que está no ar, editar/apagar aulas, questões, flashcards (na aula, "Apagar os N flashcards" apaga todos de uma vez, para refazer no padrão novo) e limpar versões antigas; `/admin/painel` só redireciona para cá), **Agenda da semana** (`/admin/agenda`: colar o cronograma do WhatsApp).

## Banco de dados

- `materias` (id curto: `nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`; `cor_inicio`/`cor_fim`, `descricao`, `ordem`)
- `aulas` (id `<materia>-a<N>`, ex.: `uro-a2`; `titulo`, `resumo`, `apostila_html`, `publicada`, `ordem`)
- `questoes` (`materia_id`, `aula_id` opcional, `ordem`, `enunciado`, `alternativas` jsonb, `correta` = índice 0–4, `comentario`, `por_que_erradas`, `tema`, `prova`, `fonte`, `origem`, `substituida_por`)
- `flashcards` (id `<aula>-fNN`, `frente`, `verso`, `ordem`)
- Progresso: `respostas` (só a última resposta de cada questão), `historico_revisoes` (cada avaliação de flashcard, com `errou` e `intervalo_dias`; gravada por gatilho em `revisoes`: "Desfazer" tira a linha desfeita e apagar o card de `revisoes` apaga o histórico dele; desde 27/10/2026, antes disso só a última revisão de cada card), `historico_respostas` (todas as respostas dadas: um gatilho do banco grava uma linha a cada resposta nova ou refeita; só o gatilho grava e o aluno só lê e apaga o seu; "Refazer" não apaga, só "Apagar progresso"), `revisoes`; alunos: `perfis` (`nome`, `grupo` de prática 1–29; o aluno só pode alterar `nome` e `grupo`)
- Recados: `recados` (`questao_id`, `user_id`, `autor` = primeiro nome, preenchido por gatilho; `tipo` `insight`/`erro`; `status` `novo`/`visto`/`corrigido`) e `recados_uteis`. Aluno lê todos, cria e apaga os seus; status só muda pelo admin (chave secreta).
- Agenda: `agenda_semanas` (segunda-feira da semana; `texto` vazio = semana criada só para as provas) e `agenda_eventos` (aulas, cancelamentos, avisos, `grupos int[]`; `fixo` = incluído à parte, como as provas da P2, e a publicação da semana não apaga)
- Visões usadas pelas telas: `questoes_do_aluno`, `progresso_aulas`, `progresso_materias`, `progresso_temas`, `progresso_tentativas` (tentativas e acerto "na 1ª vez", mostrados no Desempenho), `flashcards_do_aluno`.
  Todas escondem aulas não publicadas e questões com `substituida_por` preenchido.
- RLS: alunos leem conteúdo e só gravam o próprio progresso. Escrita de conteúdo: só pelo conector (Claude) ou pelas telas de admin (chave secreta).
- A pasta `supabase/migrations/` não reflete tudo o que foi aplicado; a verdade é o banco (`list_migrations`).

### Limite do conector do Supabase (importante)

Pelo conector, **incluir dados e alterações curtas funcionam**; **apagar e reescrever textos longos são cancelados** (trava de confirmação que a sessão não consegue mostrar). Não tente contornar.
- Corrigir uma questão: inclua uma versão nova (`<id>-v2`, mesma ordem) e marque a antiga com `update ... set substituida_por = '<id>-v2'`. Leve os recados junto: `update public.recados set questao_id = '<id>-v2' where questao_id = '<id>'`. Depois o Mauricio limpa em Conteúdo → Limpeza (a limpeza também move os recados que sobrarem para a versão nova).
- Apagar ou ajustar texto: o Mauricio faz em Conteúdo.

## Como subir uma apostila (o jeito aprovado: páginas iguais ao PDF)

1. `pdftoppm -scale-to-x 1400 -scale-to-y -1 -jpeg -jpegopt quality=80 arquivo.pdf public/apostilas/<aula-id>/p`
2. Converter cada página para `NN.webp` (qualidade 78) e apagar os .jpg; copiar o PDF como `public/apostilas/<aula-id>/apostila.pdf`.
3. Commit + push (as imagens precisam estar no ar).
4. Incluir a aula pelo conector:

```sql
insert into public.aulas (id, materia_id, ordem, titulo, resumo, publicada, apostila_html)
select '<aula-id>', '<materia>', <N>, '<Título>', '<Resumo da capa>', true,
  '<div class="paginas"><div class="pdfbar"><span class="main"><span class="t">Apostila em PDF</span><span class="s"><P> páginas · abre numa nova aba</span></span><a class="btn ghost sm" href="/apostilas/<aula-id>/apostila.pdf" target="_blank" rel="noopener">Abrir</a></div>'
  || (select string_agg(format('<img src="/apostilas/<aula-id>/%s.webp" width="1400" height="1980" alt="Página %s de <P>"%s decoding="async">', lpad(i::text, 2, '0'), i, case when i = 1 then '' else ' loading="lazy"' end), '' order by i) from generate_series(1, <P>) i)
  || '</div>'
on conflict (id) do nothing;
```

Título, resumo e professor saem da capa (`pdftotext -f 1 -l 1`). Atualize a `descricao` da matéria com o professor. Trocar uma apostila = sobrescrever as imagens e o PDF e publicar. **Se o número de páginas mudar**, refaça também o `apostila_html` da aula (mesmo modelo acima, com o número novo), senão as páginas a mais não aparecem; pelo conector isso funciona, porque o comando é curto mesmo gerando um texto longo.

**Guarde o HTML da apostila em [`apostilas-fonte/<aula-id>/`](apostilas-fonte/README.md)** (o arquivo de onde o PDF é gerado, com as figuras e os programas que as desenham). Sem ele, mudar o visual obriga a remontar a apostila inteira a partir do PDF. As apostilas anteriores a 31/10/2026 ainda não têm esse arquivo; as de Pneumologia 1 a 4 já têm.

## Questões

- `alternativas`: lista de textos sem a letra; `correta`: índice (0 = A).
- `comentario`: aparece embaixo da alternativa certa.
- `por_que_erradas`: uma linha por letra (`B: …`, ou `A, C e E: …` para várias). Linhas sem letra viram o quadro "Sobre as alternativas".
- `origem`: `professor` (corrigida em sala), `unica`, `inferido` (alternativa reconstruída), `montada` (alternativas montadas, gabarito não oficial), `resolvida` (gabarito não oficial), `adaptada` (questão oficial alterada para seguir a aula; o comentário diz o que mudou).
- Quando a prova não tem gabarito: resolva com base na apostila da aula, marque como não oficial e **discuta as duvidosas com o Mauricio uma a uma, mostrando o texto completo da questão** antes de pedir decisão.

## Flashcards

- Feitos a partir da apostila da aula, na ordem dela, cobrindo a apostila inteira com folga (Pneumonia, `pneumo-a2`: 101 cards).
- **Frente:** pergunta curta e direta ("Qual é a definição de enfisema?"); comparação com × ("Asma × DPOC: o que muda…?"); mini-caso quando ajuda ("70 anos, PA 100 por 70…: quantos pontos e qual conduta?").
- **Verso:** a resposta em 1 a 3 frases, linguagem simples, sem tópicos.
- **"PROVA · "** no começo da frente quando o professor diz que cai na prova ou que é importante (marca PROVA da apostila, "isso vocês precisam saber", "a definição importa muito", slides de "questões de prova") **e também quando ele só dá a entender que é importante**: fez questão de perguntar à turma, repetiu, frisou, insistiu, chamou a atenção. Na dúvida, marque como PROVA, sem perguntar ao Mauricio (regra dele, 22/10/2026).
- O que vem do "Complemento: fora da aula" da apostila entra avisando no próprio card ("Fora da aula: …").
- ids `<aula>-f01`, `-f02`… (acima de 99 seguem `-f100`, `-f101`); `ordem` = número do card. Mostrar a lista ao Mauricio antes de incluir.
- **Agente `flashcards`** (`.claude/agents/flashcards.md`) faz tudo isso: "faça os flashcards da Gastro 1" monta o rascunho em `rascunhos/flashcards/<aula>.md` (pasta fora do Git) para o Mauricio aprovar; "inclua o rascunho aprovado da gastro-a1" grava no banco. Ele lê a apostila com `python3 -I scripts/apostila-texto.py <pdf>`, que mantém os selos PROVA dos títulos (o `pdftotext` os perde).

## Agenda

- O Mauricio cola o cronograma do WhatsApp em `/admin/agenda`; `lib/agenda.ts` separa dias, horários, matéria (emoji ou palavra), professor, local, grupos, cancelamentos (❌) e avisos. Grupos por letra (A = práticas 1 a 7…) viram números.
- Teóricas valem para todos; práticas, só para os grupos listados. O aluno informa o grupo na própria Agenda (seletor ao lado dos filtros) ou em Configurações. Tocar numa aula abre a matéria dela.
- **Provas (P2 de 10 a 25/11/2026)**: entram pelo conector em `agenda_eventos` com `tipo = 'prova'`, `fixo = true`, título "P2 de <Matéria>" (crie antes a semana em `agenda_semanas` só com a segunda-feira, se ela ainda não existir). Aparecem no dia (Início e Agenda) e no quadro "Próximas provas" no fim da Agenda. Publicar a semana não apaga; se o cronograma do WhatsApp trouxer a prova da mesma matéria no mesmo dia, no dia vale a do cronograma. Semana só de provas não aparece em "Semanas publicadas" nem vira "a próxima semana" antes de chegar.

## Visual

**"Vidro líquido em titânio, dia e noite"** (`visual-v6`, 21/10/2026): o app inteiro com a cara da tela de entrada, igual ao quadro https://claude.ai/artifact/PCHBA8oq7akRzq53ihLkSm. Noite (padrão) = fundo preto com luz fria no alto e azul embaixo; dia = fundo prateado e vidro branco; só as cores mudam, e a barra do navegador acompanha. O aluno escolhe **Auto | Dia | Noite** (Auto segue o modo do aparelho) embaixo do cartão da entrada e em Configurações → Aparência (`components/TemaEscolha.tsx`); a escolha fica salva no aparelho (`localStorage` `mg-tema`). Um script no `<head>` (`lib/tema.ts`, chamado em `app/layout.tsx`) põe `data-tema="dia"` ou `"noite"` no `<html>` antes de pintar; o CSS do dia usa `:root[data-tema="dia"]` (nunca `@media (prefers-color-scheme)`). Cada cor tem um só trabalho:
- Titânio (metal prateado frio, nunca dourado) = ação principal (botão polido com texto escuro: Começar revisão, Próxima questão, Bom, ENTRAR), títulos e números grandes em metal. Azul (`#5AD8FF` à noite, `#0A6491` de dia) = toque, seleção (anel azul nas cápsulas e alternativas), aba ativa, selo de pendências e progresso. Verde = certo; coral = errado; âmbar = aviso e aula cancelada.
- Cartões em vidro líquido (reflexo no alto, sem borda), "Revisão de hoje" com filete de titânio, barra de abas em cápsula de vidro flutuante, engrenagem em vidro. No canto de cima, um dendrito de titânio apagado com pontas azuis. Matérias (Estudar e Início) em cartões de vidro com a "gema" da matéria: etiqueta na cor de pedra preciosa com o nome inteiro da matéria escrito dentro (`.gema.nome-gema`).
- Flashcards: Errei coral, Difícil âmbar, Bom titânio, Fácil azul.
- Matérias em tons de pedra preciosa (texto branco legível): nefro `#2563EB`/`#1E3A8A`, pneumo `#0E7490`/`#155E75`, gastro `#047857`/`#065F46`, orto `#B45309`/`#7C2D12`, uro `#6D28D9`/`#4C1D95`, pass `#BE185D`/`#831843`. A cor clara de cada matéria (agenda, brilho do bloco) fica em `COR_MATERIA` (`lib/agenda.ts`).
Tokens e regras no fim de `app/globals.css` (bloco "Vidro líquido em titânio", depois do "Tema Med Genius" e do "Neon com foco", que ele sobrepõe). Ícones do app em `public/icons`, `app/icon.png`, `app/apple-icon.png`; logo em `public/brand/med-genius.webp` (ícone de 20/10/2026, em titânio desde 21/10/2026: um "M" grande de fitas prateadas entrelaçadas, com pontas de circuito e pontos azuis acesos, sobre fundo azul-noite com circuito apagado; o original dourado de 2048 px está em `public/brand/med-genius-original.jpg`; a versão titânio sai dele trocando os tons dourados (matiz 14°–70°) por cinza quase sem cor, sem mexer nos azuis). Tamanhos: iPhone (`apple-icon`) e logo da tela de entrada usam a arte inteira ; `icon-192`/`icon-512` são a arte inteira com cantos arredondados (22,5%); Android (`maskable-512`) é a arte em 85% sobre degradê do mesmo fundo (`#182335` → `#070E1F`), para o M não ser cortado no ícone redondo; a aba do navegador (`app/icon.png`, 64 px) usa só o M (quadrado de 1720 px a partir de x 163, y 205; cantos de raio 14).
Tela de entrada: "ícone de titânio + vidro líquido" (bloco "Tela de entrada" no fim de `app/globals.css`; desenho do fundo em `app/login/page.tsx`). Noite = fundo preto; dia = fundo prateado e vidro branco (mesma escolha Auto | Dia | Noite do app, em cápsula de vidro embaixo do cartão). Logo inteiro com cantos arredondados, dendritos de titânio com pontas azuis saindo de trás dele, "MED GENIUS" metálico com "Medicina · FAG" em titânio e, num cartão de vidro, os rótulos CPF e SENHA sobre campos em cápsula (ícone à esquerda, texto centralizado, olho para mostrar a senha), campo em uso em azul e botão ENTRAR de titânio polido. Sem rodapé e sem aviso de senha esquecida. Quadro com as propostas: https://claude.ai/artifact/79Wh5QshdmEBprBVHxzrsD

Versões do visual salvas no GitHub (ramos fixos, não publicados; não apague):
- `visual-v1`: o tema neon anterior, como estava em 20/10/2026. Para voltar a ele: `git revert` do commit "Neon com foco" e as cores da v1 abaixo no banco.
- `visual-v3`: "Neon com foco" (voltou em 20/10/2026 desfazendo a v4; as telas de dentro continuam nele).
- `visual-v6`: "Vidro líquido em titânio, dia e noite" (no ar desde 21/10/2026): o app inteiro no vidro da entrada, com titânio no lugar do dourado (inclusive ícone e entrada) e modo dia/noite em todas as telas. Para voltar a ela depois de mudanças: `git checkout visual-v6 -- app public components lib` e publicar.
- `visual-v5`: "Vidro líquido dia e noite" (no ar de 21/10/2026 até a v6, commit `7300add`): o app neon da v3, o ícone do "M" de fitas douradas e prateadas e a tela de entrada de vidro líquido que segue o modo dia/noite do aparelho. Para voltar a ela depois de mudanças: `git checkout visual-v5 -- app public components lib` e publicar (ou `git revert` dos commits feitos depois de `7300add`).
- `visual-v4`: "Ouro, Cromo & Sinapse" (fundo grafite, ouro na ação, azul sinapse no progresso, cromo nas molduras; telas iguais ao quadro https://claude.ai/artifact/19dnhpGriy7UQL9NA4Fn4d). Feita nos commits `35bcad8` e `9d05bba`. Para voltar a ela: `git revert` do commit "Volta ao visual-v3" (as cores das matérias no banco são as mesmas).
- `visual-v2`: "Ouro & Sinapse" (azul-noite, vidro com filete dourado, botão principal dourado, ciano para toque, coral para erro, fonte Cinzel). Foi feito nos commits `21ce774`…`82f847c` e desfeito em `773ce11`. Para voltar a ele: `git revert 773ce11` (resolvendo conflitos com o que mudou depois) e trocar as cores das matérias no banco (`cor_inicio`/`cor_fim`): nefro `#1E4FA8`/`#14306B`, pneumo `#0F6E8C`/`#0B4560`, gastro `#11735A`/`#0A4A3C`, orto `#9A6A1F`/`#5E3F10`, uro `#5B3A9E`/`#352263`, pass `#8E2F45`/`#561B2A`. As cores da v1: nefro `#0B5BD3`/`#3B4FC9`, pneumo `#00B8F0`/`#3F6BFF`, gastro `#3EE6A8`/`#00B8F0`, orto `#FFB547`/`#FF5C8A`, uro `#6A5CFF`/`#E92FC0`, pass `#4FDDFF`/`#9B7BFF`. O quadro com a proposta: https://claude.ai/artifact/Dzu7Jr27Wc7WTo7ZMLq5G6

## Claude e Codex (dois assistentes no mesmo projeto)

- Este manual vale para os dois. O `CLAUDE.md` só aponta para cá: mudanças no manual vão neste arquivo.
- Cada um trabalha no seu ramo (`claude/...` ou `codex/...`); os dois tipos de ramo não geram prévia na Vercel (`vercel.json`). O Claude publica com `git push origin main`. O Codex entrega por PR de um ramo `codex/...`, e o GitHub junta sozinho ao `main` se o site compilar (`.github/workflows/codex-automerge.yml`); se não compilar, o PR fica aberto e nada vai para o ar.
- Só o Claude tem o conector do Supabase. Sem ele (Codex), não tente gravar no banco: mexa só no código e deixe questões, flashcards, aulas e provas para o Claude.
- Um assunto por vez para cada um, para as mudanças não baterem na mesma tela.

## Como trabalhar com o Mauricio

- Ele é sensível a custo: prefira o caminho barato (converter arquivos em vez de reescrever conteúdo; não reenviar textos grandes à toa).
- Mostre o conteúdo (a questão, a tela) antes de pedir uma decisão; um assunto por vez.
- Publique e diga em uma ou duas frases o que mudou; diga claramente o que não foi testado.
- Não deixe lixo: o que for substituído deve poder ser limpo (Conteúdo → Limpeza).

## Pendências e ideias

- Questões das aulas novas (Pneumo 1 já tem 9 questões; Pneumo 2 tem 11, 8 do Revalida; Pneumo 4 tem 17 desde 28/10/2026: 1 do Revalida 2024/2, 3 de residência e 13 montadas pela aula; as outras aulas ainda não). O Revalida quase não cobra pneumonia hospitalar (procurado de 2016 a 2026/2).
- Flashcards: todas as aulas no ar estão no padrão novo desde 23/10/2026 (2.611 cards): Pneumo 1 tem 171, Pneumo 2 tem 101, Pneumo 3 tem 113, Gastro 1 tem 152, Gastro 2 tem 133, Gastro 3 tem 198, Nefro 1 tem 99, Nefro 2 tem 156, Nefro 3 tem 147, Nefro 4 tem 154, Nefro 5 tem 133 (quatro trechos duvidosos da apostila conferidos em literatura em 28/10/2026), Orto 1 tem 166, Uro 1 tem 175, Uro 2 tem 160, PASS 1 tem 141, PASS 2 tem 153 e PASS 3 tem 118. Pneumo 4 (pneumonia hospitalar, no ar desde 28/10/2026) tem 141. Aula nova: peça ao agente `flashcards`.
- Provas do Revalida (INEP): o servidor manda o certificado incompleto; baixe com `curl --cacert` num arquivo que junte `/root/.ccr/ca-bundle.crt` e o intermediário "RNP ICPEdu GR46 OV TLS CA 2025" (http://secure.globalsign.com/cacert/rnpicpedugr46ovtlsca2025.crt, convertido para PEM). A prova de 2022.1 tem a fonte embaralhada no PDF: confira o texto na imagem da página.
- Proteção contra senhas vazadas do Supabase está desligada (recurso do plano pago).
- Sugestões e ideias de experiência do usuário (UX): veja [`MELHORIAS-UX.md`](MELHORIAS-UX.md).

## Encontrar conteúdo e voltar

- A tela Matérias não tem busca (retirada a pedido do Mauricio em 31/10/2026).
- Flashcards de aula/matéria permitem estudar livremente; Revisão reúne cards novos e pendentes para hoje. As telas explicam a diferença e oferecem atalhos entre elas.
