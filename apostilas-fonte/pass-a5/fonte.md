# Fonte da aula · pass-a5

Guardada com `scripts/fonte-aula.py` (última mudança em 13/11/2026). É o material da aula como veio, sem correção:
os erros da transcrição automática ficam aqui e quem corrige é a apostila. A apostila, as questões, os flashcards
e as conferências saem deste arquivo; onde ele e a apostila divergem, vale o que o professor falou (AGENTS.md).
Não edite à mão: para juntar material novo, rode o programa com --acrescentar.

## O que tem aqui

- Transcrição 1: `transcri_o_completa_da_aula_prof_felipe.md` (5.896 palavras, sem marcação de tempo).

## Transcrição 1 · transcri_o_completa_da_aula_prof_felipe.md
<!-- parte transcricao 1 | arquivo=transcri_o_completa_da_aula_prof_felipe.md | sha=baa121bd141a | palavras=5.896 -->

# Transcrição Completa da Aula — Epidemiologia Clínica (Prof. Felipe)

*[00:00 – 04:25] Conversas paralelas dos alunos em sala antes do início da aula.*

---

## 1. Abertura e Revisão da Aula Anterior (Tabela de Diagnóstico)

**Professor:** Vamos lá para a sala... tá bom, dá para ouvir? Precisa do microfone? Sim, precisa, né? Tá bom. Então, pessoal, boa tarde para vocês, bem-vindos aí. A gente não tinha aulas há umas três semanas, então já até me perdi aqui... Obrigado. Eu estou sem o meu passador. Eu não vou dar aula sentado, porque eu acho meio chato, mas a gente vai tocando um pouquinho da aula aqui... Opa, obrigado. Valeu.

Então assim, o que é importante da aula de hoje, enquanto eu vou colocando as coisas aqui: na última aula — vocês lembram, faz muito tempo, eu sei — a gente viu uma tabela específica que era sobre **diagnóstico**, certo? Então, na nossa tabela, nosso objetivo era encontrar quem que era verdadeiro positivo, quem que era falso positivo, verdadeiro negativo, falso negativo... Valeu. Aí, fechou.

Então a gente estava falando dessa tabelinha aqui: tabela de diagnóstico. Nosso objetivo era saber, se a gente tinha um teste, por exemplo... A gente tinha um teste e tinha uma doença, lembra? A "verdade" ficava aqui em cima: quem que realmente estava doente, quem que não estava doente, e como que o meu teste se saía para encontrar essa verdade, né? Então a gente calculava valor preditivo positivo, valor preditivo negativo, sensibilidade, especificidade, tá? E aí tem até aquela questão da prevalência, né?

Então, essa tabela aqui é da aula passada, tá? **Não confunde**, porque apesar das duas serem tabela $2 \times 2$, elas são completamente diferentes. Elas servem para coisas completamente diferentes. A única coisa que elas têm em comum é que as duas são tabela $2 \times 2$, tá? Você vai saber na hora o que fazer. Não tem como construir uma tabela de uma forma se os seus dados forem dados de uma tabela de diagnóstico, tá?

---

## 2. Tabela $2 \times 2$ de Exposição e Desfecho

**Professor:** O que a gente vai falar hoje é uma tabela de **exposição e desfecho**, tá? O que o pessoal gosta daquela tabela anterior? Sensibilidade, especificidade, como que os valores preditivos mudam de acordo com a prevalência da doença — por isso que os caras adoram. O que os caras gostam dessa tabela aqui? Tudo que a gente vai calcular hoje, tá? Todos os valores. E vocês vão ver que eles são uma construção, é como se fosse um passo a passo. Então você entende agora no começo, e as coisas vão fazendo sentido até o cálculo final, tá bom? Então beleza.

O que eu tenho aqui? Para montar essa tabela, eu tenho na minha **linha** exposição ou não exposição. Na minha **coluna**, eu tenho o **desfecho** que eu quero. Como assim? Se eu quero ver, por exemplo, se a minha medicação... como que ela se comporta em relação, por exemplo, ao tratamento de síndrome coronariana aguda, eu vou ver, por exemplo:
* **Exposição:** receber o meu remédio;
* Contra alguma coisa — **não exposição:** não receber o meu remédio.

E aí eu vou ver quantos pacientes, por exemplo, infartaram e quantos pacientes não infartaram em cada um dos quatro grupos, tá?

Então lembra que a gente chamava antes "ah, verdadeiro positivo, falso positivo..." Agora a gente vai chamar diferente. Agora a gente vai chamar:
* As pessoas que estão no **$A$**: dos **expostos** que tiveram o desfecho positivo;
* No **$B$**: os **expostos** que não tiveram o desfecho, ou seja, desfecho negativo;
* No **$C$**: os **não expostos** que tiveram o desfecho;
* E no **$D$**: os **não expostos** que não tiveram o desfecho.

Pensa o seguinte: vamos falando de medicamento para infarto, mas pensa o seguinte: **exposição**. Exposição comum: tabagismo, por exemplo, tá? Então eu coloco aqui: tabagistas. Meu desfecho: "ah, eu quero saber a relação de tabagismo com câncer de pulmão", fácil. Então o que eu coloco no meu desfecho positivo aqui? No meu grupo de pacientes, quem teve câncer de pulmão. Então o meu $A$ vai ser o exposto que teve desfecho: o tabagista que desenvolveu câncer de pulmão.

