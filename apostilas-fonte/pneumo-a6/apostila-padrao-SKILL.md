---
name: "apostila-padrao"
description: "Use ao criar ou refazer qualquer apostila de estudo em PDF (a partir de transcrição, slides ou resumo de aula): aplica o visual iOS 27 / Liquid Glass e as regras de escrita e de diagramação aprovadas."
---

# Apostila no padrão aprovado (iOS 27 / Liquid Glass, fonte Inter)

Padrão aprovado pelo Mauricio nas apostilas de Nefrologia e de Urologia. Toda apostila nova segue este documento: mesma estrutura, mesmas cores com o mesmo significado, mesmos componentes, mesmo CSS. Saída: PDF A4 gerado com WeasyPrint a partir de HTML + CSS.

O visual antigo (guia clínico em Poppins e azul-petróleo) foi substituído pelo Liquid Glass. Só volte a ele se o Mauricio pedir na conversa.

## Fluxo de trabalho

0. **Antes de qualquer coisa, perguntar ao Mauricio** — sempre, mesmo que a fonte pareça dizer — e só começar depois da resposta:
   - **Número da aula** (ex.: Aula 3);
   - **Dia da aula** (data);
   - **Professor** (da tabela da seção "Professores", ou outro);
   - **Matéria** (disciplina da tabela da seção "Disciplina").

   Fazer as quatro perguntas de uma vez, numa mensagem só (com AskUserQuestion, se disponível). Pode oferecer como opção o que a fonte sugere (por exemplo, o professor pelas pistas da fala), mas quem decide é a resposta. O que ele responder vale acima da fonte. Se ele não souber algum item, seguir sem ele e pôr na lista do que vale conferir.
1. **Ler a fonte inteira** (transcrição, slides ou resumo). Anotar: temas, valores numéricos, doses, falas marcantes do professor, avisos da disciplina (data de prova, nota, presença), o que ele disse que cobra e o que disse que não cobra, perguntas de alunos, casos contados em aula.
2. **Corrigir os erros da transcrição automática** (termos médicos trocados, nomes). Não perder nenhum conteúdo da aula. Limpar palavrão e piada longa, preservando o conteúdo clínico e as falas que valem como citação.
3. **Planejar as seções**: 00 Recados (só se houver avisos), 01 a N por tema, e a última seção "O essencial da aula".
4. **Preparar o ambiente** com o bloco da seção "Ambiente": instala o que falta, confere a fonte Inter e extrai desta skill os arquivos `apostila.css`, `render.py` e `checar.py`. **Nunca redigitar esses três arquivos**: o bloco copia o texto exato.
5. **Escrever o HTML** a partir do esqueleto e dos componentes desta skill. O texto do rodapé vai no `<meta name="rodape">`; o CSS não se edita.
6. **Desenhar as figuras** quando o tema pedir (régua, algoritmo, linha do tempo, cascata, mapa).
7. **Gerar o PDF** com `python3 render.py apostila.html "Disciplina - Aula N - Professor - Tema.pdf"`. Ele faz as duas passagens (números de página do sumário + área de anotações na última página) e já mostra o espaço livre no pé de cada página.
8. **Fechar os buracos da paginação** com a escada da seção "Paginação", rodando o `render.py` de novo depois de cada ajuste — é onde mora a maior parte do trabalho.
9. **Conferir** com `python3 checar.py "Disciplina - Aula N - Professor - Tema.pdf" apostila.html`, olhar **todas** as imagens da pasta `paginas/` e passar a lista de checagem. Entregar o PDF com SendUserFile. Na resposta: uma linha sobre o que saiu e a lista curta do que vale conferir (complementos acrescentados, trechos ininteligíveis da transcrição, nome do professor).

## Regras de escrita

- Português do Brasil, linguagem simples. **Sem siglas nem abreviações**: escrever por extenso ("taxa de filtração glomerular", "infecções sexualmente transmissíveis", "vírus da imunodeficiência humana"). Unidades de medida são permitidas (mL, mg/dL, kg, g). Nome de exame que só existe como sigla (VDRL, FTA-Abs) pode ficar, mas explique na primeira aparição e registre no glossário.
- **"Dr." e "Dra." sempre com ponto**, padronizados, mesmo que a fonte seja inconsistente.
- Números no formato brasileiro: 2.100; 1,2; 10h30.
- **Negrito com parcimônia**: no máximo um trecho por parágrafo. Em listas, negrito só no termo inicial do item.
- **Complemento**: tudo o que não foi dito em aula vai só em caixa roxa "Complemento: fora da aula" (ou no valor de referência roxo). Nunca misturar com o conteúdo da aula.
- **Marca PROVA**: só em blocos específicos (um título de subseção, um quadro), nunca na seção inteira, e só onde a fonte diz que cai ou que ele cobra. Se a fonte não diz, não marcar.
- Falas marcantes do professor viram citação (laranja), com atribuição curta.
- Glossário "Palavras da aula em linguagem simples" em **ordem alfabética**.
- **Não incluir banco de questões nem flashcards** na apostila.
- Títulos nunca em preto quase puro: use os azuis do CSS.
- Conferir o dia da semana de qualquer data citada (o `checar.py` lista cada data com o dia certo).

## Disciplina: sempre o nome da grade, nunca o da subespecialidade

A apostila leva o nome da **disciplina** da grade do Mauricio, nunca o da especialidade do professor nem o do tema da aula. Exemplo: aula de reto e canal anal dada por coloproctologista sai como **Gastroenterologia**, não "Coloproctologia".

Disciplinas do bimestre atual (a partir de outubro de 2026):

| Disciplina (escrever assim) | Áreas que entram nela (exemplos) |
|---|---|
| Nefrologia | doença renal, diálise, transplante renal, água, eletrólitos e equilíbrio ácido-base |
| Angiologia | cirurgia vascular, flebologia (varizes, trombose venosa), linfologia, doença arterial periférica |
| Urologia | andrologia, uro-oncologia, urologia pediátrica, endourologia |
| Pneumologia | tisiologia (tuberculose), cirurgia torácica, função pulmonar |
| Gastroenterologia | coloproctologia, hepatologia, cirurgia do aparelho digestivo, endoscopia digestiva |
| Ortopedia | traumatologia, coluna, cirurgia da mão, ortopedia pediátrica, medicina esportiva |
| Seminário Integrador V | — |
| PROEX: Programa de Aprendizagem Saúde e Sociedade V | — |

- O nome da disciplina, escrito como na primeira coluna, vai na linha pequena da capa ("Gastroenterologia · Aula 3 · Reto e canal anal"), no rodapé ("Mauricio Faria · Gastroenterologia · Aula 3 — título curto") e no começo do nome do arquivo PDF. O nome do arquivo segue sempre o modelo "Disciplina - Aula N - Professor - Tema.pdf", com o professor na forma curta da tabela da seção "Professores" (ex.: "Gastroenterologia - Aula 3 - Dr. Sagae - Reto e canal anal.pdf"). O código de turma (T01, T01 PA) não entra.
- A subespecialidade só pode aparecer na descrição do professor, no cartão da capa (ex.: "Coloproctologista").
- PROEX é o nome oficial da disciplina e pode ficar como sigla. No rodapé, se a linha não couber, use "PROEX V".
- **Temas de fronteira** (cálculo renal, infecção urinária, hematúria — podem ser de Nefrologia ou de Urologia; trombose e doença arterial podem aparecer em outras aulas): vale a disciplina em que a aula foi dada, indicada na fonte ou pelo Mauricio. Não deduzir só pelo tema. A disciplina vem da resposta do passo 0 do fluxo.
- Quando o Mauricio mandar a lista de um novo bimestre, ela substitui esta tabela.

## Professores: nome e cartão da capa

O cartão da capa e a atribuição das citações usam o nome e a descrição desta tabela. Sempre "Dr." ou "Dra." com ponto.

| Disciplina | Professor (escrever assim) | Forma curta (citações) | Cartão da capa (descrição) | Inicial |
|---|---|---|---|---|
| Gastroenterologia | Dr. Univaldo Etsuo Sagae | Dr. Sagae | Coloproctologista e cirurgião do aparelho digestivo | S |
| Gastroenterologia | Dr. Gustavo Kurachi | Dr. Kurachi | Coloproctologista e endoscopista | K |

Temas e pistas de cada professor (servem para confirmar quem deu a aula):

