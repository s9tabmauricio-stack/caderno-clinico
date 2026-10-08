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
- React 19, `@supabase/ssr` com chave publicável (`lib/supabase/config.ts`), fonte Inter.
- Leitura de dados: `lib/dados.ts`; agenda: `lib/agenda.ts` (leitor do cronograma) e `lib/agenda-dados.ts`; admin: `lib/admin.ts`.
- Repetição espaçada: `lib/srs.ts`. Explicação por alternativa: `lib/explicacoes.ts`.

## Login

- CPF + senha. O Supabase exige e-mail, então cada CPF vira o e-mail interno `CPF@caderno-clinico.vercel.app`
  (`DOMINIO_LOGIN` em `lib/cpf.ts`). **Nunca mude esse domínio**: as contas existentes dependem dele (é só um identificador, não o endereço do site).
- Contas são criadas pelo administrador em Perfil → Alunos (`/admin`). Cadastro aberto deve ficar desligado no Supabase.
- Nunca digite senhas ou chaves em sites; quem cria contas e configura chaves é o Mauricio.

## Telas

- Início: saudação (só o primeiro nome), Revisão de hoje, **Suas aulas hoje** (agenda), Matérias, Seu progresso.
- Barra de baixo: Início, Agenda, Revisão, Desempenho. Perfil fica na engrenagem do canto superior direito (todas as telas).
- Aula: abas Apostila / Questões / Flashcards. Matéria: aulas + Banco de questões (filtros por tema e prova).
- Questões: antes de responder, cada alternativa tem a faixa "Cortar" (tesoura; Shift + letra), que vale só enquanto o aluno está na questão. Depois de responder, certa em verde, erradas em vermelho, a marcada em destaque; comentário embaixo da certa e o motivo embaixo de cada errada. Para o administrador, cada questão tem o botão **Editar** (no canto do cartão) que abre o mesmo editor de Conteúdo ali mesmo.
- **Conversa da turma** (embaixo da questão, só depois de responder): o aluno deixa "💡 Insight para os colegas" ou "⚠️ Erro na questão"; aparece como "Augusto deixou uma dica" / "Augusto achou um erro" (sem artigo, vale para qualquer nome). Colegas marcam dica como 👍 Útil; o autor apaga o próprio recado.
- Administração (engrenagem → Perfil): **Recados da turma** (`/admin/recados`: bolinha rosa na engrenagem com os novos; marcar visto/corrigido, abrir a questão, apagar), **Alunos** (`/admin`), **Conteúdo** (`/admin/conteudo`: editar/apagar aulas, questões, flashcards e limpar versões antigas), **Agenda da semana** (`/admin/agenda`: colar o cronograma do WhatsApp).

## Banco de dados

- `materias` (id curto: `nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`; `cor_inicio`/`cor_fim`, `descricao`, `ordem`)
- `aulas` (id `<materia>-a<N>`, ex.: `uro-a2`; `titulo`, `resumo`, `apostila_html`, `publicada`, `ordem`)
- `questoes` (`materia_id`, `aula_id` opcional, `ordem`, `enunciado`, `alternativas` jsonb, `correta` = índice 0–4, `comentario`, `por_que_erradas`, `tema`, `prova`, `fonte`, `origem`, `substituida_por`)
- `flashcards` (id `<aula>-fNN`, `frente`, `verso`, `ordem`)
- Progresso: `respostas`, `revisoes`; alunos: `perfis` (`nome`, `grupo` de prática 1–29; o aluno só pode alterar `nome` e `grupo`)
- Recados: `recados` (`questao_id`, `user_id`, `autor` = primeiro nome, preenchido por gatilho; `tipo` `insight`/`erro`; `status` `novo`/`visto`/`corrigido`) e `recados_uteis`. Aluno lê todos, cria e apaga os seus; status só muda pelo admin (chave secreta).
- Agenda: `agenda_semanas` (segunda-feira da semana) e `agenda_eventos` (aulas, cancelamentos, avisos, `grupos int[]`)
- Visões usadas pelas telas: `questoes_do_aluno`, `progresso_aulas`, `progresso_materias`, `progresso_temas`, `flashcards_do_aluno`.
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
- `origem`: `professor` (corrigida em sala), `unica`, `inferido` (alternativa reconstruída), `montada` (alternativas montadas, gabarito não oficial), `resolvida` (gabarito não oficial).
- Quando a prova não tem gabarito: resolva com base na apostila da aula, marque como não oficial e **discuta as duvidosas com o Mauricio uma a uma, mostrando o texto completo da questão** antes de pedir decisão.

## Agenda

- O Mauricio cola o cronograma do WhatsApp em `/admin/agenda`; `lib/agenda.ts` separa dias, horários, matéria (emoji ou palavra), professor, local, grupos, cancelamentos (❌) e avisos. Grupos por letra (A = práticas 1 a 7…) viram números.
- Teóricas valem para todos; práticas, só para os grupos listados. O aluno informa o grupo no Perfil.

## Visual

Tema escuro "vidro sobre luzes neon", inspirado no ícone (neurônio de vidro em ciano, violeta e magenta).
Tokens e regras no fim de `app/globals.css` (bloco "Tema Med Genius"). Ícones do app em `public/icons`, `app/icon.png`, `app/apple-icon.png`; logo em `public/brand/med-genius.svg`.
Rodapé da tela de entrada: "By Mauricio".

## Como trabalhar com o Mauricio

- Ele é sensível a custo: prefira o caminho barato (converter arquivos em vez de reescrever conteúdo; não reenviar textos grandes à toa).
- Mostre o conteúdo (a questão, a tela) antes de pedir uma decisão; um assunto por vez.
- Publique e diga em uma ou duas frases o que mudou; diga claramente o que não foi testado.
- Não deixe lixo: o que for substituído deve poder ser limpo (Conteúdo → Limpeza).

## Pendências e ideias

- Questões e flashcards das aulas novas (Pneumo 1 já tem 9 questões; as outras ainda não).
- Proteção contra senhas vazadas do Supabase está desligada (recurso do plano pago).