Pode uma pessoa fumar e nunca ter câncer de pulmão?

**Alunos:** Pode.

**Professor:** Pode. E no meu período de acompanhamento — às vezes o meu acompanhamento é por 5 anos — às vezes nem deu tempo de ela desenvolver o câncer de pulmão. Então, apesar de ela ser tabagista, ela não desenvolveu câncer de pulmão; ela tem o desfecho negativo ($B$).

Agora ao contrário: pode uma pessoa que nunca fumou ter câncer de pulmão? Pode também, por qualquer outro fator de risco ocupacional, por sei lá, metástase de alguma outra coisa e tal. Então beleza: apesar de ele nunca ter fumado — que é o que eu estou querendo saber, avaliar o tabagismo —, apesar de ele não ser tabagista, ele desenvolveu câncer de pulmão dentro da minha amostra. Então ele é o não exposto que teve desfecho positivo ($C$). E no $D$, o cara que não fuma e que não teve câncer de pulmão — espero que sejam todos vocês aqui na sala, né?

Então, essa tabela vai ser montada dessa forma. O enunciado vai te dar todas essas informações ou grande parte delas também, né? Ele vai falar que tem 200 pacientes com tabagismo e 100 tiveram câncer de pulmão, quanto que é o outro... aí você vai fazendo as continhas, tá? Então beleza.

---

## 3. Intervenção, Exposição, Fator de Risco e Desfechos

**Professor:** Então, **linhas**: intervenção, exposição ou fator de risco. Lembra que são três coisas diferentes:
1. Na **intervenção**, eu entrego a medicação, eu faço alguma coisa com o meu paciente — ensaio clínico, por exemplo, tem que ter uma intervenção.
2. **Exposição**, o paciente mesmo faz: ele fuma porque ele quer, eu não entreguei cigarro para ele.
3. E **fator de risco** é um risco: obesidade, diabetes, ou qualquer outra coisa que você queira avaliar, tá?

Então, a linha 1 vai sempre receber uma dessas coisas aqui: pacientes que receberam intervenção, fator de risco, característica que você quer examinar, exame positivo, pode ser, tá? E a linha 2 vai ser sempre o oposto: é o paciente que não fuma, sem fator de risco, ou às vezes que recebeu uma intervenção também, mas que é contrária à sua primeira linha. Como assim? Na tua primeira linha é o remédio novo; na tua segunda linha é o tratamento padrão, é o placebo, é nenhum tratamento, tá? Então tudo isso vai ser linha 1 e linha 2, tá?

Dá uma olhada: *"Remédio XYZ reduz infarto?"* Então, como eu posso construir isso aqui?
* **Linha 1:** tratamento com o remédio XYZ;
* **Linha 2:** tratamento com placebo, com tratamento padrão, nenhum tratamento, tá?
* **Desfecho:** ocorrência de infarto, tá?

Vamos montar e a gente conversa sobre algumas particularidades. Então, aqui é o jeito que eu te mostrei a tabela: exposto, não exposto, desfecho positivo e desfecho negativo. Então a gente vai tirar tudo isso e montar ela. Como é que a gente vai montar?
* Tratamento com a medicação na primeira linha.
* O que vem na segunda linha aqui? Tratamento com placebo, ou nenhum tratamento. Beleza, nesse caso aqui a gente falou "tratamento com placebo", né?
* Nessa coluna, o que eu quero ver de positivo? Ocorrência de infarto. Então vai ser ocorrência de infarto (ou infarto positivo, você bota do jeito que você quiser, mas ocorrência de infarto), e na segunda coluna vai não ocorrência de infarto, tá?

Então, a gente sempre monta assim. É mais fácil, tá? Dá para complicar? Dá para complicar se quiser brigar com a questão, tá? Se você, por exemplo, quiser falar que o que você está medindo é "redução de infarto", você poderia brigar com a questão e falar que quer colocar "redução de infarto positivo" aqui e "redução de infarto negativo". Vê como é meio travadão? "Redução de infarto negativo... não reduziu o infarto, então ele..." Então assim, **não briga com a questão**. Coloca sempre um desfecho, tá? O desfecho medido ali. Então se o desfecho é negativo, deixa ele sempre como infarto: infarto aconteceu, infarto não aconteceu, tá? É mais fácil.

### Exemplos Rápidos de Montagem

**Professor:** Dá uma olhada: **tabagismo e câncer de pulmão**, já até falamos disso, né? Montar a tabelinha:
* Linha 1: tabagista; Linha 2: não tabagista.
* Coluna 1: aconteceu câncer de pulmão (ocorrência de câncer de pulmão); Coluna 2: não ocorrência de câncer de pulmão. Beleza.

Vamos mais uma: **obesidade aumenta hipertensão?** Então beleza:
* O que seria na minha primeira linha? Obesos, tá?
* O que seria na minha segunda linha? Não obesos.
* O que iria nas minhas colunas? Desenvolvimento de hipertensão, não desenvolvimento de hipertensão, né? Ocorrência de hipertensão arterial sistêmica, não ocorrência de hipertensão, tá bom?

