# Fonte da aula e arquivos de origem das apostilas

Aqui ficam, por aula, duas coisas diferentes:
- a **fonte da aula** (`fonte.md`): a transcrição e o texto dos slides, como vieram. É a base da apostila, das questões e dos flashcards, e é contra ela que tudo se confere (regra do Mauricio, 09/11/2026; seção abaixo);
- o **HTML da apostila**, que é o arquivo de onde o PDF é gerado.

## Fonte da aula (`fonte.md`)

Cada aula tem um arquivo fonte. Quando chegam a transcrição ou os slides de uma aula, a primeira coisa é guardar, **sem o modelo reescrever nada** (é trabalho mecânico):

```bash
python3 -I scripts/fonte-aula.py guardar <aula-id> --transcricao <arquivo> --slides <arquivo>
```

- Transcrição: `.txt`, `.md`, `.srt`, `.vtt`, `.docx` ou `.pdf`; aula em partes = `--transcricao` repetido. Texto colado na conversa: salve num `.txt` antes.
- Slides: `.pdf` ou `.pptx`. Entra o texto de cada página; a página que é só imagem fica marcada ("só imagem"), para quem conferir olhar o original. O arquivo original dos slides não vai para o Git (pesa): fica na pasta da aula no Drive (MEDGENIUS → `2 - Aulas`); sem acesso ao Drive, peça ao Mauricio para guardar lá.
- O que chega depois (os slides de uma aula que já tem a transcrição) entra com `--acrescentar`; material igual ao que já está é pulado. Não edite o `fonte.md` à mão: os erros da transcrição automática ficam como vieram, e quem corrige é a apostila.
- Vai para o Git no mesmo commit do trabalho da aula (na aula nova, junto com a apostila).

**Ler um pedaço** (a conferência em blocos não precisa da aula inteira):

```bash
python3 -I scripts/fonte-aula.py trecho <aula-id> --minutos 10-35 --slides 4-9
```

`--minutos` pega as falas desse intervalo (minutos, ou `1:05:00-1:20:00`), `--parte 2` só a segunda parte da transcrição, `--slides` só aquelas páginas. Os minutos de cada capítulo estão no `mapa.md` da aula.

**Como usar a fonte:**
- **Base de tudo.** A apostila sai da fonte (molde em `docs/apostila-molde.md`); as questões e os flashcards também: cobrem o que o professor ensinou e enfatizou na fonte. A apostila é o guia de ordem e páginas, corrige os termos que a transcrição automática errou e traz os complementos "Fora da aula".
- **Conferência contra a fonte.** Apostila (skill `conferir-apostila`), questões (skill `conferir-questoes` e agente `revisor`) e flashcards (skill `conferir-flashcards` e agente `revisor`) são conferidos contra a fonte.
- **Divergência:** vale a fonte, o que o professor falou (a fala manda sobre o slide). A apostila entra na lista do que corrigir; a questão ou o card segue a fonte.
- **Aula sem fonte** (as feitas antes de 09/11/2026): segue tudo pela apostila, como antes. Chegou a transcrição de uma aula antiga? Guarde do mesmo jeito.

## HTML da apostila

**Para que serve:** sem isto, mudar o visual de uma apostila obriga a remontá-la
inteira a partir do PDF (ler o texto, redesenhar as figuras, recolocar as cores),
que é caro e corre o risco de perder algum detalhe. Com o HTML guardado, uma
mudança de visual vira trocar o CSS e gerar de novo.

**Guarde aqui o HTML de toda apostila nova ou refeita.** As apostilas antigas,
feitas antes de 31/10/2026, ainda não têm o arquivo de origem: elas só existem
como PDF e imagens em `public/apostilas/`.

## O que tem em cada pasta

- `fonte.md` — a fonte da aula (acima).
- `mapa.md` — o mapa da apostila (`docs/apostila-molde.md`): capítulos ligados a páginas dos slides e minutos da fonte.
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
