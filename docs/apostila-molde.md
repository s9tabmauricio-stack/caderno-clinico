# Molde da apostila

Combinado com o Mauricio em 02/11/2026 e aprovado na pneumo-a5 (primeira apostila feita assim). Vale para toda apostila nova ou refeita, junto com a skill `apostila-padrao`; onde as duas divergem, vale este arquivo.

## Duas etapas

1. **Mapa** (abaixo) e, se a aula pedir ilustrações, `imagens-gpt.md` com os prompts. O Mauricio gera as imagens no ChatGPT e manda na conversa; a conversa principal confere cada uma (anatomia, nenhuma letra) antes de usar.
2. **Apostila**, seguindo o mapa.

**Guarde o HTML, não só a imagem.** O site mostra as páginas em imagem, mas o que se corrige é o HTML. Toda apostila nova ou refeita vai para o Git em `apostilas-fonte/<aula-id>/`: `apostila.html`, o `mapa.md`, as figuras (`*.svg`) e os programas que as desenham (como em [`apostilas-fonte/README.md`](../apostilas-fonte/README.md)). Para corrigir, mude o HTML, gere o PDF de novo e publique com a skill `subir-apostila`.

**Na aula nova automática** (skill `aula-nova`), ninguém espera imagens: a apostila sai com as imagens dos slides e os SVGs, sem ilustrações do GPT. O agente deixa `imagens-gpt.md` pronto e põe na lista do que conferir as ilustrações que valeriam a pena; o Mauricio decide depois se gera e troca a apostila.
Sem slides, o mapa liga capítulos a minutos da transcrição.

## Fontes: transcrição + slides

- **Tudo sai da fonte da aula** (regra do Mauricio, 09/11/2026): antes de começar, a transcrição e os slides são guardados num arquivo só, `apostilas-fonte/<aula-id>/fonte.md`, com `scripts/fonte-aula.py` ([`apostilas-fonte/README.md`](../apostilas-fonte/README.md)). A apostila é escrita a partir dele, e é contra ele que ela é conferida depois (skill `conferir-apostila`). Os minutos e as páginas de slide do mapa são os da fonte. O arquivo original dos slides serve para as imagens e para as páginas marcadas como "só imagem".
- **A fala manda**: o que o professor ensinou, como explicou e o que destacou.
- **Os slides completam**: números, tabelas, definições, fluxogramas, referências e as imagens para onde ele apontava ("isso aqui", "nesse fluxograma").
- **O que está só no slide conta como aula**, sem caixa roxa. O roxo fica para o que não está em nenhum dos dois.
- **O que ele disse que tirou da aula** (ex.: "não falo mais de neoplasias de pleura") não entra como conteúdo, nem se estiver no slide. O que ele deu, mesmo sendo sobre câncer (derrame neoplásico, pleurodese), entra.
- **O que o professor fala manda sempre** (regra do Mauricio, 02/11/2026). Slide e fala divergem (um número, um corte, uma definição): a apostila ensina e marca PROVA pela fala; o valor do slide aparece numa linha, só como registro, e entra na lista do que conferir. Se um livro disser outra coisa, no máximo uma linha roxa "Nos livros", sem mudar nem enfraquecer o que ele ensinou.

## Redação da apostila

- **A apostila é um material de estudo com leitura autônoma.** Ensine o conteúdo diretamente, sem narrar repetidamente que "o professor disse", "comentou" ou "explicou".
- **O PDF não mostra o processo de produção:** não mencionar gravação, áudio, transcrição, minutagem, ruídos, trechos ininteligíveis, lacunas da fonte nem ausência de slides. A rastreabilidade, as dúvidas e o que falta conferir ficam no mapa e nos arquivos internos de revisão.
- **As citações do professor devem permanecer**, com autoria e sem minutagem, quando destacarem lições de vida e profissão, experiência clínica, humanidade, ética, relação com o paciente ou sinais do que pode ser cobrado na prova. Selecione as que ensinam algo; não transforme cada explicação técnica em citação.
- **Marca PROVA: quando o professor diz ou dá a entender que é importante** (regra do Mauricio, 07/11/2026). Ninguém fala "isso cai na prova"; o professor insinua. Conta como sinal:
  - **palavra de ênfase:** "é importante", "obrigatório", "precisa gravar", "guardem na cabeça", "não esqueçam", "lembrem";
  - **repetição:** volta ao assunto várias vezes, ou "já falei, mas vou falar de novo";
  - **ordem direta:** "nunca", "sempre", "é proibido";
  - **teatro:** demonstra com um aluno, encena um diálogo, conta "aquele paciente que chega no pronto-socorro…";
  - **alerta de erro:** "se virem alguém fazendo isso, não é o certo";
  - **resumo:** "esse slide é o que vocês precisam gravar";
  - **pergunta à turma** sobre o ponto, esperando a resposta.

  Não conta: o assunto ser importante na medicina em geral, ocupar muito tempo, aparecer só no slide, ou ser parêntese ou piada. A marca vai no bloco exato (subtítulo ou quadro), nunca na seção inteira. No mapa, cada PROVA leva a frase do professor e o minuto. Na dúvida, marque; mas se a maioria dos subtítulos ganhar PROVA, a marca perde o valor: reveja. É a mesma regra das questões e dos flashcards (`cai_na_prova`): o que é PROVA na apostila vira faixa PROVA na questão.