Mais uma, para finalizar: **cirurgia ou tratamento clínico em relação a óbitos**. Como é que a gente monta isso?
* Linha 1: cirurgia;
* Linha 2: tratamento clínico;
* Colunas: óbito positivo (ocorreu óbito) e óbito negativo (não ocorreu óbito). Então beleza, ocorrência de óbito. Tá tranquilo, né?

Porque assim, que nem na aula passada, o primeiro passo é montar. Se a gente montar errado, a gente vai fazer os cálculos errados, tá?

---

## 4. Desfechos Negativos vs. Desfechos Positivos e Primeiros Exemplos

**Professor:** Uma coisa que pode acontecer é que a gente está falando, por exemplo — é mais fácil quando a gente fala — de morte, infarto, AVC, sangramento, internação: **desfechos negativos**, tá? Então, quando a gente fala isso aqui, é tranquilo: você chega lá no final e calcula que o risco do teu paciente morrer é duas vezes maior no grupo de tabagista, ou o risco de desenvolver câncer de pulmão é três vezes maior.

Mas algumas vezes você pode estar olhando para um **desfecho positivo**. Às vezes você vai estar olhando para cura da doença — qual a incidência de cura da doença no teu grupo —, aumento de sobrevida, controle da pressão, tá? Então só verifica isso: se o teu desfecho for positivo, a gente vai fazer um cálculo que vai dar às vezes um risco de isso aqui ser bom, e às vezes não. Então a gente vai chegar no final e vai rever esse conceito aqui, mas já entenda que é possível calcular as duas coisas: coisas ruins (aumento do risco de sangramento, aumento do número de internações em um ano), mas pode ser aumento do tempo de alta hospitalar, melhora da pressão, piora da pressão, tá?

Dá uma olhadinha. Agora então vamos montar:
> *"Um estudo sobre a nova medicação, ocorrência de infarto. 200 pacientes foram acompanhados. No grupo de tratamento, 10 tiveram infarto e 90 não tiveram. No grupo placebo, 20 tiveram infarto e 80 não tiveram."*

Então zeramos aqui a nossa tabela, como é que a gente monta?
* Linha 1: nova medicação; Linha 2: placebo.
* Colunas: ocorrência de infarto e não ocorrência de infarto.
* No grupo nova medicação: 10 tiveram infarto e 90 não tiveram.
* No grupo placebo: 20 tiveram infarto e 80 não tiveram.

O que, olhando assim só por cima, parece para vocês aqui?

**Alunos:** Que a nova medicação é boa / tem algum efeito.

**Professor:** A nova medicação tem algum efeito, né? Parece, né? Pelo menos olhando por cima, parece que ela tem algum efeito. Esse grupo aqui, placebo, por que que ele infartou?

**Alunos:** Porque já ia infartar.

**Professor:** É porque ele já ia infartar de qualquer forma! Esse grupo placebo aqui não está recebendo nenhum tratamento. Esse grupo aqui é a população; esse grupo é o paciente que não recebe remédio, tá? Ele infartou porque, na história dessa população, duas a cada 10 pessoas vão infartar. E está tudo bem, essa é a história dessa população. Eu estou desenvolvendo um remédio para tentar mudar isso. Parece que eu consegui? Ah, olhando por cima parece que sim, né? De números brutos aqui, de 20 eu passei para 10.

Às vezes você vai receber assim, né: *"100 receberam o novo tratamento, 100 receberam placebo"*. Coloca o totalzinho lá na ponta: nova medicação 100, placebo 100. No grupo de tratamento, 10 tiveram infarto ($100 - 10 = 90$); no grupo placebo, 20 tiveram infarto ($100 - 20 = 80$). Então a tabelinha ou vai te trazer todos os dados ou vai te trazer os números totais para você subtrair, tá bom?

### Exemplo: Novo Programa de Acompanhamento na Hipertensão

**Professor:** Diferente agora:
> *"Um estudo avaliou se um novo programa de acompanhamento melhora o controle da pressão arterial em pacientes hipertensos. Foram avaliados 200 pacientes, 100 em cada grupo. No grupo do programa, 70 pacientes tiveram controle de pressão. No grupo habitual, 50 pacientes tiveram controle de pressão."*

Vê que agora o desfecho positivo é um desfecho bom, né? É controle de pressão.
* Linha 1: novo programa; Linha 2: tratamento habitual.
* Coluna 1: controle da pressão; Coluna 2: não controle.
* Totais: 100 e 100.
* No grupo do programa: 70 tiveram controle (e 30 não).
* No grupo habitual: 50 tiveram controle (e 50 não).

O que essa tabela responde para a gente olhando por cima? Parece que melhora a pressão! Porque se o tratamento habitual é a nossa população hipertensa, metade delas já ia controlar a pressão com o tratamento habitual (medicação, exercício, dieta). O meu programa é novo, tem mais exercício físico, tem remédio que não está disponível no SUS e tal, e subiu de 50 para 70. Então é isso que a gente quer ver: qual que é a chance, qual que é o risco de controlar a pressão desse paciente em relação ao outro paciente.

