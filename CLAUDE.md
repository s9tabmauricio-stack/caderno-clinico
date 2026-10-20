@AGENTS.md

# Med Genius — manual do projeto

App de estudos da turma de Medicina (FAG) do Mauricio: apostilas de cada aula, banco de questões, flashcards com repetição espaçada, agenda da semana e desempenho.
Tudo em português do Brasil. O dono do projeto não é programador: explique em linguagem simples.

## Onde fica cada coisa

| | |
|---|---|
| Site | https://medgenius.vercel.app (o endereço antigo caderno-clinico.vercel.app não existe mais) |
| Código | GitHub `s9tabmauricio-stack/caderno-clinico`, ramo `main` |
| Publicação | A Vercel publica sozinha a cada `git push origin main` (1–2 min) |
| Banco | Supabase, projeto `xtlpmtylifbalzxnfkib` (São Paulo), plano gratuito |
| Administrador | CPF 086.994.266-23 (variável `ADMIN_CPFS` na Vercel; padrão no código) |
| Chave secreta | `SUPABASE_SECRET_KEY` na Vercel (usada só no servidor: alunos, agenda, conteúdo) |

## Tecnologia

- Next.js 16 (App Router, `proxy.ts` no lugar de middleware, `params`/`searchParams` assíncronos, tipos `PageProps<'/rota'>`).
  Rotas novas: rode `npx next build` antes do `tsc`, porque os tipos das rotas são gerados no build.
- React 19, `@supabase/ssr` com chave publicável (`lib/supabase/config.ts`). Fonte: Cinzel em todo o app (`--font`); os campos de senha usam a Inter (`--font-texto`), porque na Cinzel minúscula e maiúscula ficam quase iguais.
- Leitura de dados: `lib/dados.ts`; agenda: `lib/agenda.ts` (leitor do cronograma) e `lib/agenda-dados.ts`; admin: `lib/admin.ts`.
- Repetição espaçada: `lib/srs.ts`. Explicação por alternativa: `lib/explicacoes.ts`.

## Login

- CPF + senha. O Supabase exige e-mail, então cada CPF vira o e-mail interno `CPF@caderno-clinico.vercel.app`
  (`DOMINIO_LOGIN` em `lib/cpf.ts`). **Nunca mude esse domínio**: as contas existentes dependem dele (é só um identificador, não o endereço do site).
- Contas são criadas pelo administrador em Configurações → Alunos (`/admin`). Cadastro aberto deve ficar desligado no Supabase.
- Nunca digite senhas ou chaves em sites; quem cria contas e configura chaves é o Mauricio.

## Telas

- Nomes na tela (manter): **Configurações** (nunca "Perfil"; só o endereço `/perfil` e o código usam esse nome), **Revisão** = fila de flashcards do dia, **Flashcards** = os cards de uma aula, **Estudar** = a aba das matérias (aulas e banco), **Questões** = as de uma aula, **Banco de questões** = todas as questões de uma matéria.
- **Tablet deitado** (tela de pelo menos 900 × 560 px): a barra de abas vira uma coluna de vidro à esquerda e as telas de estudo (Início, Estudar, Matéria, Banco, Aula, Desempenho) usam mais largura (`<Pagina larga>`). Início em duas colunas; na questão o enunciado fica à esquerda e as alternativas à direita; Desempenho em duas colunas. Em pé ou no celular nada muda. O CSS está no fim de `app/globals.css`.
- Início: saudação (só o primeiro nome), Revisão de hoje, **Suas aulas hoje** (agenda), Continuar (última aula e atalho para Estudar), Seu progresso.
- **Revisão** (`/revisao`): fila do dia com todos os cards. Os botões de matéria no topo (e a lista "Por matéria") abrem `/revisao?materia=<id>`, que revisa só os cards daquela matéria.
- **Estudar** (`/estudar`): uma carta por matéria (aulas, progresso) com o atalho do Banco de questões embaixo. `/questoes` só redireciona para cá.
- Barra de baixo: Início, Agenda, Estudar, Revisão, Desempenho. A tela "Configurações" (`/perfil`) fica na engrenagem do canto superior direito (todas as telas); para o administrador, com recados novos a engrenagem abre direto os Recados.
- Início: "Seu progresso" e as aulas de hoje são atalhos (Desempenho e a matéria da aula). Desempenho: cada tema abre o banco já filtrado e cada matéria tem "Refazer as erradas".
- Banco de questões: os filtros ficam recolhidos no botão "Filtrar"; tema e prova escolhidos ficam lembrados (cookie `mgf_<matéria>`). O botão Voltar segue `?de=` (questoes, desempenho ou `aula:<id>`).
- Aula: abas Apostila / Questões / Flashcards. Matéria: abas **Aulas | Banco de questões** (as duas telas mostram as mesmas abas; o Banco tem filtros por tema e prova).
- Questões: antes de responder, cada alternativa tem a faixa "Cortar" (tesoura; Shift + letra), que vale só enquanto o aluno está na questão. Depois de responder, certa em verde, erradas em vermelho, a marcada em destaque; comentário embaixo da certa e o motivo embaixo de cada errada. Para o administrador, cada questão tem o botão **Editar** (no canto do cartão) que abre o mesmo editor de Conteúdo ali mesmo.
- **Conversa da turma** (embaixo da questão, só depois de responder): o aluno deixa "💡 Insight para os colegas" ou "⚠️ Erro na questão"; aparece como "Augusto deixou uma dica" / "Augusto achou um erro" (sem artigo, vale para qualquer nome). Colegas marcam dica como 👍 Útil; o autor apaga o próprio recado.
- Administração (engrenagem → Configurações): **Recados da turma** (`/admin/recados`: bolinha rosa na engrenagem com os novos; marcar visto/corrigido, abrir a questão, apagar), **Alunos** (`/admin`), **Conteúdo** (`/admin/conteudo`: resumo do que está no ar, editar/apagar aulas, questões, flashcards e limpar versões antigas; `/admin/painel` só redireciona para cá), **Agenda da semana** (`/admin/agenda`: colar o cronograma do WhatsApp).