- **Dr. Univaldo Etsuo Sagae (Gastroenterologia).** Temas: coloproctologia e doenças anais (hemorroida, fissura, abscesso, fístula), constipação e incontinência, câncer do aparelho digestivo, cirurgia do cólon e do reto, doenças do fígado, esôfago, estômago, duodeno, vesícula biliar, pâncreas e vias biliares, cirurgia minimamente invasiva e robótica, endometriose intestinal. Pistas na fala: Gastroclínica Cascavel (fundador e diretor), Hospital Gênesis, residência e mestrado na Universidade de São Paulo, técnica COPE (cirurgia conservadora do reto na endometriose, pela vagina), cirurgias NOTES e NOSES, núcleo dos ostomizados do oeste do Paraná. Também é professor da Universidade Estadual do Oeste do Paraná e preceptor de residência de cirurgia geral.
- **Dr. Gustavo Kurachi (Gastroenterologia).** Temas: doenças do intestino e do ânus, doença inflamatória intestinal (doença de Crohn e retocolite ulcerativa), distúrbios do assoalho pélvico, endoscopia digestiva alta e baixa, diagnóstica e terapêutica. Pistas na fala: graduação na Universidade Estadual de Londrina, residência em coloproctologia na Universidade Federal de Goiás, residência em cirurgia geral no Hospital Governador Celso Ramos, grupo de estudos de doença inflamatória intestinal, Sociedade Brasileira de Endoscopia Digestiva. Professor de cirurgia e gastroenterologia da FAG.

Regras:

- O professor vem da resposta do passo 0 do fluxo. As pistas servem só para sugerir uma opção na pergunta; o tema sozinho não basta, porque os dois professores de Gastroenterologia dão doenças anais e assoalho pélvico.
- Se o Mauricio não souber quem deu a aula, o cartão fica "Professor de [disciplina]" com a subespecialidade na descrição, e o nome entra na lista do que vale conferir.
- No cartão da capa: `<span class="av">S</span><div><b>Dr. Univaldo Etsuo Sagae</b><span>Coloproctologista e cirurgião do aparelho digestivo</span></div>` (ou a linha do professor certo da tabela). Nas citações e nos parênteses: a forma curta ("Dr. Sagae, sobre ...").
- **Quadro "Sobre o professor"** (obrigatório): na página 2, logo depois da legenda e antes da seção 00 ou 01, com o currículo do professor que deu a aula, copiado do bloco abaixo. Sem números de registro (CRM, RQE) e sem siglas: nomes de instituições e sociedades por extenso. O cartão da capa continua só com o nome, a descrição curta e a data.
- Quando o Mauricio mandar novos professores, acrescentar uma linha na tabela, um item de temas e pistas e o bloco do currículo.

Currículo de cada professor (HTML pronto para o quadro "Sobre o professor"):

```html
<!-- Dr. Gustavo Kurachi -->
<div class="prof"><div class="kick">Sobre o professor · Dr. Gustavo Kurachi</div>
<div class="rows">
  <div class="row"><div class="k">Especialidades</div><div class="v">Coloproctologia, cirurgia geral e endoscopia digestiva.</div></div>
  <div class="row"><div class="k">Atuação</div><div class="v">Doenças do intestino e do ânus; doença inflamatória intestinal (doença de Crohn e retocolite ulcerativa); distúrbios do assoalho pélvico; endoscopia digestiva alta e baixa, diagnóstica e terapêutica.</div></div>
  <div class="row"><div class="k">Formação</div><div class="v">Graduação pela Universidade Estadual de Londrina. Residência em cirurgia geral no Hospital Governador Celso Ramos e em coloproctologia na Universidade Federal de Goiás.</div></div>
  <div class="row"><div class="k">Sociedades</div><div class="v">Membro titular da Sociedade Brasileira de Coloproctologia, do Grupo de Estudos de Doença Inflamatória Intestinal do Brasil e da Sociedade Brasileira de Endoscopia Digestiva.</div></div>
  <div class="row"><div class="k">Docência</div><div class="v">Professor de cirurgia e gastroenterologia do Centro Universitário Fundação Assis Gurgacz.</div></div>
</div></div>

<!-- Dr. Univaldo Etsuo Sagae -->
<div class="prof"><div class="kick">Sobre o professor · Dr. Univaldo Etsuo Sagae</div>
<div class="rows">
  <div class="row"><div class="k">Especialidades</div><div class="v">Coloproctologia, cirurgia do aparelho digestivo, cirurgia geral e videolaparoscopia.</div></div>
  <div class="row"><div class="k">Atuação</div><div class="v">Câncer do aparelho digestivo; doenças do fígado, esôfago, estômago, duodeno, vesícula biliar, pâncreas e vias biliares; cirurgia avançada do cólon e do reto, laparoscópica e por orifícios naturais; cirurgia minimamente invasiva e robótica; endometriose intestinal; doenças anais.</div></div>
  <div class="row"><div class="k">Formação</div><div class="v">Mestrado pela Faculdade de Medicina da Universidade de São Paulo. Residência em cirurgia geral e em cirurgia do aparelho digestivo na Universidade de São Paulo. Treinamento em cirurgia robótica e em preservação de nervos. Pós-graduação em pesquisa e prática clínica pela Universidade de Harvard.</div></div>
  <div class="row"><div class="k">Sociedades</div><div class="v">Titular do Colégio Brasileiro de Cirurgiões, da Sociedade Brasileira de Coloproctologia e do Colégio Brasileiro de Cirurgia Digestiva. Presidente da Sociedade Paranaense de Coloproctologia (gestão 2018-2019).</div></div>
  <div class="row"><div class="k">Docência</div><div class="v">Professor de medicina da Universidade Estadual do Oeste do Paraná e do Centro Universitário Fundação Assis Gurgacz. Preceptor da residência de cirurgia geral do Hospital Universitário e do Hospital São Lucas.</div></div>
  <div class="row"><div class="k">Destaques</div><div class="v">Fundador e diretor-geral da Gastroclínica Cascavel e diretor técnico do Hospital Gênesis. Criador da técnica COPE, cirurgia conservadora do reto na endometriose pelo acesso vaginal. Pioneiro em cirurgia laparoscópica e nas cirurgias por orifícios naturais. Fundador do Núcleo Regional dos Ostomizados do Oeste do Paraná.</div></div>
</div></div>
```

## Cores: significado fixo (legenda na página 2)

| Cor | Uso | Fundo / borda / texto |
|---|---|---|
| Azul | conteúdo da aula e raciocínio (padrão de caixas e cartões) | #E8F0FE / #C3D8F8 / #0B5BD3 |
| Verde | **só** dose ou valor de referência | #E7F7EC / #BFE5CB / #1E7A34 |
| Vermelho | **só** alerta, erro comum ou armadilha | #FDECEB / #F8C9C5 / #C0362C |
| Laranja | **só** fala ou parêntese do professor | #FFF3E1 / #F7DCAE / #9A5B00 |
| Roxo | **só** complemento que não foi dito em aula | #F4EBFB / #DEC7F1 / #6E3AA7 |
| Marca PROVA | o ponto exato que cai na prova | fundo #1F2933, texto branco |

Cartões comuns são sempre brancos com borda cinza, mesmo lado a lado. Os passos de um fluxo são todos da mesma cor. Texto do corpo #3A3A3C; negrito #1F2933; texto secundário #6C6C70 (nunca mais claro que isso para texto de leitura); títulos #16315C e subtítulos #0B5BD3.

## Estrutura do documento

1. **Capa** (degradê azul → roxo, página inteira, painéis de vidro): linha pequena "Disciplina · Aula N · Tema" (disciplina e número da aula como respondidos no passo 0); título; subtítulo de uma frase; cartão do professor com a inicial (nome e descrição pela tabela da seção "Professores"; na segunda linha do cartão, depois da descrição, a data: "Coloproctologista · 30 de setembro de 2026"); **"Três números para levar"** (se a aula não tiver números, três ideias-chave curtas); **sumário "Nesta apostila"** com número, título e página (clicável); nota de origem.
2. **Página 2**: legenda "Como ler esta apostila" (2 colunas, 6 itens), o quadro "Sobre o professor" com o currículo (seção "Professores") e, em seguida, a seção 00 ou 01.
3. **00 Recados da disciplina** (se houver): cartão de data da prova, linhas rótulo/texto (Nota, Presença, Na prova, Perguntas, Slides, Gravação...), caixa "O que cobra e o que não cobra", citação.
4. **Seções 01 a N**: cabeçalho numerado + chips de tema (nada de "Cai na prova" como chip), texto, subtítulos (h3), componentes.
5. **Última seção "O essencial da aula"**: Números da aula, A aula em uma linha por tema, figura de síntese quando couber, Erros comuns, Glossário alfabético, área de Anotações preenchendo a última página.