---

## 5. Risco Absoluto ($RA$) e Risco Relativo ($RR$)

**Professor:** Agora a gente entra nas contas, tá? E não, vocês não podem levar calculadora para a prova, tá bom? Eu vou ser honesto, eu também sou péssimo em matemática, os números vão ser agradáveis, tá? Mas não tem como, cara: você vai fazer prova de residência, vai cair isso aqui, você tem que saber fazer, tá?

Olha lá aquele nosso grupo de infarto: nova medicação (10 infartos, 90 não; total 100) e placebo (20 infartos, 80 não; total 100). Qual que é o risco de uma pessoa infartar estando no meu grupo que está usando a medicação?

**Alunos:** 10%.

**Professor:** 10% de lata assim, mas como é que você chega nessa conta? Só para a gente entender o raciocínio — porque aqui é tranquilo, né, mas e se eu tivesse 78 pacientes num grupo de 260? A gente está falando aqui de **Risco Absoluto do grupo**, tá? Presta atenção: risco absoluto do grupo, porque lá para frente a gente vai falar de uma outra coisa que usa o mesmo nome "absoluto". Aqui é o risco de um paciente desenvolver o que eu estou observando dentro daquele grupo.

Como é que eu vou fazer isso? Vou pegar o número de pessoas que tiveram o meu desfecho e dividir pelo número de participantes do meu grupo:
* Grupo medicação: $\frac{10}{100} = 0,10 = 10\%$.
* Cada grupo vai ter seu próprio risco absoluto. Qual que é o risco do grupo que não usou medicação (placebo)? $\frac{20}{100} = 0,20 = 20\%$.

Até aqui está tudo bem? Porque todas as contas vão partir desses dois números que a gente calculou. Se errar a conta aqui, vai errar até o final.

Quando eu quero saber se o tratamento reduziu o risco, eu posso olhar para os dois e falar: "Ah, reduziu, está na cara". Mas eu quero responder **quanto**! Quanto que o tratamento reduziu do risco? Existe um risco que a gente chama de **Risco Relativo ($RR$)**, tá? Como é que eu vou calcular esse risco relativo? Eu vou pegar o meu risco no meu grupo de intervenção e vou dividir pelo risco no meu grupo de controle:

$$
RR = \frac{RA_{\text{intervenção}}}{RA_{\text{controle}}}
$$

Esse é o risco relativo: **quantas vezes** o meu risco foi maior ou menor em um grupo em relação ao outro, tá? Vamos fazer a conta: se no meu grupo de tratamento eu tenho $10\%$ ($0,10$) e no meu grupo de placebo eu tenho $20\%$ ($0,20$), qual vai ser o meu risco relativo?

$$
RR = \frac{0,10}{0,20} = 0,5
$$

O que eu faço com esse $0,5$? Isso aqui me dá em porcentagem? Não! Isso aqui me dá em risco relativo. E aonde que a gente já viu risco relativo anteriormente? Nas nossas aulas de interpretação de artigos: menor do que $1$ é proteção, maior do que $1$ é risco! De onde que vem essa conta desse número que antes você só decorou? Agora você está entendendo como é que chega lá.

Se eu cheguei num risco relativo de $0,5$ aqui, a minha medicação é fator de risco ou fator de proteção para o meu desfecho?

**Alunos:** Fator de proteção.

**Professor:** Fator de proteção para o meu desfecho. O meu paciente teve $0,5$ vezes a chance de desenvolver o meu desfecho. Isso é meio estranho de falar ("pô, $0,5$ vezes", ninguém fala isso), mas quando a gente chega em riscos relativos maiores do que $1$ — $1,8$; $2$; $3$; $5$ — aí começa a fazer bastante sentido, né? "O risco de infartar é 5 vezes maior sem a medicação".

Vocês já sabem:
* Se o $RR = 1$, não tem diferença entre os grupos (os valores dos dois grupos são iguais, por exemplo, 10 infartos em um e 10 infartos no outro).
* Quando que vai dar menor do que $1$? Quando o risco for menor no grupo intervenção.
* E quando que ele vai dar maior do que $1$? Quando o risco no grupo de intervenção for maior.

"Ué, pode dar maior do que $1$? Eu posso ter uma medicação que vai causar alguma coisa ruim para o meu paciente?" Claro que sim! E a gente vai ver um monte delas hoje. Putz, eu vou usar AAS para prevenir infarto: beleza, o risco relativo para prevenir infarto dele vai dar menor do que $1$. E o risco relativo para sangramento dele? Será que uma pessoa que usa AAS sangra mais ou menos que a pessoa que não usa AAS? Sangra mais! Então as medicações, as intervenções, vão ter um risco relativo para cada coisa que for importante para ela. Não dá para olhar só para um desfecho para ter certeza. Lembra aquele estudo da vitamina C e ramipril? Eles testaram morte, infarto, morte cardiovascular... o ramipril era bom em todas elas, e a vitamina C não deu diferença em nenhuma.

### Cuidado com a Interpretação do Desfecho

