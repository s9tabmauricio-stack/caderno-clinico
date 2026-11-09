---
name: conferir-apostila
description: Use quando o Mauricio pedir para conferir, verificar ou revisar a apostila de uma aula do Med Genius contra a fonte da aula, a transcrição e os slides guardados (ex.: "confere a apostila da Pneumo 7"). Acha o que está errado, o que falta e as marcas PROVA fora do lugar; corrige o HTML e publica só depois do "pode".
---

# Conferir a apostila de uma aula contra a fonte

Regra do Mauricio (09/11/2026): cada aula tem um arquivo fonte (`apostilas-fonte/<aula-id>/fonte.md`, a transcrição e o texto dos slides, como vieram), e a apostila é conferida contra ele. **A fonte manda:** onde a apostila diz outra coisa, a apostila está errada. Entre fala e slide, vale a fala (`docs/apostila-molde.md`).

Para conferir as questões ou os flashcards, use `conferir-questoes` ou `conferir-flashcards`.

## 1. Preparar (quem coordena, sem agente)

1. **Fila**: anote "Conferir a apostila da `<aula-id>`" em `docs/fila.md` (regras no topo do arquivo).
2. **Fonte**: `apostilas-fonte/<aula-id>/fonte.md`. Se não existir (aulas antigas), pare e diga ao Mauricio que a aula não tem fonte: se ele mandar a transcrição ou os slides, guarde com `python3 -I scripts/fonte-aula.py guardar <aula-id> …` ([`apostilas-fonte/README.md`](../../../apostilas-fonte/README.md)) e siga.
3. **Texto da apostila**: `python3 -I scripts/apostila-texto.py public/apostilas/<aula-id>/apostila.pdf > <scratchpad>/<aula-id>-apostila.txt`.
4. **Um conferente ou blocos**: fonte com até uns 15 mil palavras (`wc -w`), um conferente só, com a fonte e a apostila inteiras. Maior que isso e com `mapa.md`: 2 ou 3 blocos de capítulos inteiros, cada um com as suas páginas (`apostila-texto.py --paginas`) e o seu trecho da fonte, com 3 minutos de folga para cada lado (`python3 -I scripts/fonte-aula.py trecho <aula-id> --minutos 12-41 --slides 6-15`).

## 2. Conferir

Abra o conferente (ou os blocos, na mesma mensagem) com a ferramenta Agent, `model: opus`, `effort: xhigh`, com este pedido:

> Confira a apostila `<aula-id>` contra a fonte da aula. Siga a seção "2. Conferir" de `.claude/skills/conferir-apostila/SKILL.md`. Fonte: `<arquivo da fonte ou do trecho>`. Apostila: `<arquivo>`, páginas `<páginas>`.

**Antigravity e Codex**: façam os blocos um depois do outro, seguindo esta seção.

O conferente lê uma vez a fonte e a apostila (o seu pedaço) e procura só o que tem problema:
1. **Errado**: número, dose, corte, critério, nome, conduta ou sequência que diverge do que o professor falou (ou do slide, quando a fala não diz). A apostila que seguiu o slide contra a fala está errada.
2. **Faltando**: o que o professor ensinou e não está na apostila, e slide com conteúdo sem lugar nela. Não conta: piada, conversa fora do assunto e o que ele disse que tirou da aula.
3. **PROVA fora do lugar**: ponto que o professor enfatizou sem o selo (sinais em "Marca PROVA" do `docs/apostila-molde.md`), ou selo PROVA sem nenhum sinal na fonte.
4. **Roxo trocado**: conteúdo que não está na fonte e aparece como aula (sem a caixa roxa de complemento), ou conteúdo da fonte posto como complemento.
5. **Tirado da aula**: o que ele disse que não cobra ou que tirou da aula aparecendo como conteúdo.
6. **Citação**: fala entre aspas atribuída ao professor que não está na fonte.

Não é problema: termo médico que a transcrição automática errou e a apostila corrigiu; ordem diferente da fala, quando o capítulo junta o assunto. Trecho ininteligível na fonte: não decide, lista como "conferir com o Mauricio".

**Responde curto, só com problemas** (nada de listar o que está certo), e não muda nada:

| Página | Tipo | Problema | Fonte (minuto ou slide e trecho curto) | Proposta |
|---|---|---|---|---|
| p. 7 | errado | apostila diz corte de 500; o professor falou 400 | 32:15: "…" | trocar 500 por 400 no quadro "…" |

Depois da tabela, uma linha: "Páginas X–Y: N problemas."

## 3. Mostrar ao Mauricio

Junte as tabelas na ordem das páginas, com o resumo numa linha ("Pneumo 7: 22 páginas, 3 erros, 2 faltando, 1 PROVA fora do lugar"). Mostre cada problema com o trecho da fonte e a proposta e espere o "pode". Pode mostrar todos de uma vez quando forem curtos; se ele pedir, um por vez.

## 4. Corrigir (só depois do "pode")

1. **HTML**: `apostilas-fonte/<aula-id>/apostila.html`. Apostila antiga sem HTML: a correção pede remontá-la; diga ao Mauricio e ofereça refazer a apostila pela fonte (agente `apostila`).
2. **Gerar de novo** numa pasta de trabalho (`apostilas-fonte/ferramentas/preparar.sh`, como em [`apostilas-fonte/README.md`](../../../apostilas-fonte/README.md)): mude o HTML, `render.py`, feche os buracos da paginação (escada da skill `apostila-padrao`), `checar.py` e olhe as páginas que mudaram.
3. **Publicar**: `scripts/publicar-apostila.sh` ("Como publicar depois de gerar" no README; se o número de páginas mudou, refaça o `apostila_html` da aula). Commit do `apostila.html` e de `public/apostilas/<aula-id>/` e PR, como em `docs/publicar.md`.
4. **Questões e flashcards** que repetem o erro: procure no banco pelo termo do ponto corrigido (`select id, frente, verso from public.flashcards where aula_id = '<aula-id>' and (frente ilike '%<termo>%' or verso ilike '%<termo>%');` e o mesmo em `questoes`, com `substituida_por is null`) e corrija pelo caminho de sempre (seção 4 da `conferir-flashcards`; versão `-v2` da questão, como no manual).
5. Apague os arquivos temporários e tire a linha da fila no PR.