## Banco de dados

- `materias` (id curto: `nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`; `cor_inicio`/`cor_fim`, `descricao`, `ordem`)
- `aulas` (id `<materia>-a<N>`, ex.: `uro-a2`; `titulo`, `resumo`, `apostila_html`, `publicada`, `ordem`)
- `questoes` (`materia_id`, `aula_id` opcional, `ordem`, `enunciado`, `alternativas` jsonb, `correta` = índice 0–4, `comentario`, `por_que_erradas`, `tema`, `prova`, `fonte`, `origem`, `substituida_por`)
- `flashcards` (id `<aula>-fNN`, `frente`, `verso`, `ordem`)
- Progresso: `respostas` (só a última resposta de cada questão), `historico_respostas` (todas as respostas dadas: um gatilho do banco grava uma linha a cada resposta nova ou refeita; só o gatilho grava e o aluno só lê e apaga o seu; "Refazer" não apaga, só "Apagar progresso"), `revisoes`; alunos: `perfis` (`nome`, `grupo` de prática 1–29; o aluno só pode alterar `nome` e `grupo`)
- Recados: `recados` (`questao_id`, `user_id`, `autor` = primeiro nome, preenchido por gatilho; `tipo` `insight`/`erro`; `status` `novo`/`visto`/`corrigido`) e `recados_uteis`. Aluno lê todos, cria e apaga os seus; status só muda pelo admin (chave secreta).
- Agenda: `agenda_semanas` (segunda-feira da semana) e `agenda_eventos` (aulas, cancelamentos, avisos, `grupos int[]`)
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

Título, resumo e professor saem da capa (`pdftotext -f 1 -l 1`). Atualize a `descricao` da matéria com o professor. Trocar uma apostila = sobrescrever as imagens e o PDF com o mesmo número de páginas e publicar.

## Questões

- `alternativas`: lista de textos sem a letra; `correta`: índice (0 = A).
- `comentario`: aparece embaixo da alternativa certa.
- `por_que_erradas`: uma linha por letra (`B: …`, ou `A, C e E: …` para várias). Linhas sem letra viram o quadro "Sobre as alternativas".
- `origem`: `professor` (corrigida em sala), `unica`, `inferido` (alternativa reconstruída), `montada` (alternativas montadas, gabarito não oficial), `resolvida` (gabarito não oficial), `adaptada` (questão oficial alterada para seguir a aula; o comentário diz o que mudou).
- Quando a prova não tem gabarito: resolva com base na apostila da aula, marque como não oficial e **discuta as duvidosas com o Mauricio uma a uma, mostrando o texto completo da questão** antes de pedir decisão.

## Agenda

- O Mauricio cola o cronograma do WhatsApp em `/admin/agenda`; `lib/agenda.ts` separa dias, horários, matéria (emoji ou palavra), professor, local, grupos, cancelamentos (❌) e avisos. Grupos por letra (A = práticas 1 a 7…) viram números.
- Teóricas valem para todos; práticas, só para os grupos listados. O aluno informa o grupo na própria Agenda (seletor ao lado dos filtros) ou em Configurações. Tocar numa aula abre a matéria dela.

## Visual