**Professor:** Deu menor do que $1$, é bom ou ruim? Depende do teu desfecho, né?
* Se o teu desfecho é **infarto** e deu $0,5$: reduziu o risco de infarto (bom).
* Se o teu desfecho é **cura** e deu $0,5$: quer dizer que o meu paciente tem $0,5$ vezes a chance de se curar em relação ao outro — putz, que merda, né, cara? Reduz a sua chance de cura!
* Se o teu desfecho é **sobrevida** e deu $RR < 1$: menos sobrevida!

Então não existe "Ah, $RR < 1$ é sempre bom, $RR > 1$ é sempre ruim". Não é assim:
* $RR < 1$ para um desfecho ruim $\rightarrow$ ótimo (menos incidência do desfecho ruim).
* $RR < 1$ para um desfecho bom $\rightarrow$ ruim (menos incidência do desfecho bom).

---

## 6. Exercícios de Fixação ($RA$ e $RR$)

### Exercício 1: Tabagismo e Câncer de Pulmão

**Professor:** Vamos lá de novo:
> *"Um estudo comparou 200 indivíduos para avaliar a associação entre tabagismo e câncer de pulmão. 100 eram fumantes, 100 não eram fumantes. Entre os fumantes, 30 tiveram câncer; entre os não fumantes, 5 tiveram câncer."*

* Linha 1: fumantes (30 com câncer, 70 sem câncer; total 100).
* Linha 2: não fumantes (5 com câncer, 95 sem câncer; total 100).
* Risco absoluto de câncer nos fumantes: $\frac{30}{100} = 0,30$ ($30\%$).
* Risco absoluto de câncer nos não fumantes: $\frac{5}{100} = 0,05$ ($5\%$).
* Risco relativo: $\frac{0,30}{0,05} = 6$.

O que significa esse $6$? Tabagistas têm **6 vezes mais risco** de desenvolver câncer de pulmão em relação a não tabagistas. As contas são sempre com base no primeiro grupo (exposição/intervenção).

### Exercício 2: Novo Programa e Controle da Pressão

**Professor:** Aquela mesma tabelinha que a gente já montou do novo programa de hipertensão:
* Risco absoluto de controle de pressão no grupo novo programa: $\frac{70}{100} = 0,70$ ($70\%$).
* Risco absoluto de controle de pressão no programa habitual: $\frac{50}{100} = 0,50$ ($50\%$).
* Risco relativo: $\frac{0,70}{0,50} = 1,4$.

Interpretação: a chance (ou probabilidade) de controlar a pressão no grupo de intervenção foi $1,4$ vezes maior do que no grupo do programa habitual.

### Exercício 3 e 4: Novo Anticoagulante (Sangramento vs. AVC)

**Professor:** Anticoagulante e risco de sangramento:
> *"Novo anticoagulante: 24 sangramentos num total de 150 pacientes. Tratamento anticoagulante padrão: 30 sangramentos num total de 300 pacientes."*

* Risco absoluto no novo anticoagulante: $\frac{24}{150} = 0,16$ ($16\%$).
* Risco absoluto no anticoagulante padrão: $\frac{30}{300} = 0,10$ ($10\%$).
* Risco relativo: $\frac{0,16}{0,10} = 1,6$.

O que significa $1,6$ nesse contexto? O risco de sangramento de uma pessoa que está usando o novo anticoagulante é $1,6$ vezes maior do que o risco de uma pessoa que está sob o tratamento padrão.

Agora, o **mesmo anticoagulante** para ver o risco de **AVC**:
> *"Novo anticoagulante: 10 AVCs em 200 pacientes. Anticoagulante padrão: 25 AVCs em 200 pacientes."*

* Risco absoluto no novo anticoagulante: $\frac{10}{200} = 0,05$ ($5\%$).
* Risco absoluto no grupo padrão: $\frac{25}{200} = 0,125$ ($12,5\%$).
* Risco relativo: $\frac{0,05}{0,125} = 0,4$.

Agora, para prevenir ocorrência de AVC, ele é bom: a pessoa que usa o anticoagulante novo tem $0,4$ vezes o risco de ter AVC em relação a quem não usa.

---

## 7. Redução Relativa do Risco ($RRR$) e Redução Absoluta do Risco ($RAR$)

**Professor:** Por que eu falei que você tinha que cuidar com o risco absoluto do grupo? Porque agora vem um carinha chamado **Redução Absoluta do Risco ($RAR$)** e a **Redução Relativa do Risco ($RRR$)**, tá? A gente usa siglas: $RR$ (risco relativo), $RRR$ (redução relativa do risco) e $RAR$ (redução absoluta do risco).

Vamos voltar de novo lá no infarto:
* Risco absoluto na medicação: $10\%$.
* Risco absoluto no placebo: $20\%$.
* Risco relativo: $0,5$.

Agora eu quero saber: **proporcionalmente**, quanto que o risco caiu ($RRR$), e em **pontos percentuais**, quanto que o risco caiu ($RAR$)?

### Redução Relativa do Risco ($RRR$)

**Professor:** A redução relativa do risco vai ser $1 - RR$:

$$
RRR = 1 - RR
$$

