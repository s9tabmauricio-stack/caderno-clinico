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

   Fazer as quatro perguntas de uma vez, numa mensagem só (com a ferramenta de perguntas do assistente, se houver; senão, em texto). Pode oferecer como opção o que a fonte sugere (por exemplo, o professor pelas pistas da fala), mas quem decide é a resposta. O que ele responder vale acima da fonte. Se ele não souber algum item, seguir sem ele e pôr na lista do que vale conferir.
1. **Ler a fonte inteira** (transcrição, slides ou resumo). Anotar: temas, valores numéricos, doses, falas marcantes do professor, avisos da disciplina (data de prova, nota, presença), o que ele disse que cobra e o que disse que não cobra, perguntas de alunos, casos contados em aula.
2. **Corrigir os erros da transcrição automática** (termos médicos trocados, nomes). Não perder nenhum conteúdo da aula. Limpar palavrão e piada longa, preservando o conteúdo clínico e as falas que valem como citação.
3. **Planejar as seções**: 00 Recados (só se houver avisos), 01 a N por tema, e a última seção "O essencial da aula".
4. **Preparar o ambiente** com a linha da seção "Ambiente" (`apostilas-fonte/ferramentas/preparar.sh <pasta>`): instala o que falta e copia `apostila.css`, `render.py`, `checar.py` e a fonte. **Nunca redigitar esses arquivos.**
5. **Escrever o HTML** a partir do esqueleto e dos componentes desta skill. O texto do rodapé vai no `<meta name="rodape">`; o CSS não se edita.
6. **Desenhar as figuras** quando o tema pedir (régua, algoritmo, linha do tempo, cascata, mapa).
7. **Gerar o PDF** com `python3 render.py apostila.html "Disciplina - Aula N - Professor - Tema.pdf"`. Ele faz as duas passagens (números de página do sumário + área de anotações na última página) e já mostra o espaço livre no pé de cada página.
8. **Fechar os buracos da paginação** com a escada da seção "Paginação", rodando o `render.py` de novo depois de cada ajuste — é onde mora a maior parte do trabalho.
9. **Conferir** com `python3 checar.py "Disciplina - Aula N - Professor - Tema.pdf" apostila.html`, olhar **todas** as imagens da pasta `paginas/` e passar a lista de checagem. Entregar o PDF (no Claude, com SendUserFile; nos outros assistentes, dizendo o caminho do arquivo). Na resposta: uma linha sobre o que saiu e a lista curta do que vale conferir (complementos acrescentados, trechos ininteligíveis da transcrição, nome do professor).

## Regras de escrita

- Português do Brasil, linguagem simples. **Sem siglas nem abreviações**: escrever por extenso ("taxa de filtração glomerular", "infecções sexualmente transmissíveis", "vírus da imunodeficiência humana"). Unidades de medida são permitidas (mL, mg/dL, kg, g). Nome de exame que só existe como sigla (VDRL, FTA-Abs) pode ficar, mas explique na primeira aparição e registre no glossário.
- **"Dr." e "Dra." sempre com ponto**, padronizados, mesmo que a fonte seja inconsistente.
- Números no formato brasileiro: 2.100; 1,2; 10h30.
- **Negrito com parcimônia**: no máximo um trecho por parágrafo. Em listas, negrito só no termo inicial do item.
- **Complemento**: tudo o que não foi dito em aula vai só em caixa roxa "Complemento: fora da aula" (ou no valor de referência roxo). Nunca misturar com o conteúdo da aula.
- **Marca PROVA**: onde o professor diz ou dá a entender que é importante (regra do Mauricio, 07/11/2026). Ninguém fala "isso cai na prova": valem palavra de ênfase ("obrigatório", "precisa gravar", "guardem na cabeça"), repetição ("vou falar de novo"), ordem direta ("nunca", "é proibido"), demonstração ou caso encenado, alerta de erro, slide de resumo "para gravar" e pergunta à turma. Não basta o assunto ser importante na medicina, longo ou estar só no slide. A lista completa está em `docs/apostila-molde.md` ("Redação da apostila"). Só em blocos específicos (um título de subseção, um quadro), nunca na seção inteira; no mapa, a frase e o minuto de cada uma. Na dúvida, marque; se a maioria dos subtítulos ganhar PROVA, reveja.
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

Uma linha, na pasta de trabalho, antes de escrever o HTML (vale para Claude, Antigravity e Codex):

```bash
apostilas-fonte/ferramentas/preparar.sh <pasta-de-trabalho>
```