**Rodapé** em todas as páginas, menos a capa: à esquerda **"Mauricio Faria · Disciplina · Aula N — título curto"** (o nome Mauricio Faria vem sempre primeiro e é fixo em toda apostila; a disciplina é a da tabela); à direita o número da página. O texto vai no `<meta name="rodape">` do esqueleto; o `render.py` aplica em todas as páginas e tira da capa.

O texto corre direto entre as seções: **não** force quebra de página em nenhuma seção. A seção final só começa em página nova se isso não deixar meia página vazia antes.

## Componentes (HTML)

Esqueleto do arquivo `apostila.html` (na mesma pasta do `apostila.css`):

```html
<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<title>Gastroenterologia · Aula 3 · Reto e canal anal</title>
<meta name="rodape" content="Mauricio Faria · Gastroenterologia · Aula 3 — Reto e canal anal">
<link rel="stylesheet" href="apostila.css">
</head><body>
<div class="cover">...</div>      <!-- capa (modelo mais abaixo) -->
<div class="legend">...</div>     <!-- legenda -->
<div class="prof">...</div>       <!-- sobre o professor -->
<section id="s00">...</section>   <!-- recados, só se houver -->
<section id="s01">...</section>
<section id="s07">... {{NOTAS}}</section>   <!-- última: O essencial da aula -->
</body></html>
```

```html
<!-- cabeçalho de seção -->
<section id="s01">
  <div class="sec-head"><span class="num">01</span><h2>Título da seção</h2></div>
  <div class="chips"><span class="chip">Tema</span></div>

<!-- subtítulo com marca de prova (data-bm = título limpo para o marcador do PDF) -->
<h3 data-bm="O caminho da ureia">O caminho da ureia <span class="prova">PROVA</span></h3>

<!-- caixas: .box (azul) | .box.purple | .box.orange | .box.red — o ponto colorido vem no kicker -->
<div class="box"><div class="kick"><span class="dot"></span>Guarde para a próxima aula</div><p>...</p></div>
<div class="box purple"><div class="kick"><span class="dot"></span>Complemento: fora da aula</div><p>...</p></div>
<div class="box orange"><div class="kick"><span class="dot"></span>Parêntese do professor</div><p>...</p></div>
<div class="box red"><div class="kick"><span class="dot"></span>Erros comuns</div><ul><li><span class="medium">Achar que X.</span> Correção.</li></ul></div>

<!-- citação -->
<div class="quote"><p>“Frase.”</p><div class="who">Dr. Nome, sobre o contexto</div></div>

<!-- cartões: .grid2 / .grid3 com .card; .card.wide ocupa a largura toda; lista em 2 colunas: .card.wide + ul.cols2 -->
<div class="grid2"><div class="card"><span class="tag">Rótulo</span><h4>Título</h4><p>...</p></div>...</div>

<!-- dose ou valor de referência (verde); .ref.purple quando o valor não foi dado em aula -->
<div class="ref">
  <div class="txt"><div class="kick"><span class="dot"></span>Sífilis recente</div><p>Explicação curta.</p></div>
  <div class="val">2,4 milhões<small>unidades, dose única</small></div>
</div>
<!-- dois valores: <div class="vals"><div class="val"><small>Clamídia</small>Azitromicina 1 g</div><div class="val"><small>Gonococo</small>Ciprofloxacino 500 mg</div></div> -->

<!-- quadro de vidro escuro: raciocínio que se repete; .es.big para a regra de ouro da aula -->
<div class="es">
  <div class="kick">Se não melhorou, pense em quatro coisas</div>
  <p class="lead">Frase de situação.</p>
  <div class="cells">
    <div class="cell"><div class="lab">Entrada</div><p>...</p></div>
    <div class="cell"><div class="lab">Saída</div><p>...</p></div>
  </div>
</div>

<!-- fluxo numerado (título do passo embutido na frase) -->
<ol class="flow"><li><b class="t">Fígado: ciclo da ureia.</b> Texto do passo.</li></ol>

<!-- lista agrupada estilo iOS: .rows | .rows.terms (glossário) | .rows.terms.ess (uma linha por tema) -->
<div class="rows"><div class="row"><div class="k">Nota</div><div class="v">...</div></div></div>

<!-- comparação lado a lado: as MESMAS linhas nas duas colunas -->
<div class="cmp">
  <div class="r h"><div class="k"></div><div class="c">Gonorreia</div><div class="c">Clamídia</div></div>
  <div class="r"><div class="k">Incubação</div><div class="c">2 a 5 dias</div><div class="c">Mais longa</div></div>
</div>

<!-- régua de faixas (valores contínuos com zonas normal/alterado); larguras em % somam 100 -->
<div class="regua">
  <div class="ticks"><span class="first" style="left:0">0</span><span style="left:22%">400</span>...</div>
  <div class="bar"><span class="seg r" style="width:22%"></span><span class="seg n" style="width:23%"></span><span class="seg g" style="width:27%"></span>...<span class="dot"></span></div>
  <div class="labs"><div class="lab g" style="width:33%"><div class="nm">Normal <span class="v">2.100 a 2.800 mL</span></div>Descrição curta.</div>...</div>
</div>
<p class="regua-note">Nota sobre unidade e faixas sem nome.</p>

<!-- números da aula: .tile.g (valor normal), .tile.r (alterado), .tile (neutro) -->
<div class="tiles"><div class="tile g"><div class="lab">Ureia</div><div class="n">10 a 40 mg/dL</div><div class="s">no sangue do adulto</div></div></div>

<!-- data da prova -->
<div class="date"><div class="d"><span class="m">Novembro</span><span class="dd">12</span></div><div class="t"><b>Prova de ...</b><span>Quinta-feira, às 10h30...</span></div></div>

<!-- seta dentro do texto (Inter e Poppins não têm o caractere →) -->
Proteína <span class="arr"></span> amônia

<!-- figura -->
<div class="figure"><img src="mapa.svg" alt="..."></div>
```

Capa, legenda e sumário: copiar a estrutura abaixo e trocar os textos.

```html
<div class="cover">
  <div class="kicker">Disciplina · Aula N · Tema</div>
  <h1>Título da aula</h1>
  <p class="sub">Subtítulo de uma frase.</p>
  <div class="author"><span class="av">F</span><div><b>Dr. Nome</b><span>Descrição curta · 30 de setembro de 2026</span></div></div>
  <div class="keynums"><div class="kick">Três números para levar</div>
    <div class="kn-grid"><div class="kn"><div class="n">340 milhões</div><div class="l">de casos por ano no mundo</div></div>...</div></div>
  <div class="toc"><div class="kick">Nesta apostila</div>
    <a href="#s01"><span class="tn">01</span><span class="tt">Título da seção</span><span class="pg">{{s01}}</span></a>
    ...
    <p class="note">Organizada a partir da transcrição da aula, com os erros da transcrição automática corrigidos e a linguagem ajustada. A legenda de cores está na página 2.</p>
  </div>
</div>
<div class="legend"><div class="kick">Como ler esta apostila</div><div class="lg-grid">
  <div class="lg"><span class="sw blue"></span><div><b>Azul</b> conteúdo da aula e raciocínio</div></div>
  <div class="lg"><span class="sw green"></span><div><b>Verde</b> dose ou valor de referência</div></div>
  <div class="lg"><span class="sw red"></span><div><b>Vermelho</b> alerta, erro comum ou armadilha</div></div>
  <div class="lg"><span class="sw orange"></span><div><b>Laranja</b> fala ou parêntese do professor</div></div>
  <div class="lg"><span class="sw purple"></span><div><b>Roxo</b> complemento que não foi dito em aula</div></div>
  <div class="lg"><span class="prova">PROVA</span><div><b>Marca de prova</b> o ponto que cai na prova</div></div>
</div></div>
```

No fim da última seção, antes de `</section>`, colocar o marcador `{{NOTAS}}`. Os ids das seções são `s00`, `s01`... e o sumário usa `{{s01}}` como marcador de página.

## Ambiente

Rodar este bloco uma vez, na pasta de trabalho, antes de escrever o HTML. Ele instala o WeasyPrint e o pdfplumber, baixa a fonte Inter só se ela faltar e extrai desta skill os blocos marcados com `arquivo:` (o CSS e os dois scripts). A checagem roda toda em Python: não precisa de pdftoppm, pdftotext nem pdffonts.