Quanto que é o meu risco relativo? $0,5$. Quanto vai ser a minha $RRR$? $1 - 0,5 = 0,5$, ou seja, **$50\%$**! No Medcurso, pelo menos, a primeira vez que eu vi isso aqui, os caras tinham um mnemônico para você lembrar, que era pegar o microfone bem pertinho assim e falar: *"Não precisa fazer conta!"* Por que não precisa fazer conta? Porque vai ser só o quanto eu preciso para chegar em $1$, tá?
* Meu $RR$ é $0,3 \rightarrow RRR = 70\%$.
* Meu $RR$ é $0,95 \rightarrow RRR = 5\%$.
* Meu $RR$ deu $0,99 \rightarrow RRR = 1\%$.
* Deu $0,2 \rightarrow RRR = 80\%$.

*(Nota sobre dúvida de aluno: quando o $RR > 1$, não falamos em redução, falamos em **Aumento Relativo do Risco**, onde a conta é $RR - 1$).*

### Redução Absoluta do Risco ($RAR$) e Explicação Gráfica

**Professor:** Agora eu quero calcular isso em **pontos percentuais** ($RAR$). Para fazer em pontos percentuais, eu vou pegar o risco no grupo controle e diminuir do risco no grupo intervenção. O meu jeito de memorizar isso aqui era fazer o mnemônico $R - A - R$: o maior risco menos o menor risco ($RA_{\text{maior}} - RA_{\text{menor}}$).

Qual que é o maior risco absoluto aqui? $20\%$. Qual que é o menor risco absoluto aqui? $10\%$. $20 - 10 = 10$ **pontos percentuais**!

Os dois são redução, mas eu não entendi: por que eu vou usar um, por que eu vou usar outro? Dá uma olhadinha nesse gráfico:
* Se eu não tratar meus pacientes (placebo/população), $20\%$ têm chance de infartar e $80\%$ **não vão infartar de nenhum jeito**, você tratando ou não tratando.
* Se eu tratar meus pacientes, $10\%$ ainda infartam apesar do tratamento.
* Ou seja, o meu tratamento está mexendo **só nessa faixa entre $20\%$ e $10\%$**!

Quando eu olho só para as pessoas que infartaram ($20\%$ vs. $10\%$), o meu remédio reduziu em **$50\%$** os infartos ($RRR = 50\%$). Mas em relação a toda a população tratada (descontando os $80\%$ que já não iam infartar mesmo sem tratamento), a redução real foi de **10 pontos percentuais** ($RAR = 10\text{ p.p.}$).

Concorda que às vezes a indústria farmacêutica vai pegar e vai te falar: *"Cara, o remédio é muito bom, ele reduziu em $90\%$ a ocorrência dessa complicação!"* Você fala: *"Caralho, $90\%$ a ocorrência dessa complicação, esse remédio é maravilhoso!"* Aí você vai ver: a complicação base é $0,05\%$. Reduziu em $90\%$ de $0,05\%$, foi para $0,005\%$. Já era uma coisa tão rara de acontecer na minha população inteira — vale a pena eu gastar para fazer um tratamento? Então é isso que eu quero que vocês entendam: $RRR$ fala proporcionalmente em relação ao outro grupo; $RAR$ fala em pontos percentuais em relação ao todo. E tem mais uma coisa: esse carinha aqui, a $RAR$, vai ser o resultado que a gente vai usar na próxima conta.

### Exercício: Novo Medicamento e Risco de AVC

**Professor:** Vamos lá:
> *"Um estudo avaliou se um novo medicamento reduz o risco de AVC em 400 pacientes: 200 receberam o novo, 200 receberam placebo. 20 tiveram AVC no grupo novo, 40 tiveram AVC no placebo."*

* Risco absoluto no grupo nova medicação: $\frac{20}{200} = 10\%$.
* Risco absoluto no grupo placebo: $\frac{40}{200} = 20\%$.
* Risco relativo: $\frac{10\%}{20\%} = 0,5$.
* $RRR$: $1 - 0,5 = 50\%$.
* $RAR$: $20\% - 10\% = 10\text{ pontos percentuais}$.

---

## 8. Número Necessário para Tratar ($NNT$) e Número Necessário para Causar Dano ($NNH$)

**Professor:** E aí a gente chega no último cálculo: **$NNT$**. Quando eu estava no quarto ano de faculdade, tinha uma daquelas provas semestrais com duas questões abertas, e uma pedia para dizer em 10 linhas o que é $NNT$.

$NNT$: **Número Necessário para Tratar** (*Number Needed to Treat*). Na contrapartida, existe o **$NNH$**, Número Necessário para Causar Dano (*Number Needed to Harm*), que vem das contas com risco maior.

O que é esse $NNT$? Quantos pacientes eu preciso tratar (quantos pacientes precisam passar pela intervenção) para que eu evite **1** desfecho! "Putz, mas então não é todo mundo que eu tratar com aspirina que vai reduzir o infarto?" Exato! Não são todos os pacientes que eu tratar com aspirina que vão evitar o infarto, mas eu tenho um número de pacientes que eu preciso tratar para que **um deles** se beneficie.

Como que eu calculo isso?

$$
NNT = \frac{1}{RAR}
$$