- Notas clínicas, limites dos dados e referências científicas continuam quando necessários, com redação natural e a identificação roxa de complemento quando couber, sem expor problemas de gravação ou de elaboração da apostila.

## Antes de escrever: o mapa

`mapa.md` na pasta da aula, curto, em tópicos:
1. **Trilha da aula**: o caminho de raciocínio em 5 a 9 etapas (ex.: falta de ar → exame físico → radiografia → punção → Light → empiema → drenagem; pneumotórax ao lado).
2. **Para cada capítulo**: título provisório; rascunho do "Em palavras simples"; páginas dos slides e minutos da transcrição que entram; pontos PROVA (com a fala e o minuto); pegadinhas; divergências; o formato de cada bloco (ver "Formato segue o conteúdo"); figuras (SVG a desenhar, imagem de exame do slide com o que apontar, ilustração do GPT).
3. **Cobertura**: cada página dos slides (1 a N) → capítulo, ou "fora: motivo".
4. **Fica de fora e por quê.**

## As cinco mudanças

1. **"Em palavras simples"** logo abaixo do cabeçalho de cada capítulo: 2 a 3 linhas, em linguagem de conversa: o que é e o que muda para o paciente ou para a conduta. O termo técnico vem depois, no texto. O glossário do fim fica só com os termos que não aparecem nessas aberturas.
2. **Trilha da aula**: uma figura do caminho da aula no começo (logo antes do capítulo 01) e, no cabeçalho de cada capítulo, uma faixa "você está aqui" com a etapa atual destacada, no lugar dos chips cinzas de tema.
3. **Formato segue o conteúdo** (não pôr tudo na mesma caixa rótulo/texto):
   - comparar → tabela lado a lado (ex.: transudato × exsudato);
   - técnica → passos numerados, com ilustração quando houver;
   - decisão → fluxograma em SVG (o que o professor disse que é a base da prova leva PROVA);
   - exame → imagem do slide recortada, com setas e rótulos desenhados por nós e a legenda "O que olhar".
4. **Pegadinha do professor**: caixa vermelha (vermelho = alerta, erro comum ou armadilha) dentro do capítulo, no ponto onde o erro acontece. A lista "Erros comuns" do fim fica curta.
5. **Página de véspera** no fim, no lugar do resumo longo: uma página com todos os pontos PROVA e os números da aula, na ordem da trilha. Glossário e Anotações continuam depois dela.

## Ajustes de diagramação

- Cartão grande para uma linha só vira faixa compacta.
- Cabeçalho de capítulo não começa no último terço da página deixando espaço vazio embaixo: empurre para a página seguinte ou rearrume os blocos.
- A turma lê no **tablet**: mantenha A4 retrato e o tamanho de letra atual.

## Componentes novos

- Os blocos novos vão num `<style>` no próprio `apostila.html`, depois do `apostila.css` (que não muda, para as apostilas antigas saírem iguais se forem geradas de novo). Comece por este, o aprovado na pneumo-a5 (estes estilos ajustam também `.cover`, `.figure`, `.tiles`, `.cmp` e `.sw`):