```bash
pip install --break-system-packages -q weasyprint pdfplumber
if ! fc-list : family | grep -q "Inter SemiBold"; then
  curl -sSL -o /tmp/Inter.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz,wght%5D.ttf"
  mkdir -p ~/.fonts
  for w in 400:Regular 500:Medium 600:SemiBold 700:Bold; do
    python3 -m fontTools.varLib.instancer /tmp/Inter.ttf wght=${w%%:*} opsz=14 --update-name-table -o ~/.fonts/Inter-${w##*:}.ttf
  done
  fc-cache -f
fi
python3 - <<'EOF'
import re, glob, pathlib, os
achados = [a for pasta in ('/mnt/skills', os.path.expanduser('~/.claude/skills'))
           for a in sorted(glob.glob(pasta + '/**/apostila-padrao/SKILL.md', recursive=True))]
if not achados:
    raise SystemExit('SKILL.md da apostila-padrao não encontrado: copie à mão os blocos marcados com "arquivo:"')
md = pathlib.Path(achados[0]).read_text(encoding='utf-8')
F = '`' * 3
for corpo in re.findall(F + r'\w*\n(.*?)' + F, md, re.S):
    m = re.match(r'(?:/\*|#) arquivo: ([\w.-]+)', corpo)
    if m:
        pathlib.Path(m.group(1)).write_text(corpo, encoding='utf-8')
        print('extraído:', m.group(1))