No nosso exemplo do infarto, chegamos em $RAR = 10\text{ pontos percentuais}$ ($0,10$):

$$
NNT = \frac{1}{0,10} = 10
$$

O que esse $NNT$ de $10$ me diz? Que eu preciso tratar **10 pacientes** para evitar **1 infarto**. Qual seria o $NNT$ perfeito? $1$ para $1$ ($NNT = 1$). A gente tem $NNT$ de $1$? Não, não existe, é que nem sensibilidade e especificidade de $100\%$ ao mesmo tempo. Mas a gente tem $NNT$s muito bons — por exemplo, antibióticos endovenosos de uso hospitalar têm $NNT$ de $1,2$ ou $1,5$. Quanto menor o $NNT$, maior o impacto.

E tudo vai depender do contexto clínico: o $NNT$ vai ser sempre comparado com o $NNH$ (quantos pacientes eu preciso tratar para ter um evento adverso). Dá uma olhada nessa medicação de verdade:
1. **Caso 1:** $NNT$ para evitar um infarto $= 77$; $NNH$ para causar sangramento $= 400$.
   * A cada 77 pacientes eu evito um infarto; a cada 400 pacientes tratados eu causo um sangramento. Parece bom! Essa medicação é a **Aspirina (AAS)** na **prevenção secundária** (para o meu vozinho que já infartou ou já teve AVC). Eu dou aspirina para o meu paciente pós-infarto? Todos eles!
2. **Caso 2:** $NNT$ para evitar infarto $= 333$; $NNH$ para causar um sangramento $= 250$.
   * A cada 333 pacientes tratados eu evito 1 infarto, mas a cada 250 pacientes eu causo 1 sangramento! Parece uma boa medicação para usar agora? Não! Que remédio é esse? A mesma **Aspirina**, só que usada na **prevenção primária** (para velho que nunca infartou, que nunca teve AVC)!

Então você vê: mesmo remédio, populações diferentes. Na prevenção primária não tem benefício líquido; na prevenção secundária usa! Uma decisão clínica depende do equilíbrio do benefício e do dano, como quase tudo na medicina.

### Exercício: Mobilização Precoce e Pneumonia Pós-Operatória

**Professor:** Dá uma olhadinha:
> *"Estudo avaliou se o protocolo de mobilização precoce no pós-operatório reduz o risco de pneumonia hospitalar em pacientes internados após cirurgia abdominal. Foram avaliados 250 pacientes no grupo mobilização e 400 no grupo cuidado habitual. No grupo mobilização, 20 tiveram pneumonia; no grupo cuidado habitual, 64 tiveram pneumonia."*

* Risco absoluto no grupo mobilização: $\frac{20}{250} = 0,08$ ($8\%$).
* Risco absoluto no cuidado habitual: $\frac{64}{400} = 0,16$ ($16\%$).
* Risco relativo: $\frac{0,08}{0,16} = 0,50$.
* Redução do risco relativo ($RRR$): $50\%$.
* Redução absoluta do risco ($RAR$): $0,16 - 0,08 = 0,08$ ($8\text{ pontos percentuais}$).
* $NNT$: $\frac{1}{0,08} = 12,5$.

Ou seja, interpreta para mim: quantos pacientes eu preciso tratar para evitar uma pneumonia?

**Alunos:** 13!

**Professor:** **13 pacientes**, né, porque eu não tenho meio paciente! Eu preciso tirar 13 pacientes da cama depois de cirurgia abdominal para evitar que um deles tenha pneumonia.

---

## 9. Revisão Geral das Medidas de Risco e Questões Rápidas

**Professor:** Revisãozinha dos conceitos que a gente viu até agora antes de entrar no assunto mais chato da aula:
* **Risco Absoluto ($RA$):** proporção de indivíduos que teve o desfecho em cada grupo ($\text{eventos} / \text{participantes de cada grupo}$).
* **Risco Relativo ($RR$):** risco do desfecho no grupo intervenção comparado ao grupo controle ($RA_{\text{intervenção}} / RA_{\text{controle}}$).
* **Redução Relativa do Risco ($RRR$):** diferença proporcional de um grupo em relação ao outro ($1 - RR$).
* **Redução Absoluta do Risco ($RAR$):** diferença em pontos percentuais entre o risco do grupo controle e o do grupo tratamento ($RA_{\text{maior}} - RA_{\text{menor}}$).
* **Número Necessário para Tratar ($NNT$):** quantos pacientes têm que receber a intervenção para evitar um evento ($1 / RAR$).

### Questões Rápidas

1. **Náuseas após uso de novo medicamento:** 18 eventos em 100 pacientes no grupo novo medicamento. Qual o risco absoluto? $\frac{18}{100} = 18\%$.
2. **Privação de sono e cefaleia:** Grupo que dorme $< 6\text{ horas}$ tem $30\%$ de cefaleia; grupo que dorme $\ge 6\text{ horas}$ tem $10\%$. Qual o $RR$? $\frac{0,30}{0,10} = 3$.
3. **Insuficiência cardíaca e internação:** Nova medicação ($10/100 = 10\%$) vs. Placebo ($25/100 = 25\%$).
   * $RR = \frac{0,10}{0,25} = 0,4$.
   * $RRR = 1 - 0,4 = 60\%$.
   * $RAR = 25\% - 10\% = 15\text{ pontos percentuais}$.
