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
todas. Ele vem do padrão das apostilas (a habilidade `apostila-padrao`, no
claude.ai), que é onde ele deve ser alterado.

## Como gerar o PDF de novo

Numa pasta de trabalho fora do repositório (os arquivos auxiliares não devem ser
commitados):

```bash
mkdir -p /tmp/gerar && cp apostilas-fonte/<aula-id>/* apostilas-fonte/apostila.css /tmp/gerar/
```

Depois, na pasta `/tmp/gerar`, prepare o ambiente e extraia `render.py` e
`checar.py` com o bloco "Ambiente" do padrão das apostilas, e rode:

```bash
python3 render.py apostila.html "Disciplina - Aula N - Professor - Tema.pdf"
```

```bash
python3 checar.py "Disciplina - Aula N - Professor - Tema.pdf" apostila.html
```

Para mudar o visual de todas de uma vez, use o `apostila.css` novo do padrão no
lugar desta cópia, gere cada apostila e refaça a paginação de cada uma (a escada
do padrão), porque mudar o CSS desloca o conteúdo das páginas.

## Como publicar depois de gerar

1. Converter as páginas em imagem, com 1400 px de largura:

```bash
pdftoppm -scale-to-x 1400 -scale-to-y -1 -jpeg -jpegopt quality=80 "<pdf novo>" /tmp/conv/p
```

2. Converter cada `p-NN.jpg` para `NN.webp` com qualidade 78 e apagar os `.jpg`.

3. Trocar os arquivos e publicar:

```bash
rm -f public/apostilas/<aula-id>/*.webp && cp /tmp/conv/*.webp public/apostilas/<aula-id>/
```

```bash
cp "<pdf novo>" public/apostilas/<aula-id>/apostila.pdf
```

```bash
git add -A public/apostilas apostilas-fonte && git commit && git push origin HEAD:main
```

4. **Se o número de páginas mudou**, atualizar o `apostila_html` da aula no banco,
   senão a última página não aparece no app. O comando está no manual do projeto.

## O que tem aqui hoje

| Pasta | Apostila | Páginas |
|---|---|---|
| `pneumo-a1` | Pneumologia · Aula 1 · Tromboembolia pulmonar | 24 |
| `pneumo-a2` | Pneumologia · Aula 2 · Pneumonia adquirida na comunidade | 19 |
| `pneumo-a3` | Pneumologia · Aula 3 · Doença pulmonar obstrutiva crônica | 21 |
| `pneumo-a4` | Pneumologia · Aula 4 · Pneumonia hospitalar | 21 |
| `angio-a1` | Angiologia · Aula 2 · Pé diabético | 26 |

As quatro estão no padrão de capítulos de 31/10/2026 (cartão com a coluna do
número em degradê) e foram conferidas: gerar o PDF a partir destes arquivos dá
exatamente o mesmo texto e o mesmo número de páginas do que está publicado.