EOF
```

As famílias ficam "Inter" (400 e 700), "Inter Medium" (500) e "Inter SemiBold" (600) — é assim que o CSS as chama.

## CSS completo (o bloco do Ambiente salva como apostila.css — não redigitar nem editar)

```css
/* arquivo: apostila.css */
/* ===== Apostila — visual iOS 27 / Liquid Glass (Inter) ===== */
@page {
  size: A4;
  margin: 16mm 15mm 18mm 15mm;
  background: #F2F2F7;
  /* o texto do rodapé vem do <meta name="rodape"> do HTML; o render.py aplica */
  @bottom-left { content: "Mauricio Faria · Disciplina · Aula — título curto"; font-family: Inter; font-size: 7.4pt; color: #8E8E93; }
  @bottom-right { content: counter(page); font-family: "Inter SemiBold"; font-size: 8pt; color: #0B5BD3; }
}
@page cover { margin: 0; background: #0A2A6B; @bottom-left { content: none; } @bottom-right { content: none; } }

html { font-family: Inter; font-size: 9.5pt; line-height: 1.55; color: #3A3A3C; }
body { margin: 0; }
p { margin: 0 0 7pt; }
b, strong { font-family: "Inter SemiBold"; font-weight: 600; color: #1F2933; }
em { font-style: italic; }
sub { font-size: 70%; vertical-align: -0.25em; line-height: 0; }
ul { margin: 0 0 8pt; padding: 0; list-style: none; }
ul li { position: relative; padding-left: 12pt; margin-bottom: 3pt; }
ul li::before { content: ""; position: absolute; left: 2pt; top: 0.58em; width: 4pt; height: 4pt; border-radius: 2pt; background: #A9C4EE; }
.small { font-size: 8.5pt; color: #6C6C70; }
.src { font-size: 8.3pt; color: #8E8E93; }
.medium { font-family: "Inter Medium"; font-weight: 500; color: #1F2933; }
.arr { display: inline-block; width: 1.05em; height: 0.62em; vertical-align: 0.02em;
  background: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 17 10'><path d='M1.2 5h13.2M10.6 1.6 14.4 5l-3.8 3.4' fill='none' stroke='%230B5BD3' stroke-width='1.7' stroke-linecap='round' stroke-linejoin='round'/></svg>") no-repeat center / contain; }

/* ===== capa: degradê + painéis de vidro ===== */
.cover { page: cover; width: 210mm; height: 297mm; box-sizing: border-box; position: relative;
  background: linear-gradient(155deg, #0A84FF 0%, #3B5BDB 42%, #6A3FC0 74%, #8E3BB8 100%);
  color: #FFFFFF; padding: 24mm 18mm 15mm; break-after: page; }
.cover .kicker { font-family: "Inter Medium"; font-size: 7.6pt; letter-spacing: .22em; text-transform: uppercase; color: #D9E6FF; margin-bottom: 10pt; }
.cover h1 { font-family: Inter; font-weight: 700; font-size: 30pt; line-height: 1.1; letter-spacing: -0.02em; color: #FFFFFF; margin: 0 0 12pt; bookmark-level: none; }
.cover .sub { font-size: 11.5pt; line-height: 1.5; color: #E6EDFF; margin: 0 0 20pt; max-width: 152mm; }
.cover .author { display: flex; align-items: center; background: #3D63C8; border: 1px solid #7FA2E8; border-radius: 14pt; padding: 9pt 14pt; width: 108mm; }
.cover .author .av { flex: none; width: 24pt; height: 24pt; border-radius: 12pt; background: #86B4FF; color: #16307A; font-family: "Inter SemiBold"; font-size: 10pt; text-align: center; line-height: 24pt; margin-right: 11pt; }
.cover .author b { display: block; font-family: "Inter SemiBold"; color: #FFFFFF; font-size: 10pt; }
.cover .author span { font-size: 8.6pt; color: #DCE7FF; }
.cover .keynums { margin-top: 26mm; }
.cover .kick { font-family: "Inter SemiBold"; font-size: 7.2pt; letter-spacing: .2em; text-transform: uppercase; color: #CFDEFF; margin-bottom: 8pt; }
.kn-grid { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 9pt; }
.kn { background: #4A66C6; border: 1px solid #8AA6EC; border-radius: 16pt; padding: 12pt 13pt 13pt; }
.kn .n { font-family: Inter; font-weight: 700; font-size: 19pt; line-height: 1.12; letter-spacing: -0.02em; color: #FFFFFF; }
.kn .l { font-size: 8.4pt; line-height: 1.4; color: #DFE8FF; margin-top: 4pt; }
.cover .toc { position: absolute; left: 18mm; right: 18mm; bottom: 15mm;
  background: #3E5FC4; border: 1px solid #89A6EA; border-radius: 18pt; padding: 12pt 16pt 14pt; }
.toc a { display: flex; align-items: baseline; text-decoration: none; color: #FFFFFF; font-size: 9.4pt; padding: 4.4pt 0; border-bottom: 1px solid #6E8FE0; }
.toc a:last-of-type { border-bottom: 0; }
.toc a .tn { width: 26pt; font-family: "Inter SemiBold"; font-size: 8.6pt; color: #B9D0FF; }
.toc a .tt { flex: 1; }
.toc a .pg { font-family: "Inter Medium"; font-size: 8.8pt; color: #CFDEFF; }
.cover .note { font-size: 8pt; line-height: 1.5; color: #D4E0FF; margin: 9pt 0 0; }

/* ===== legenda ===== */
.legend { background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 16pt; padding: 12pt 15pt 11pt; margin: 0 0 14pt; break-inside: avoid; }
.legend .kick { font-family: "Inter SemiBold"; font-size: 7.2pt; letter-spacing: .14em; text-transform: uppercase; color: #6C6C70; margin-bottom: 8pt; }
.lg-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 7pt 18pt; }
.lg { display: flex; align-items: center; font-size: 8.5pt; line-height: 1.35; }
.lg > span { margin-right: 9pt; }
.sw { flex: none; width: 20pt; height: 14pt; border-radius: 5pt; border: 1px solid; }
.sw.blue { background: #E8F0FE; border-color: #B9D2F8; }
.sw.green { background: #E7F7EC; border-color: #B4E3C2; }
.sw.red { background: #FDECEB; border-color: #F7C3BF; }
.sw.orange { background: #FFF3E1; border-color: #F6D6A4; }
.sw.purple { background: #F4EBFB; border-color: #DCC3F0; }
.lg .prova { margin-left: 0; flex: none; width: 20pt; padding-left: 2pt; padding-right: 2pt; text-align: center; vertical-align: 0; font-size: 5.6pt; letter-spacing: .06em; }

/* ===== títulos ===== */
.sec-head { display: flex; align-items: center; margin: 22pt 0 0; break-after: avoid; }
section:first-of-type .sec-head { margin-top: 0; }
.sec-head .num { flex: none; width: 26pt; height: 26pt; border-radius: 9pt; background: linear-gradient(145deg, #0A84FF, #5856D6);
  color: #FFFFFF; font-family: "Inter SemiBold"; font-size: 10pt; text-align: center; line-height: 26pt; margin-right: 11pt; }
h2 { font-family: Inter; font-weight: 700; font-size: 17pt; line-height: 1.18; letter-spacing: -0.015em; color: #16315C; margin: 0; bookmark-level: 1; }
.chips { margin: 6pt 0 10pt 37pt; break-after: avoid; }
.chip { display: inline-block; font-family: "Inter SemiBold"; font-size: 6.6pt; letter-spacing: .06em; text-transform: uppercase;
  color: #4F5B70; background: #E9EAF0; padding: 2.6pt 9pt 2.2pt; border-radius: 9pt; margin-right: 4pt; }
h3 { font-family: "Inter SemiBold"; font-weight: 600; font-size: 11.2pt; line-height: 1.3; letter-spacing: -0.01em; color: #0B5BD3; margin: 15pt 0 6pt; break-after: avoid; bookmark-level: 2; }
h3[data-bm] { bookmark-label: attr(data-bm); }
h4 { bookmark-level: none; }
.prova { display: inline-block; font-family: "Inter SemiBold"; font-size: 6.2pt; letter-spacing: .12em; line-height: 1.25;
  color: #FFFFFF; background: #1F2933; border-radius: 4pt; padding: 2pt 5pt 1.6pt 5.6pt; margin-left: 6pt; vertical-align: 1.6pt; }
.es .prova { background: #FFFFFF; color: #16315C; }

/* ===== caixas de vidro ===== */
.box { background: #E8F0FE; border: 1px solid #C3D8F8; border-radius: 15pt; padding: 11pt 15pt; margin: 11pt 0; break-inside: avoid; }
.box p:last-child, .box ul:last-child { margin-bottom: 0; }
.kick { font-family: "Inter SemiBold"; font-size: 7pt; letter-spacing: .12em; text-transform: uppercase; color: #0B5BD3; margin-bottom: 4pt; }
.kick .dot { display: inline-block; width: 5pt; height: 5pt; border-radius: 3pt; background: currentColor; margin-right: 5pt; vertical-align: 0.5pt; }
.box.purple { background: #F4EBFB; border-color: #DEC7F1; } .box.purple .kick { color: #6E3AA7; }
.box.orange { background: #FFF3E1; border-color: #F7DCAE; } .box.orange .kick { color: #9A5B00; }
.box.red { background: #FDECEB; border-color: #F8C9C5; } .box.red .kick { color: #C0362C; }
.box ul li::before { background: #9FBDEA; }
.box.red ul li::before { background: #EBA9A3; }

.quote { background: #FFF8EE; border: 1px solid #F3DCB6; border-radius: 15pt; padding: 10pt 15pt; margin: 12pt 0; break-inside: avoid; }
.quote p { font-style: italic; font-size: 10pt; color: #4A4A4F; margin: 0 0 3pt; }
.quote p i { font-style: normal; }
.quote .who { font-family: "Inter Medium"; font-size: 6.8pt; letter-spacing: .1em; text-transform: uppercase; color: #9A5B00; }

/* ===== cartões ===== */
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 9pt; margin: 8pt 0 11pt; }
.grid3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 9pt; margin: 8pt 0 11pt; }
.card { background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 15pt; padding: 10pt 13pt 11pt; break-inside: avoid; }
.card h4 { font-family: "Inter SemiBold"; font-weight: 600; font-size: 10pt; line-height: 1.3; color: #16315C; margin: 0 0 4pt; }
.grid3 .card h4 { font-size: 9.4pt; }
.card p, .card li { font-size: 9pt; line-height: 1.5; }
.card p:last-child, .card ul:last-child { margin-bottom: 0; }
.card .sub { color: #6C6C70; font-size: 8.6pt; margin-bottom: 5pt; }
.card .big { font-family: Inter; font-weight: 700; font-size: 15pt; color: #16315C; line-height: 1.2; margin: 1pt 0 4pt; letter-spacing: -0.015em; }
.card .tag { display: inline-block; font-family: "Inter SemiBold"; font-size: 6.4pt; letter-spacing: .08em; text-transform: uppercase;
  color: #0B5BD3; background: #E8F0FE; border-radius: 6pt; padding: 2pt 6pt 1.6pt; margin-bottom: 5pt; }
.card.red { border-color: #F3C9C5; } .card.red h4 { color: #C0362C; } .card.red .tag { color: #C0362C; background: #FDECEB; }
.card.green { border-color: #BFE5CB; } .card.green h4 { color: #1E7A34; } .card.green .tag { color: #1E7A34; background: #E7F7EC; }
.card.wide { margin: 8pt 0 11pt; }
.cols2 { column-count: 2; column-gap: 18pt; }
.cols2 li { break-inside: avoid; }

/* ===== valor / dose de referência ===== */
.ref { display: flex; align-items: center; background: #E7F7EC; border: 1px solid #BFE5CB; border-radius: 15pt; padding: 10pt 15pt; margin: 11pt 0; break-inside: avoid; }
.ref .txt { flex: 1; padding-right: 14pt; }
.ref .kick { color: #1E7A34; }
.ref .txt p { font-size: 8.9pt; margin: 0; }
.ref .val { font-family: Inter; font-weight: 700; font-size: 15pt; color: #1E7A34; white-space: nowrap; line-height: 1.15; text-align: right; letter-spacing: -0.015em; }
.ref .val small { display: block; font-family: "Inter Medium"; font-weight: 500; font-size: 7pt; letter-spacing: .06em; text-transform: uppercase; color: #3C8B51; }
.ref .vals { display: flex; }
.ref .vals .val + .val { margin-left: 18pt; padding-left: 16pt; border-left: 1px solid #BFE5CB; }
.ref.purple { background: #F4EBFB; border-color: #DEC7F1; }
.ref.purple .kick, .ref.purple .val { color: #6E3AA7; }
.ref.purple .val small { color: #8256BE; }
.ref.purple .vals .val + .val { border-color: #DEC7F1; }

/* ===== régua de faixas ===== */
.regua { margin: 10pt 0 6pt; break-inside: avoid; }
.regua .ticks { position: relative; height: 13pt; font-size: 7.6pt; font-family: "Inter Medium"; color: #6C6C70; }
.regua .ticks span { position: absolute; top: 0; width: 40pt; margin-left: -20pt; text-align: center; }
.regua .ticks span.first { margin-left: 0; text-align: left; }
.regua .bar { position: relative; display: flex; height: 11pt; }
.regua .seg { display: block; height: 11pt; box-sizing: border-box; border-right: 2pt solid #F2F2F7; }
.regua .seg:first-child { border-radius: 6pt 0 0 6pt; }
.regua .seg:last-child { border-radius: 0 6pt 6pt 0; border-right: 0; }
.regua .seg.r { background: #FF6B60; }
.regua .seg.g { background: #34C759; }
.regua .seg.n { background: #DCDCE2; }
.regua .dot { position: absolute; left: -4pt; top: -3.5pt; width: 14pt; height: 14pt; border-radius: 9pt; background: #C0362C; border: 2.2pt solid #FFFFFF; }
.regua .labs { display: flex; margin-top: 7pt; }
.regua .lab { box-sizing: border-box; padding-right: 8pt; font-size: 8.3pt; line-height: 1.4; }
.regua .lab .nm { font-family: "Inter SemiBold"; font-size: 9pt; white-space: nowrap; line-height: 1.5; }
.regua .lab .v { font-family: "Inter SemiBold"; font-size: 10pt; margin-left: 3pt; }
.regua .lab.r .nm, .regua .lab.r .v { color: #C0362C; }
.regua .lab.g .nm, .regua .lab.g .v { color: #1E7A34; }
.regua .lab.n { color: #8E8E93; font-size: 8pt; padding-top: 1pt; }
.regua .lab.r2 { margin-top: 5pt; }
.regua-note { font-size: 8.4pt; color: #6C6C70; margin: 4pt 0 10pt; }

/* ===== fluxo numerado ===== */
ol.flow { list-style: none; counter-reset: st; margin: 6pt 0 12pt; padding: 0; }
ol.flow li { counter-increment: st; position: relative; padding: 0 0 8pt 29pt; break-inside: avoid; font-size: 9.2pt; line-height: 1.5; }
ol.flow li::before { content: counter(st); position: absolute; left: 0; top: 0.3pt; width: 19pt; height: 19pt; border-radius: 7pt;
  background: #E8F0FE; border: 1px solid #C3D8F8; color: #0B5BD3; font-family: "Inter SemiBold"; font-size: 8pt; text-align: center; line-height: 18pt; }
ol.flow li::after { content: ""; position: absolute; left: 9.5pt; top: 21pt; bottom: 2pt; width: 1.2pt; background: #D3E1F8; }
ol.flow li:last-child::after { display: none; }
ol.flow li:last-child { padding-bottom: 0; }
ol.flow .t { color: #16315C; }

/* ===== listas agrupadas (estilo iOS) ===== */
.rows { background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 15pt; margin: 8pt 0 11pt; padding: 0 14pt; }
.row { display: flex; padding: 8pt 0; border-top: 1px solid #ECECF0; break-inside: avoid; }
.row:first-child { border-top: 0; }
.row .k { flex: none; width: 78pt; font-family: "Inter SemiBold"; font-size: 7pt; letter-spacing: .08em; text-transform: uppercase; color: #0B5BD3; padding-top: 2pt; padding-right: 8pt; }
.row .v { flex: 1; font-size: 9.2pt; }
.rows.terms .row .k { width: 122pt; font-family: "Inter SemiBold"; font-size: 9pt; letter-spacing: 0; text-transform: none; color: #16315C; padding-top: 0; }
.rows.ess .row .k { width: 92pt; }

/* ===== data da prova ===== */
.date { display: flex; align-items: center; background: linear-gradient(140deg, #0A5BD6, #5B49CE); border-radius: 16pt; padding: 12pt 16pt; margin: 10pt 0 12pt; color: #DCE7FF; break-inside: avoid; }
.date .d { flex: none; width: 66pt; border-right: 1px solid #7E9BE8; margin-right: 14pt; }
.date .m { display: block; font-family: "Inter SemiBold"; font-size: 7pt; letter-spacing: .2em; text-transform: uppercase; color: #CFE0FF; }
.date .dd { display: block; font-family: Inter; font-weight: 700; font-size: 27pt; color: #FFFFFF; line-height: 1.05; }
.date .t b { display: block; font-family: "Inter SemiBold"; color: #FFFFFF; font-size: 10.5pt; }
.date .t span { font-size: 8.8pt; line-height: 1.45; }

/* ===== quadro de vidro escuro / regra de ouro ===== */
.es { background: linear-gradient(140deg, #0A5BD6, #5B49CE); border-radius: 17pt; padding: 12pt 15pt 13pt; margin: 12pt 0; break-inside: avoid; color: #E9F0FF; }
.es .kick { color: #FFFFFF; margin-bottom: 5pt; }
.es .lead { font-size: 9.4pt; line-height: 1.5; color: #FFFFFF; margin: 0 0 9pt; }
.es .cells { display: flex; }
.es .cell { flex: 1; background: #3F63D4; border: 1px solid #7E9BE8; border-radius: 11pt; padding: 8pt 10pt 9pt; }
.es .cell + .cell { margin-left: 8pt; }
.es .cell .lab { font-family: "Inter SemiBold"; font-size: 6.8pt; letter-spacing: .12em; text-transform: uppercase; color: #CFE0FF; }
.es .cell p { font-size: 8.8pt; line-height: 1.45; color: #FFFFFF; margin: 3pt 0 0; }
.es .foot { font-size: 8.8pt; line-height: 1.5; color: #DCE7FF; margin: 9pt 0 0; }
.es.big { padding: 15pt 17pt 16pt; }
.es.big .lead { font-family: "Inter Medium"; font-size: 12.2pt; margin-bottom: 11pt; }
.es.big .cell p { font-size: 9.2pt; }

/* ===== comparação lado a lado ===== */
.cmp { background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 15pt; padding: 2pt 14pt 4pt; margin: 8pt 0 11pt; break-inside: avoid; }
.cmp .r { display: flex; border-top: 1px solid #ECECF0; padding: 6pt 0; }
.cmp .r.h { border-top: 0; padding: 9pt 0 6pt; }
.cmp .r.h div { font-family: "Inter SemiBold"; font-size: 10pt; color: #16315C; }
.cmp .k { flex: none; width: 76pt; font-family: "Inter SemiBold"; font-size: 7pt; letter-spacing: .08em; text-transform: uppercase; color: #0B5BD3; padding-top: 2pt; padding-right: 8pt; }
.cmp .c { flex: 1; font-size: 9pt; padding-right: 12pt; }
.cmp .g { color: #1E7A34; font-family: "Inter SemiBold"; }
.cmp .muted { color: #8E8E93; }

/* ===== números da aula ===== */
.tiles { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 9pt; margin: 8pt 0 12pt; }
.tile { background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 15pt; padding: 9pt 12pt 10pt; break-inside: avoid; }
.tile .lab { font-family: "Inter SemiBold"; font-size: 6.6pt; letter-spacing: .1em; text-transform: uppercase; color: #8E8E93; }
.tile .n { font-family: Inter; font-weight: 700; font-size: 13pt; line-height: 1.25; margin: 2pt 0 1pt; color: #16315C; letter-spacing: -0.015em; }
.tile .s { font-size: 8pt; line-height: 1.4; color: #6C6C70; }
.tile.g .n { color: #1E7A34; }
.tile.r .n { color: #C0362C; }

.figure { background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 16pt; padding: 12pt 14pt; margin: 8pt 0 12pt; break-inside: avoid; }
.figure img { width: 100%; }
.keep { break-inside: avoid; }
.notes { background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 16pt; padding: 10pt 14pt 12pt; break-inside: avoid; margin-top: 14pt; }
.notes .kick { color: #8E8E93; margin-bottom: 6pt; }
.notes .line { border-bottom: 1px solid #ECECF0; height: 21pt; }
.prof { background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 16pt; padding: 11pt 15pt 2pt; margin: 0 0 14pt; break-inside: avoid; }
.prof .kick { color: #6C6C70; letter-spacing: .14em; margin-bottom: 2pt; }
.prof .rows { border: 0; padding: 0; margin: 0; border-radius: 0; }

/* ===== ritmo vertical compacto + correções — manter no fim do arquivo ===== */
html { line-height: 1.5; }
p { margin-bottom: 6pt; }
h3 { margin-top: 12pt; }
.sec-head { margin-top: 17pt; }
.sec-head h2 { flex: 1 1 auto; min-width: 0; }   /* sem isto o título quebra em duas linhas */
.box { margin: 9pt 0; padding: 9.5pt 14pt; }
.grid2, .grid3 { margin: 6pt 0 9pt; }
.card { padding: 9pt 12pt 9pt; }
.cmp { margin: 6pt 0 9pt; }
.ref { margin: 9pt 0; padding: 9pt 14pt; }
.ref .txt { flex: 1.25; }
.ref .vals .val { font-size: 13pt; }
.ref .vals .val + .val { margin-left: 14pt; padding-left: 13pt; }
.es { margin: 10pt 0; }
.rows { margin: 6pt 0 9pt; break-inside: avoid; }  /* cartão de lista nunca é cortado */
.rows + .rows { margin-top: -3pt; }
.row { padding: 7pt 0; }
.figure { margin: 6pt 0 10pt; padding: 10pt 12pt; }
ol.flow li { padding-bottom: 5.5pt; }
```

## Armadilhas do WeasyPrint (erros já cometidos — não repetir)

- **Título de seção quebrando em duas linhas.** O `h2` dentro do `.sec-head` (flex) não cresce sozinho. A regra `.sec-head h2 { flex: 1 1 auto; min-width: 0 }` resolve — já está no CSS.
- **Linha de lista partida entre páginas.** `break-inside: avoid` em container flex (`.row`) não é respeitado: o rótulo fica numa página e o texto na outra, com o cartão cortado. Por isso `.rows` é atômico (`break-inside: avoid`) e **listas longas são divididas em vários grupos de 2 a 4 linhas** no HTML — vale para o glossário e para "A aula em uma linha por tema".
- **Grades são atômicas.** Uma faixa de `.tiles` ou uma linha de `.grid3` não se divide. Publique os números em blocos de 3 (uma faixa por bloco) e, quando uma linha de três cartões não couber, vire `.grid2` + `.card.wide`.
- **A corrente de `break-after: avoid`** (`.sec-head` → `.chips` → `h3` → primeiro bloco) tem de caber inteira, **incluindo a margem superior da seção**. Quando falta pouco, reduza a margem ou encurte o primeiro bloco.
- **Figura com colunas de alturas diferentes** fica torta: alinhe a última caixa de cada coluna na mesma base.
- **Texto do SVG cortado na borda**: ancore o primeiro rótulo em `start` e o último em `end`, nunca `middle` nas pontas. Deixe folga entre a caixa de apoio e os rótulos do eixo.
- **Cartão quase vazio ao lado de um cheio**: em `.grid2` os dois esticam para a mesma altura. Se um tem duas linhas, tire-o da grade e transforme em frase no texto ou use `.card.wide`.
- **Faixa `.ref` espremida**: com dois valores longos, use rótulo curto no `kick` e os valores em `.vals` (o CSS já reduz a fonte deles).
- **Rodapé longo demais**: com "Mauricio Faria · " na frente, o título da aula no rodapé tem de ser curto para caber numa linha só. Se quebrar (o `checar.py` avisa), encurte o título da aula no `<meta name="rodape">`, nunca tire o nome.
- **`letter-spacing` e o texto extraído**: rótulos em caixa alta saem com espaços entre as letras no `texto.txt` e no relatório do `render.py`. É artefato da extração, não defeito do PDF — confirme na imagem da página antes de "consertar".

## Geração do PDF (render.py — extraído pelo bloco do Ambiente)

Rodar `python3 render.py apostila.html "Disciplina - Aula N - Professor - Tema.pdf"` depois de cada mudança no HTML. Ele aplica o rodapé do `<meta name="rodape">`, encontra a maior área de anotações que cabe na última página, preenche os números de página do sumário e, no fim, imprime o espaço livre no pé de cada página.

```python
# arquivo: render.py
# uso: python3 render.py apostila.html "Disciplina - Aula N - Professor - Tema.pdf"
# Gera o PDF em duas passagens (páginas do sumário + área de anotações na última página)
# e mede o espaço livre no pé de cada página. Rodar de novo depois de cada ajuste.
import os, re, sys, html, logging, weasyprint, pdfplumber
logging.getLogger('weasyprint').setLevel(logging.ERROR)
LIMITE = 90        # pt livres aceitos no pé de cada página (a última não conta)
MAX_LINHAS = 26    # linhas da área de anotações, no máximo

src_path, out_path = sys.argv[1], sys.argv[2]
base = os.path.dirname(os.path.abspath(src_path))
src = open(src_path, encoding='utf-8').read()

# rodapé: texto do <meta name="rodape"> no <head>; a capa fica sem rodapé
m = re.search(r'<meta\s+name="rodape"\s+content="([^"]+)"', src)
if not m:
    sys.exit('Falta no <head>: <meta name="rodape" content="Mauricio Faria · Disciplina · Aula N — título curto">')
rod = html.unescape(m.group(1)).replace('\\', '\\\\').replace('"', '\\"')
estilo = ('<style>@page { @bottom-left { content: "%s"; } } '
          '@page cover { @bottom-left { content: none; } }</style>' % rod)
src = src.replace('</head>', estilo + '\n</head>', 1) if '</head>' in src else estilo + src
if '{{NOTAS}}' not in src:
    print('AVISO: falta o marcador {{NOTAS}} no fim da última seção')

def notas(n):
    return '' if n <= 0 else ('<div class="notes"><div class="kick">Anotações</div>'
                              + '<div class="line"></div>' * n + '</div>')
def montar(n, paginas=None):
    h = src.replace('{{NOTAS}}', notas(n))
    return re.sub(r'\{\{(s\d\d)\}\}', lambda x: str((paginas or {}).get(x.group(1), 0)), h)
def render(h):
    return weasyprint.HTML(string=h, base_url=base).render()

# maior área de anotações que cabe sem criar página nova (busca binária: poucas passagens)
total = len(render(montar(0)).pages)
lo, hi = 0, MAX_LINHAS
while lo < hi:
    mid = (lo + hi + 1) // 2
    if len(render(montar(mid)).pages) == total:
        lo = mid
    else:
        hi = mid - 1
doc = render(montar(lo))
paginas = {}
for i, p in enumerate(doc.pages):
    for a in p.anchors:
        paginas.setdefault(a, i + 1)
faltam = sorted(set(re.findall(r'\{\{(s\d\d)\}\}', src)) - set(paginas))
if faltam:
    print('AVISO: o sumário cita seções sem id correspondente:', ', '.join(faltam))
doc = render(montar(lo, paginas))
doc.write_pdf(out_path)
print(f'{out_path}: {len(doc.pages)} páginas | {lo} linhas de anotação')

# espaço livre no pé de cada página (sem a capa e sem a última)
def linhas(p, de_baixo=False):
    t = [l for l in (p.crop((0, 0, p.width, 791)).extract_text() or '').splitlines() if l.strip()]
    return t[-2:] if de_baixo else t[:2]
with pdfplumber.open(out_path) as pdf:
    pags, livres, buracos = pdf.pages, [], []
    for i in range(1, len(pags) - 1):
        p = pags[i]
        ys = [o['bottom'] for o in p.chars + p.rects + p.curves + p.lines if o['bottom'] < 790]
        livre = round(791 - max(ys)) if ys else 700
        livres.append(f'{i + 1}:{livre}' + ('!' if livre > LIMITE else ''))
        if livre > LIMITE:
            buracos.append((i, livre))
    print('Espaço livre no pé (pt; ! = acima de %d):' % LIMITE, ' '.join(livres) or '—')
    for i, livre in buracos:
        print(f'\nPágina {i + 1}: {livre} pt livres')
        print('  termina com:   ', ' / '.join(linhas(pags[i], True)))
        print(f'  página {i + 2} começa:', ' / '.join(linhas(pags[i + 1])))
    if not buracos:
        print('Nenhum buraco acima do limite.')
```

## Paginação: medir e fechar os buracos

O `render.py` mede sozinho o espaço livre no pé de cada página, menos a capa e a última. Meta: no máximo 90pt (cerca de 11% da página). Exemplo de saída: `Espaço livre no pé (pt; ! = acima de 90): 2:34 3:12 4:118! 5:8`. Para cada página marcada com `!`, ele mostra como a página termina e como a seguinte começa: o primeiro bloco da página seguinte é o que não coube.

Escada de correção, nesta ordem (nunca cortando conteúdo da aula):

1. **Reordenar blocos** dentro da seção: um bloco curto sobe para preencher o pé da página, o bloco alto desce. Exemplos que funcionaram: cartões das fases antes da linha do tempo; a caixa sobre exames logo depois da definição; a caixa de alerta antes da tabela.
2. **Dividir blocos atômicos**: listas em grupos de 2 a 4 linhas, números em faixas de 3, `.grid3` em `.grid2` + `.card.wide`.
3. **Tirar redundância de texto** (uma linha aqui, uma ali) até o bloco caber — reescrevendo, não deletando informação.
4. **Ajustar o ritmo vertical** (o bloco final do CSS) em último caso, e nunca abaixo de `line-height: 1.5`.

Um bloco que não cabe empurra a página inteira: quando faltarem menos de 10pt, meça a altura real do bloco com `pdfplumber` (`p.rects` e `p.curves`: as caixas de canto arredondado são curvas) em vez de adivinhar.

## Figuras

Desenhe em SVG gerado por Python, medindo o texto com `PIL.ImageFont.truetype(arquivo, tamanho).getlength()` para quebrar linha; o caminho do arquivo da fonte sai de `fc-match -f '%{file}' 'Inter:weight=regular'` (o PIL não entende `~` no caminho). Largura do SVG = 478pt (a largura útil dentro do cartão `.figure`). Paleta: caixas brancas com borda #C3D8F8, fundo de apoio #F5F8FF, setas #8AA9DF (desenhadas como polígono, sem `marker`), texto #1F2933, títulos #16315C. A figura usa só o azul: verde e vermelho continuam reservados para valor e alerta.

Repertório já aprovado:

- **Régua** para grandezas com faixas (diurese, glicemia, pressão): faixa normal verde, alterada vermelha, faixa sem nome em cinza com a nota "sem nome na aula".
- **Algoritmo sindrômico**: uma coluna por síndrome, caixas encadeadas por setas, a conduta final em verde, **todas as colunas terminando na mesma base**.
- **Linha do tempo**: eixo com marcos acima e caixas de fase abaixo, mais uma caixa de apoio explicando o comportamento dos exames.
- **Cascata**: nome da etapa e nota à esquerda, barra proporcional à direita, uma cor só; o que se perde em cada etapa em vermelho, ao lado.
- **Mapa de caminhos** (metabolismo, fisiopatologia): colunas = órgãos ou etapas, linhas = cada produto, caixas tracejadas para o que entra pela dieta, selos numerados quando a ordem importa.

Nunca use caracteres que a fonte não tem (→, ①, ✓, ★): seta no texto é `<span class="arr"></span>` e número em círculo é desenhado.

## Checagem automática (checar.py — extraído pelo bloco do Ambiente)

Rodar `python3 checar.py "Disciplina - Aula N - Professor - Tema.pdf" apostila.html` com o PDF pronto. Ele confere fontes, rodapé, marcadores do PDF, marcadores `{{ }}` esquecidos, siglas e o dia da semana de cada data; salva o texto do PDF em `texto.txt` e as páginas em espelho (capa sozinha, depois pares) na pasta `paginas/`. Avisos dele são defeitos a corrigir; a lista de siglas e as datas são para revisar.

```python
# arquivo: checar.py
# uso: python3 checar.py "Disciplina - Aula N - Professor - Tema.pdf" apostila.html
# Checagem automática antes de entregar: fontes, rodapé, marcadores do PDF, marcadores {{ }}
# esquecidos, siglas e datas (dia da semana) no texto. Salva o texto do PDF em texto.txt
# (para comparar com a fonte) e as páginas em espelho na pasta paginas/ (para olhar com Read).
import os, re, sys, html, datetime, pdfplumber, pypdfium2 as pdfium
from PIL import Image
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.utils import decode_text

pdf_path, html_path = sys.argv[1], sys.argv[2]
avisos = []
pdf = pdfplumber.open(pdf_path)
pags = pdf.pages

# 1. fontes: só Inter (o Inter-Oblique sintético das citações é esperado)
fontes = sorted({re.sub(r'^[A-Z]{6}\+', '', c['fontname']) for p in pags for c in p.chars})
print('Fontes:', ', '.join(fontes))
fora = [f for f in fontes if not f.lower().startswith('inter')]
if fora:
    avisos.append('fonte fora do padrão: ' + ', '.join(fora))

# 2. rodapé: nenhum na capa, um em cada página seguinte, sempre numa linha só
for i, p in enumerate(pags, 1):
    rod = [c for c in p.chars if c['top'] > 795 and c['x0'] < p.width * 0.75]
    if i == 1:
        if rod:
            avisos.append('a capa tem rodapé')
        continue
    if not rod:
        avisos.append(f'página {i} sem rodapé')
        continue
    tops = sorted(c['top'] for c in rod)
    if sum(1 for a, b in zip(tops, tops[1:]) if b - a > 4):
        avisos.append(f'rodapé em mais de uma linha na página {i}: encurte o título curto')
if len(pags) > 1:
    print('Rodapé:', (pags[1].crop((0, 795, pags[1].width, pags[1].height)).extract_text() or '').strip())

# 3. marcadores do PDF (sem "PROVA" no nome)
with open(pdf_path, 'rb') as f:
    try:
        marc = [(n, decode_text(t) if isinstance(t, bytes) else str(t))
                for n, t, *_ in PDFDocument(PDFParser(f)).get_outlines()]
    except Exception:
        marc = []
print('Marcadores:', ' | '.join(('  ' * (n - 1)) + t for n, t in marc) or 'nenhum')
if any('PROVA' in t for _, t in marc):
    avisos.append('marcador com "PROVA" no nome: use data-bm no h3')

# 4. texto do PDF em texto.txt + marcadores {{ }} esquecidos
texto = ''.join(f'\n=== página {i} ===\n' + (p.extract_text() or '') for i, p in enumerate(pags, 1))
open('texto.txt', 'w', encoding='utf-8').write(texto)
if '{{' in texto:
    avisos.append('sobrou marcador {{ }} no PDF')

# 5. siglas e datas, lidas do HTML (o PDF tem rótulos em caixa alta que confundiriam)
fonte = open(html_path, encoding='utf-8').read()
fonte = re.sub(r'(?s)<head>.*?</head>|<style.*?</style>|<script.*?</script>|\{\{.*?\}\}', ' ', fonte)
corrido = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', fonte)))
siglas = {}
for s in re.findall(r'\b[A-ZÀ-Ý]{2,}\b', corrido):
    if s not in ('PROVA', 'PROEX') and not re.fullmatch(r'[IVXLC]+', s):
        siglas[s] = siglas.get(s, 0) + 1
print('Siglas para revisar:', ', '.join(f'{s} ({n}x)' for s, n in sorted(siglas.items())) or 'nenhuma')

MESES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto',
         'setembro', 'outubro', 'novembro', 'dezembro']
NOMES = ['segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado', 'domingo']
mes = '(' + '|'.join(MESES) + ')'
achadas = []   # (início, fim, data, ano presumido?)
for m in re.finditer(r'\b(\d{1,2})º? de ' + mes + r' de (\d{4})', corrido, re.I):
    achadas.append((m.start(), m.end(), datetime.date(int(m[3]), MESES.index(m[2].lower()) + 1, int(m[1])), False))
for m in re.finditer(r'\b(\d{1,2})/(\d{1,2})/(\d{4})\b', corrido):
    achadas.append((m.start(), m.end(), datetime.date(int(m[3]), int(m[2]), int(m[1])), False))
ano = min((a[2].year for a in achadas), default=datetime.date.today().year)
for m in re.finditer(r'\b' + mes + r' (\d{1,2})\b(?! de \d)', corrido, re.I):   # cartão da data da prova
    achadas.append((m.start(), m.end(), datetime.date(ano, MESES.index(m[1].lower()) + 1, int(m[2])), True))
print('Datas:' if achadas else 'Datas: nenhuma')
dia = r'\b(?:segunda|terça|quarta|quinta|sexta)-feira\b|\bsábado\b|\bdomingo\b'
for ini, fim, d, presumido in sorted(achadas):
    certo = NOMES[d.weekday()]
    antes = corrido[max(0, ini - 40):ini]
    perto = [(m.start(), m[0]) for m in re.finditer(dia, corrido[fim:fim + 60], re.I)]      # logo depois
    perto += [(len(antes) - m.end(), m[0]) for m in re.finditer(dia, antes, re.I)]          # logo antes
    citado = min(perto)[1].lower() if perto else None   # o dia da semana mais próximo da data
    nota = f'  {d.strftime("%d/%m/%Y")} é {certo}' + (' (ano presumido)' if presumido else '')
    if citado and citado != certo:
        nota += f'  <- o texto diz "{citado}"'
        avisos.append(f'dia da semana errado: {d.strftime("%d/%m/%Y")} é {certo}, o texto diz {citado}')
    print(nota + ('  · confere' if citado == certo else ''))

# 6. páginas em espelho (capa sozinha, depois pares) na pasta paginas/
os.makedirs('paginas', exist_ok=True)
for f in os.listdir('paginas'):
    if f.startswith('pag-') and f.endswith('.png'):
        os.remove(os.path.join('paginas', f))
doc = pdfium.PdfDocument(pdf_path)
imgs = [doc[i].render(scale=82 / 72).to_pil() for i in range(len(doc))]
grupos = [[0]] + [list(range(i, min(i + 2, len(imgs)))) for i in range(1, len(imgs), 2)]
nomes = []
for g in grupos:
    folha = Image.new('RGB', (sum(imgs[i].width for i in g) + 14 * (len(g) - 1), max(imgs[i].height for i in g)), '#8E8E93')
    x = 0
    for i in g:
        folha.paste(imgs[i], (x, 0))
        x += imgs[i].width + 14
    nome = f'paginas/pag-{g[0] + 1:02d}' + (f'-{g[-1] + 1:02d}' if len(g) > 1 else '') + '.png'
    folha.save(nome)
    nomes.append(nome)
print('Imagens para olhar uma a uma:', ' '.join(nomes))
print('Texto do PDF salvo em texto.txt')

print('\nAvisos:' if avisos else '\nNenhum aviso automático.', *('\n  - ' + a for a in avisos))
print('Falta o olhar humano: imagens das páginas, cores contra a tabela e conteúdo contra a fonte.')
```

## Lista de checagem antes de entregar

- Número da aula, data, professor e disciplina iguais aos respondidos no passo 0, na capa, no rodapé e no nome do arquivo ("Disciplina - Aula N - Professor - Tema.pdf").
- Disciplina conferida na tabela da seção "Disciplina": capa, rodapé e nome do arquivo com o nome da disciplina da grade, nunca o da subespecialidade.
- Professor conferido na seção "Professores": nome completo com "Dr."/"Dra." e descrição no cartão da capa, forma curta nas citações, quadro "Sobre o professor" com o currículo na página 2.
- `render.py` sem nenhuma página marcada com `!` (a última não conta) e sem avisos.
- `checar.py` sem avisos: só Inter nas fontes (o Inter-Oblique sintético das citações é esperado); rodapé "Mauricio Faria · Disciplina · Aula N — título curto" em todas as páginas menos a capa, numa linha só; marcadores do PDF sem "PROVA"; nenhum `{{ }}` sobrando; nenhuma data com dia da semana errado.
- Siglas da lista do `checar.py` revisadas: só fica nome de exame que só existe como sigla, explicado na primeira aparição e no glossário.
- Olhar uma a uma **todas** as imagens da pasta `paginas/`: títulos quebrados, cartões cortados no fim da página, cartão vazio ao lado de cheio, texto encostando na borda de figura, órfãos no pé, sumário legível.
- Comparar o `texto.txt` com a fonte: nada da aula ficou de fora; nenhum complemento sem a caixa roxa.
- Cores conferidas contra a tabela de significado: nenhum verde que não seja valor ou dose, nenhum vermelho que não seja alerta ou erro, nenhum roxo fora de complemento.
- "Dr."/"Dra." com ponto.