4. **Risco de um evento caiu de $8\%$ no controle para $4\%$ na intervenção:**
   * $RAR = 8 - 4 = 4\text{ pontos percentuais}$.
   * $RRR = 50\%$.
5. **Tratamento reduziu o risco de $12\%$ no controle para $8\%$ no tratamento. Qual o $NNT$?**
   * $RAR = 12\% - 8\% = 4\text{ p.p.}$ ($0,04$).
   * $NNT = \frac{1}{0,04} = 25\text{ pacientes}$.

---

## 10. Estudos de Caso-Controle: *Odds* e *Odds Ratio* ($OR$)

**Professor:** Tem mais uma conta que vocês vão ter que saber fazer, tá? Porque eles gostam de cobrar especificamente esse cálculo nas provas. Até agora eu estava falando de **estudos de coorte** e **ensaios clínicos**, porque esses estudos vão medir **risco** — o risco de uma coisa acontecer no futuro.

Mas nos **estudos de caso-controle**, eu parto de onde e vou para onde? Eu parto da **doença que já aconteceu** e eu olho a **exposição** no passado! Qual que é o risco de uma pessoa desenvolver a doença que ela já tem? Não faz sentido fazer essa pergunta, ela já tem a doença! Então eu **não posso falar de risco** em estudos de caso-controle.

Quando a gente fala em caso-controle, eu falo em ***Odds*** e ***Odds Ratio*** (a tradução mais próxima é **chance** e **razão de chances**, embora a maior parte dos lugares use *Odds* e *Odds Ratio* mesmo). É a única fórmula que o caso-controle vai te dar.

O que eu quero saber com o *Odds Ratio*? Para cada paciente sem o evento, quantos tiveram o evento. Vamos montar a tabela $2 \times 2$:
* **Linha 1:** Fumantes ($A = 80$ com câncer de pulmão; $B = 40$ sem câncer de pulmão).
* **Linha 2:** Não fumantes ($C = 20$ com câncer de pulmão; $D = 60$ sem câncer de pulmão).

Calculando por partes:
* *Odds* nos fumantes: $\frac{80}{40} = 2$.
* *Odds* nos não fumantes: $\frac{20}{60} = 0,33$.
* *Odds Ratio* ($OR$): $\frac{2}{0,33} = 6$.

A conta que a gente está fazendo, no final das contas, é $\frac{A / B}{C / D}$. E aí passaram aquele mnemônico do **"Peixinho"**: você pega e multiplica cruzado! Multiplica $A \times D$ e divide por $B \times C$:

$$
OR = \frac{A \times D}{B \times C}
$$

Aí fica mais agradável: você faz $80 \times 60$ ($4.800$) e divide por $40 \times 20$ ($800$). Corta os zeros: $\frac{48}{8} = 6$!

Interpretação: a razão de chances de câncer de pulmão é $6$ vezes maior no grupo fumante do que no grupo não fumante (a chance de você encontrar um paciente com câncer de pulmão no grupo de fumantes é $6$ vezes mais frequente do que no grupo não fumante).

### Exemplos Resolvidos de *Odds Ratio*

#### Exemplo 1: Uso de Telas Antes de Dormir e Insônia

**Professor:**
> *"Estudo avaliou a associação entre uso de telas antes de dormir e insônia. 60 pessoas usavam telas antes de dormir e 30 apresentavam insônia. 40 pessoas não usavam telas antes de dormir e 10 apresentavam insônia."*

Eu estou falando de risco de desenvolver insônia? Não, elas já têm insônia!
* **Usam telas (60):** 30 com insônia ($A$), 30 sem insônia ($B$).
* **Não usam telas (40):** 10 com insônia ($C$), 30 sem insônia ($D$).

Fazendo pelo "peixinho":

$$
OR = \frac{30 \times 30}{30 \times 10} = \frac{900}{300} = 3
$$

Entre os participantes que usavam telas, a chance de apresentar insônia foi $3$ vezes maior do que entre os que não usavam telas.

#### Exemplo 2: Consumo Frequente de Energéticos e Palpitação

**Professor:** Acho que esse é o último:
> *"Estudo avaliou a associação entre consumo frequente de energéticos e palpitação. Qual é o Odds Ratio?"*

Dados da tabela: $A = 9$, $B = 141$, $C = 6$, $D = 294$:

$$
OR = \frac{9 \times 294}{141 \times 6} = \frac{2.646}{846} \approx 3,12\text{ (ou }3,13\text{)}
$$

---

## 11. Encerramento

**Professor:** Esse site aqui, **`thennt.com`**, é de onde a gente tira essas informações clínicas: eles fazem um apanhadão de várias medicações onde você pode botar o nome do remédio que você quer — por exemplo, aspirina na prevenção de doença cardiovascular — e ele fala os benefícios ($NNT$) e os danos ($NNH$).

Beleza, pessoal! Bom ter vocês de volta. Isso é tudo por hoje. Obrigado pelo presente! Bom dia para vocês.