Ele instala o WeasyPrint e o pdfplumber se faltarem, instala a fonte Inter guardada no projeto (sem internet) e copia para a pasta o `apostila.css` oficial (`apostilas-fonte/apostila.css`), o `render.py`, o `checar.py` e a pasta `fonts/`. **Nunca redigite nem edite esses arquivos**, nem abra o CSS para "conferir": os componentes abaixo dizem tudo o que o HTML precisa. A checagem roda toda em Python: não precisa de pdftoppm, pdftotext nem pdffonts.

As famílias ficam "Inter" (400 e 700), "Inter Medium" (500) e "Inter SemiBold" (600) — é assim que o CSS as chama.

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

## Geração do PDF (render.py, copiado pelo preparar.sh)

Rodar `python3 render.py apostila.html "Disciplina - Aula N - Professor - Tema.pdf"` depois de cada mudança no HTML. Ele aplica o rodapé do `<meta name="rodape">`, encontra a maior área de anotações que cabe na última página, preenche os números de página do sumário e, no fim, imprime o espaço livre no pé de cada página.

## Paginação: medir e fechar os buracos

O `render.py` mede sozinho o espaço livre no pé de cada página, menos a capa e a última. Meta: no máximo 90pt (cerca de 11% da página). Exemplo de saída: `Espaço livre no pé (pt; ! = acima de 90): 2:34 3:12 4:118! 5:8`. Para cada página marcada com `!`, ele mostra como a página termina e como a seguinte começa: o primeiro bloco da página seguinte é o que não coube.

Escada de correção, nesta ordem (nunca cortando conteúdo da aula):

1. **Reordenar blocos** dentro da seção: um bloco curto sobe para preencher o pé da página, o bloco alto desce. Exemplos que funcionaram: cartões das fases antes da linha do tempo; a caixa sobre exames logo depois da definição; a caixa de alerta antes da tabela.
2. **Dividir blocos atômicos**: listas em grupos de 2 a 4 linhas, números em faixas de 3, `.grid3` em `.grid2` + `.card.wide`.
3. **Tirar redundância de texto** (uma linha aqui, uma ali) até o bloco caber — reescrevendo, não deletando informação.
4. **Ajustar o ritmo vertical** (sobrescrevendo, no `<style>` do HTML, as regras do bloco final do `apostila.css`) em último caso, e nunca abaixo de `line-height: 1.5`.

Um bloco que não cabe empurra a página inteira: quando faltarem menos de 10pt, meça a altura real do bloco com `pdfplumber` (`p.rects` e `p.curves`: as caixas de canto arredondado são curvas) em vez de adivinhar.

## Figuras

Desenhe em SVG gerado por Python, medindo o texto com `PIL.ImageFont.truetype(arquivo, tamanho).getlength()` para quebrar linha; o arquivo da fonte é `fonts/Inter-Regular.ttf` (ou `-Medium`, `-SemiBold`, `-Bold`) da pasta de trabalho, copiada pelo `preparar.sh`. Largura do SVG = 478pt (a largura útil dentro do cartão `.figure`). Paleta: caixas brancas com borda #C3D8F8, fundo de apoio #F5F8FF, setas #8AA9DF (desenhadas como polígono, sem `marker`), texto #1F2933, títulos #16315C. A figura usa só o azul: verde e vermelho continuam reservados para valor e alerta.

Repertório já aprovado:

- **Régua** para grandezas com faixas (diurese, glicemia, pressão): faixa normal verde, alterada vermelha, faixa sem nome em cinza com a nota "sem nome na aula".
- **Algoritmo sindrômico**: uma coluna por síndrome, caixas encadeadas por setas, a conduta final em verde, **todas as colunas terminando na mesma base**.
- **Linha do tempo**: eixo com marcos acima e caixas de fase abaixo, mais uma caixa de apoio explicando o comportamento dos exames.
- **Cascata**: nome da etapa e nota à esquerda, barra proporcional à direita, uma cor só; o que se perde em cada etapa em vermelho, ao lado.
- **Mapa de caminhos** (metabolismo, fisiopatologia): colunas = órgãos ou etapas, linhas = cada produto, caixas tracejadas para o que entra pela dieta, selos numerados quando a ordem importa.

Nunca use caracteres que a fonte não tem (→, ①, ✓, ★): seta no texto é `<span class="arr"></span>` e número em círculo é desenhado.

## Checagem automática (checar.py, copiado pelo preparar.sh)

Rodar `python3 checar.py "Disciplina - Aula N - Professor - Tema.pdf" apostila.html` com o PDF pronto. Ele confere fontes, rodapé, marcadores do PDF, marcadores `{{ }}` esquecidos, siglas e o dia da semana de cada data; salva o texto do PDF em `texto.txt` e as páginas em espelho (capa sozinha, depois pares) na pasta `paginas/`. Avisos dele são defeitos a corrigir; a lista de siglas e as datas são para revisar.

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