# Arquivos de origem das apostilas

Aqui fica o HTML de cada apostila, que é o arquivo de onde o PDF é gerado.

**Para que serve:** sem isto, mudar o visual de uma apostila obriga a remontá-la
inteira a partir do PDF (ler o texto, redesenhar as figuras, recolocar as cores),
que é caro e corre o risco de perder algum detalhe. Com o HTML guardado, uma
mudança de visual vira trocar o CSS e gerar de novo.

**Guarde aqui o HTML de toda apostila nova ou refeita.** As apostilas antigas,
feitas antes de 31/10/2026, ainda não têm o arquivo de origem: elas só existem
como PDF e imagens em `public/apostilas/`.

## O que tem em cada pasta

- `apostila.html` — o arquivo da apostila, exatamente como gerou o PDF que está
  no ar. Não edite para "arrumar": qualquer mudança aqui só vale depois de gerar
  o PDF de novo e publicar.
- `*.svg` — as figuras.
- `figuras.py`, `figlib.py`, `fig_decisao.py` — os programas que desenham as
  figuras, para quando for preciso mudar uma.

`apostila.css` fica na raiz desta pasta, numa cópia só, porque é o mesmo para
todas. **É o CSS oficial** e não muda à toa, para as apostilas antigas saírem
iguais se forem geradas de novo: estilos novos vão num `<style>` no próprio
`apostila.html` (ver `docs/apostila-molde.md`).

As ferramentas de gerar e conferir o PDF ficam em `ferramentas/` (desde 04/11/2026),
iguais para Claude, Antigravity e Codex: `render.py`, `checar.py`, a fonte Inter
(`fonts/`, com a licença) e o `preparar.sh`, que instala o que falta e copia tudo
para a pasta de trabalho. Nunca redigite esses arquivos: copie com o `preparar.sh`.

## Como gerar o PDF de novo

Numa pasta de trabalho fora do repositório (os arquivos auxiliares não devem ser
commitados):

```bash
apostilas-fonte/ferramentas/preparar.sh /tmp/gerar && cp -r apostilas-fonte/<aula-id>/* /tmp/gerar/
```

Depois, na pasta `/tmp/gerar`:

```bash
python3 render.py apostila.html "Disciplina - Aula N - Professor - Tema.pdf"
```

```bash
python3 checar.py "Disciplina - Aula N - Professor - Tema.pdf" apostila.html
```

Para mudar o visual de todas de uma vez, mude o `apostila.css` desta pasta,
gere cada apostila e refaça a paginação de cada uma (a escada da skill
`apostila-padrao`), porque mudar o CSS desloca o conteúdo das páginas.

## Como publicar depois de gerar

`scripts/publicar-apostila.sh "<pdf novo>" <aula-id>` troca as imagens e o PDF em
`public/apostilas/<aula-id>/` e mostra o número de páginas. Antes, apague as
imagens antigas (`rm -f public/apostilas/<aula-id>/*.webp`). Depois, commit e
publicação como manda a skill `subir-apostila`. **Se o número de páginas mudou**,
refaça o `apostila_html` da aula no banco (comando na skill `subir-apostila`),
senão a última página não aparece no app.

## O que tem aqui hoje

| Pasta | Apostila | Páginas |
|---|---|---|
| `pneumo-a1` | Pneumologia · Aula 1 · Tromboembolia pulmonar | 24 |
| `pneumo-a2` | Pneumologia · Aula 2 · Pneumonia adquirida na comunidade | 19 |
| `pneumo-a3` | Pneumologia · Aula 3 · Doença pulmonar obstrutiva crônica | 21 |
| `pneumo-a4` | Pneumologia · Aula 4 · Pneumonia hospitalar | 21 |
| `pneumo-a5` | Pneumologia · Aula 5 · Doenças da pleura | 27 |
| `pneumo-a6` | Pneumologia · Aula 6 · Tabagismo | 16 |
| `angio-a1` | Angiologia · Aula 2 · Pé diabético | 26 |
| `nefro-a10` | Nefrologia · Aula 10 · Doença renal crônica | 22 |

As de Pneumologia 1 a 4 e a de Angiologia estão no padrão de capítulos de 31/10/2026 (cartão com a coluna do
número em degradê) e foram conferidas: gerar o PDF a partir destes arquivos dá
exatamente o mesmo texto e o mesmo número de páginas do que está publicado.