Tema escuro **"Ouro, Cromo & Sinapse"** (`visual-v4`, no ar desde 20/10/2026), inspirado nos ícones em ouro, cromo e neurônios azuis: fundo grafite `#0B0C0F` com um holofote suave no alto e um brilho azul embaixo. Cada cor tem um só trabalho.
- **Ouro** (`#D6B15C`, botão em degradê metálico com texto escuro) = ação principal e destaque: botões principais, cartão "Revisão de hoje" (vidro azul-noite com moldura de ouro e neurônios ao fundo), aba aberta, botão Entrar.
- **Azul sinapse** `#5CB8FF` = progresso e seleção (barras, filtros ligados, alternativa marcada, links). **Cromo** = molduras finas dos cartões, barra de abas, engrenagem e letras das alternativas.
- Verde-menta `#34D399` = certo; coral `#FF6B5E` = errado (nunca rosa); âmbar = atenção; bolinha de novidade em azul `#2F6FEB`.
- Títulos na Cinzel; rótulos pequenos em maiúsculas na Inter espaçada (`.eyebrow`, `.sec`, `.review-k`…).
- Matérias em tons de pedra preciosa com moldura de cromo, como ícones de app: nefro `#2563EB`/`#1E3A8A`, pneumo `#0E7490`/`#155E75`, gastro `#047857`/`#065F46`, orto `#B45309`/`#7C2D12`, uro `#6D28D9`/`#4C1D95`, pass `#BE185D`/`#831843`. A cor clara de cada matéria (agenda, brilho do bloco) fica em `COR_MATERIA` (`lib/agenda.ts`).
Tokens e regras no fim de `app/globals.css`: bloco "Tema Med Genius" (base), "Neon com foco" (v3) e, por último, "Ouro, Cromo & Sinapse" (v4), que sobrescreve os anteriores. Ícones do app em `public/icons`, `app/icon.png`, `app/apple-icon.png`; logo em `public/brand/med-genius.webp` (ícone de neurônios em "M" com moldura dourada; o original está em `public/brand/med-genius-original.jpg`).
Tela de entrada: cartão de vidro com moldura de cromo, logo, "MED GENIUS" prateado com "Medicina · FAG" embaixo, campos de CPF e senha centralizados (ícone à esquerda, olho para mostrar a senha) e botão ENTRAR de ouro largo. Sem rodapé e sem aviso de senha esquecida.

Versões do visual salvas no GitHub (ramos fixos, não publicados; não apague):
- `visual-v1`: o tema neon anterior, como estava em 20/10/2026. Para voltar a ele: `git revert` do commit "Neon com foco" e as cores da v1 abaixo no banco.
- `visual-v4`: "Ouro, Cromo & Sinapse" (no ar). Quadro da proposta: https://claude.ai/artifact/19dnhpGriy7UQL9NA4Fn4d
- `visual-v3`: "Neon com foco" (ciano para toque, degradê neon no destaque). Para voltar a ele: `git revert` do commit "Ouro, Cromo & Sinapse" (as cores das matérias no banco são as mesmas).
- `visual-v2`: "Ouro & Sinapse" (azul-noite, vidro com filete dourado, botão principal dourado, ciano para toque, coral para erro, fonte Cinzel). Foi feito nos commits `21ce774`…`82f847c` e desfeito em `773ce11`. Para voltar a ele: `git revert 773ce11` (resolvendo conflitos com o que mudou depois) e trocar as cores das matérias no banco (`cor_inicio`/`cor_fim`): nefro `#1E4FA8`/`#14306B`, pneumo `#0F6E8C`/`#0B4560`, gastro `#11735A`/`#0A4A3C`, orto `#9A6A1F`/`#5E3F10`, uro `#5B3A9E`/`#352263`, pass `#8E2F45`/`#561B2A`. As cores da v1: nefro `#0B5BD3`/`#3B4FC9`, pneumo `#00B8F0`/`#3F6BFF`, gastro `#3EE6A8`/`#00B8F0`, orto `#FFB547`/`#FF5C8A`, uro `#6A5CFF`/`#E92FC0`, pass `#4FDDFF`/`#9B7BFF`. O quadro com a proposta: https://claude.ai/artifact/Dzu7Jr27Wc7WTo7ZMLq5G6

## Como trabalhar com o Mauricio

- Ele é sensível a custo: prefira o caminho barato (converter arquivos em vez de reescrever conteúdo; não reenviar textos grandes à toa).
- Mostre o conteúdo (a questão, a tela) antes de pedir uma decisão; um assunto por vez.
- Publique e diga em uma ou duas frases o que mudou; diga claramente o que não foi testado.
- Não deixe lixo: o que for substituído deve poder ser limpo (Conteúdo → Limpeza).

## Pendências e ideias

- Questões e flashcards das aulas novas (Pneumo 1 já tem 9 questões; as outras ainda não).
- Proteção contra senhas vazadas do Supabase está desligada (recurso do plano pago).
- Sugestões e ideias de experiência do usuário (UX): veja [`MELHORIAS-UX.md`](MELHORIAS-UX.md).
