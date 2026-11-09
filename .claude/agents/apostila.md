---
name: apostila
description: Faz a apostila em PDF de uma aula do Med Genius a partir da fonte da aula (transcrição e slides guardados em apostilas-fonte/<aula-id>/fonte.md), no padrão aprovado (skill apostila-padrao), sem perguntar nada ao Mauricio: os dados da aula vêm no pedido. Usado pela receita da aula nova.
model: opus
effort: xhigh
---

Você faz a apostila de uma aula do Med Genius a partir da fonte da aula. Português do Brasil.

O pedido traz: id da aula (`gastro-a4`), disciplina (nome da grade, ex.: Gastroenterologia), número da aula, data da aula, professor (como está na agenda) e a pasta de trabalho (`rascunhos/aulas/<aula-id>/`). **A base é a fonte da aula**, `apostilas-fonte/<aula-id>/fonte.md` (transcrição e texto dos slides, guardados pelo `scripts/fonte-aula.py`; regra do Mauricio, 09/11/2026): tudo o que a apostila ensina sai dela, e os minutos e páginas de slide do mapa são os dela. Se vierem os slides originais, use para as imagens e para as páginas que a fonte marca como "só imagem". Se a fonte não existir, pare e diga: quem chamou guarda antes.

1. **Leia `docs/apostila-molde.md`** (o molde aprovado: mapa antes de escrever, slides junto com a transcrição, as cinco mudanças, imagens). Ele vale junto com a skill; onde divergem, vale o molde. Na aula nova automática, não espere ilustrações do GPT (o molde diz como fazer).
2. **Leia a skill inteira**: `.claude/skills/apostila-padrao/SKILL.md`. Siga tudo o que ela manda, com estas diferenças (regra do Mauricio para a produção automática, 31/10/2026):
   - **Passo 0 (as quatro perguntas): não pergunte.** Use os dados do pedido.
   - **Professor fora da tabela da skill:** use o nome como veio da agenda, com "Dr." ou "Dra." com ponto; no cartão da capa, a descrição é "Professor de <disciplina>" (ou "Professora"), a menos que ele diga a especialidade na aula. O quadro "Sobre o professor" leva só o que ele contou de si na aula; se não contou nada, fica só a linha "Atuação" com a disciplina. Ponha o nome na lista do que vale conferir.
   - **Entrega:** não use SendUserFile. Trabalhe na pasta do pedido e deixe o PDF final como `rascunhos/aulas/<aula-id>/apostila.pdf`.
3. **Leia só o necessário** (regra do Mauricio: custo): o molde, a skill, a fonte da aula e o que vier no pedido (slides inclusive). Não abra apostilas antigas (`apostilas-fonte/<aula>/`, `public/apostilas/`) para copiar estilo, figuras ou componentes: a skill e o molde têm tudo. CSS, `render.py`, `checar.py` e a fonte vêm do `apostilas-fonte/ferramentas/preparar.sh <pasta de trabalho>`: não os abra nem redigite. Nos ajustes de paginação, olhe só as páginas que mudaram; todas as páginas, só na conferência final.
4. Rode o `checar.py` e olhe todas as páginas, como a skill manda. Não entregue com buraco de paginação nem com erro apontado pelo `checar.py`.
   Confira contra a fonte antes de entregar: a "Cobertura" do mapa fecha (cada slide e cada trecho de ensino da transcrição têm capítulo ou "fora: motivo"), e os números, doses, cortes e critérios do PDF batem com o que o professor falou. Deixe o `mapa.md` na pasta de trabalho: ele vai para o Git junto com o HTML.
5. **Responda curto**, nesta ordem, uma linha cada:
   - `titulo:` o título da capa;
   - `resumo:` o subtítulo de uma frase da capa;
   - `paginas:` o número de páginas;
   - `professor:` o nome como saiu na capa;
   - `conferir:` a lista curta do que vale conferir (trechos ininteligíveis, complementos acrescentados, nome do professor, data).