```css
/* ===== componentes do molde novo (em teste na pneumo-a5) ===== */
.simples { background: #FFFFFF; border: 1px solid #C3D8F8; border-left: 4pt solid #0B5BD3; border-radius: 12pt; padding: 9pt 14pt 10pt; margin: 0 0 10pt; break-inside: avoid; }
.simples p { font-size: 10.2pt; line-height: 1.5; color: #1F2933; margin: 0; }
.aqui { display: flex; margin-top: 7pt; }
.aqui span { flex: 1; border-top: 3pt solid #DCDCE2; padding-top: 2.5pt; margin-right: 2.5pt; font-family: "Inter Medium"; font-size: 6pt; line-height: 1.25; color: #8E8E93; }
.aqui span:last-child { margin-right: 0; }
.aqui span.feito { border-top-color: #A9C4EE; color: #6C6C70; }
.aqui span.on { border-top-color: #0B5BD3; color: #0B5BD3; font-family: "Inter SemiBold"; }
.aqui span.ramo { border-top-style: dashed; }
.figure .olhar { margin-top: 8pt; }
.figure .olhar .kick { margin-bottom: 3pt; }
.figure .olhar ul { margin: 0; }
.figure .olhar li { padding-left: 0; font-size: 8.7pt; line-height: 1.45; margin-bottom: 2pt; }
.figure .olhar li::before { display: none; }
.figure .olhar li b { color: #0B5BD3; }
.figure .leg { font-size: 7.8pt; color: #8E8E93; margin: 5pt 0 0; }
.reg { font-size: 8.3pt; line-height: 1.45; color: #6C6C70; background: #F7F7FA; border: 1px solid #E3E3E8; border-radius: 9pt; padding: 5pt 10pt; margin: 6pt 0 9pt; break-inside: avoid; }
.reg b { font-family: "Inter SemiBold"; color: #4F5B70; }
.livros { font-size: 8.3pt; line-height: 1.45; color: #6E3AA7; background: #F4EBFB; border: 1px solid #DEC7F1; border-radius: 9pt; padding: 5pt 10pt; margin: 6pt 0 9pt; break-inside: avoid; }
.livros b { color: #6E3AA7; }
.sw.simples-sw { background: #FFFFFF; border-color: #C3D8F8; border-left: 3pt solid #0B5BD3; }
.sw.aqui-sw { background: linear-gradient(90deg, #A9C4EE 0, #A9C4EE 45%, #0B5BD3 45%, #0B5BD3 70%, #DCDCE2 70%); border: 0; height: 4pt; border-radius: 2pt; }
.sw.exame-sw { background: #1F2933; border-color: #1F2933; }
.cmp .destaque { font-family: "Inter SemiBold"; color: #0B5BD3; }
.cmp.c4 .k { width: 62pt; }
.cmp.c4 .c { font-size: 8.3pt; padding-right: 8pt; }
.vesp { break-before: page; }
.vesp .item { display: flex; align-items: baseline; background: #FFFFFF; border: 1px solid #E3E3E8; border-radius: 12pt; padding: 7pt 12pt; margin: 0 0 6pt; break-inside: avoid; }
.vesp .item .prova { flex: none; margin: 0 9pt 0 0; }
.vesp .item p { margin: 0; font-size: 9.2pt; }
.tiles.t4 { margin: 6pt 0 8pt; }
.figure.lado { display: flex; align-items: center; }
.figure.lado > img { flex: none; }
.figure.lado .olhar { flex: 1; margin: 0 0 0 12pt; }
.cover .toc a { padding: 3.6pt 0; }
```
- A legenda da página 2 ganha as linhas dos blocos novos ("Em palavras simples", "Pegadinha do professor", "Você está aqui").
- Cores continuam com o mesmo significado da skill (azul aula, verde valor, vermelho alerta, laranja fala do professor, roxo complemento).

## Imagens

- **Exames (radiografia, tomografia, ultrassom): sempre dos slides, nunca de IA.** Recorte da página do PDF em boa resolução; setas e rótulos por cima, desenhados por nós; legenda "Imagem dos slides da aula".
- **Fluxogramas, tabelas, esquemas com setas**: SVG nosso, como manda a skill.
- **Ilustrações** (anatomia, técnica de procedimento, montagem de dreno): o Mauricio gera no ChatGPT a partir dos nossos prompts. Só quando a ilustração ensina melhor que um SVG ou a imagem do slide. Cada prompt:
  - estilo vetorial plano e limpo, fundo branco, **sem nenhum texto, letra ou número na imagem** (os rótulos em português vão por cima, feitos por nós);
  - paleta: azul-marinho #16315C, azul-claro #C3D8F8, cinzas suaves, pele em tom neutro; vermelho só se for sangue ou alerta;
  - formato horizontal 3:2 (ou o que a figura pedir), alta resolução;
  - a anatomia que precisa sair certa descrita com todas as letras no próprio prompt;
  - junto, a lista "o que conferir" na imagem que voltar.
