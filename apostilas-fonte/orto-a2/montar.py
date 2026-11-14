from pathlib import Path
from html import escape
from PIL import ImageFont
import re

ROOT = Path(__file__).resolve().parent
font = ImageFont.truetype(str(ROOT / 'fonts/Inter-Regular.ttf'), 10)

def svg_text(s, x, y, width, size=10, color='#1F2933', bold=False):
    f = ImageFont.truetype(str(ROOT / ('fonts/Inter-SemiBold.ttf' if bold else 'fonts/Inter-Regular.ttf')), size)
    lines, current = [], ''
    for word in s.split():
        test = (current + ' ' + word).strip()
        if current and f.getlength(test) > width:
            lines.append(current); current = word
        else:
            current = test
    lines.append(current)
    return ''.join(f'<text x="{x}" y="{y+i*size*1.5}" font-family="Inter" font-size="{size}" fill="{color}" font-weight="{600 if bold else 400}">{escape(line)}</text>' for i,line in enumerate(lines))

def rect(x,y,w,h):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="white" stroke="#C3D8F8"/>'

def arrow(x,y):
    return f'<path d="M{x} {y}v12" stroke="#8AA9DF" stroke-width="2"/><polygon points="{x-4},{y+10} {x+4},{y+10} {x},{y+16}" fill="#8AA9DF"/>'

def make_svg(name,height,body):
    (ROOT/name).write_text(f'<svg xmlns="http://www.w3.org/2000/svg" width="478" height="{height}" viewBox="0 0 478 {height}">{body}</svg>')

labels = ['01 Base da doença','02 Clínica e eixos','03 Imagem','04 Tratar o paciente','05 Quadril','06 Joelho e polegar','07 Ombro','08 Coluna']
body=''
for i,label in enumerate(labels):
 x=2+(i%4)*119; y=2+(i//4)*43
 body+=rect(x,y,113,36)+svg_text(label,x+9,y+16,97,9,bold=True)
make_svg('trilha.svg',82,body)
body=''
for i,(title,desc) in enumerate([
    ('Amolecimento','A cartilagem perde sua consistência.'),
    ('Fibrilação','A superfície se desorganiza em fibras.'),
    ('Destacamento','Partes se separam do osso subcondral.'),
    ('Erosão','A perda de cartilagem expõe o osso.')]):
    x=2+i*120
    body+=rect(x,2,112,82)+svg_text(str(i+1)+'. '+title,x+7,19,100,8,bold=True)+svg_text(desc,x+7,39,97,8.5)
    if i<3: body+=f'<polygon points="{x+114},38 {x+118},42 {x+114},46" fill="#8AA9DF"/>'
make_svg('cartilagem.svg',87,body)
body=rect(99,2,280,45)+svg_text('Avaliar a função do manguito rotador',110,22,260,10,bold=True)
body+='<path d="M239 47v15H116v14M239 62H362v14" fill="none" stroke="#8AA9DF" stroke-width="2"/>'
for x,title,lines in [(2,'Manguito funcional',['Biomecânica preservada','Prótese anatômica','Cabeça no úmero; cavidade na glenoide']), (248,'Manguito insuficiente',['Biomecânica comprometida','Prótese reversa','Esfera na glenoide; cavidade no úmero'])]:
    body+=rect(x,77,228,128)+svg_text(title,x+12,98,205,10,bold=True)
    for j,line in enumerate(lines): body+=svg_text(line,x+12,120+j*24,204,9)
body+=svg_text('Na prótese reversa, o deltoide passa a ter papel central no movimento.',10,225,456,9)
make_svg('ombro.svg',243,body)
body=rect(109,2,260,44)+svg_text('Dor na coluna: história e exame neurológico',120,20,237,10,bold=True)
body+='<path d="M239 46v16H77v12M239 62v12M239 62H401v12" fill="none" stroke="#8AA9DF" stroke-width="2"/>'
paths=[('Alteração perineal ou esfincteriana','Suspeitar de compressão da cauda equina.','Atendimento urgente'),('Déficit neurológico progressivo','A função neurológica pode indicar cirurgia.','Avaliação especializada'),('Dor refratária, instabilidade ou estenose','Avaliar a indicação e a estratégia cirúrgica.','Conduta individualizada')]
for i,(a,b,c) in enumerate(paths):
    x=2+i*160
    body+=rect(x,77,152,68)+svg_text(a,x+10,98,132,10,bold=True)+arrow(x+76,146)
    body+=rect(x,164,152,62)+svg_text(b,x+10,186,132,9)+arrow(x+76,227)
    body+=rect(x,245,152,40)+svg_text(c,x+10,263,132,9,bold=True)
make_svg('coluna.svg',288,body)

def p(s): return '<p>'+s+'</p>'
def h(s,prova=False): return '<h3 data-bm="'+escape(s)+'">'+s+(' <span class="prova">PROVA</span>' if prova else '')+'</h3>'
def box(title,text,color=''): return '<div class="box '+color+'"><div class="kick"><span class="dot"></span>'+title+'</div>'+p(text)+'</div>'
def quote(text,ctx): return '<div class="quote"><p>“'+text+'”</p><div class="who">Dr. Gustavo Colombo · '+ctx+'</div></div>'
def ul(items): return '<ul>'+''.join('<li>'+x+'</li>' for x in items)+'</ul>'
def flow(items): return '<ol class="flow">'+''.join('<li>'+x+'</li>' for x in items)+'</ol>'
def rows(items,terms=False):
    # Keep small groups so that long atomic blocks do not strand text.
    out=''
    for i in range(0,len(items),3):
        out+='<div class="rows'+(' terms' if terms else '')+'">'+''.join('<div class="row"><div class="k">'+a+'</div><div class="v">'+b+'</div></div>' for a,b in items[i:i+3])+'</div>'
    return out
def compare(headers,items):
    return '<div class="cmp"><div class="r h"><div class="k"></div>'+''.join('<div class="c">'+x+'</div>' for x in headers)+'</div>'+''.join('<div class="r"><div class="k">'+a+'</div>'+''.join('<div class="c">'+x+'</div>' for x in bs)+'</div>' for a,*bs in items)+'</div>'
def fig(name,alt): return '<div class="figure"><img src="'+name+'" alt="'+escape(alt)+'"></div>'
def sec(n,title,simple,body):
    stage=min(n,8)
    bar='<div class="aqui">'+''.join('<span class="'+('on' if i+1==stage else 'feito' if i+1<stage else '')+'">'+x[3:]+'</span>' for i,x in enumerate(labels))+'</div>'
    return f'<section id="s{n:02d}"><div class="sec-head"><span class="num">{n:02d}</span><h2>{title}</h2></div>'+bar+'<div class="simples">'+p('<b>Em palavras simples.</b> '+simple)+'</div>'+body+'</section>'

sections=[]
sections.append(sec(1,'O que é a artrose',
 'O revestimento que ajuda a articulação a deslizar e distribuir a carga vai se deteriorando. Com o tempo, outras estruturas também se alteram, e o movimento pode ficar doloroso e limitado.',
 h('O ponto de partida é a cartilagem',True)+
 p('A artrose, também chamada osteoartrite ou osteoartrose, é uma doença degenerativa e progressiva. O foco inicial do raciocínio é a <b>cartilagem articular</b>; as alterações ósseas aparecem como parte das consequências do processo. É a doença articular crônica mais comum e pode reduzir a qualidade de vida, a amplitude dos movimentos e a capacidade funcional, sobretudo no idoso com pouca reserva muscular.')+
 box('Pegadinha do professor','Não confundir artrose com perda de densidade mineral óssea. A densitometria óssea não é o exame usado para investigar a artrose.','red')+
 compare(['Primária','Secundária'],[
 ('Causa','Idiopática: não se identifica um fator causal único.','Relacionada a uma causa reconhecível.'),
 ('Exemplos','Forma mais comum; destacam-se mulheres após os 55 anos.','Trauma, deformidade prévia, artrite reumatoide, infecção, doenças metabólicas, da sinóvia ou do desenvolvimento.')])+
 h('Fatores associados')+
 ul(['<b>Idade e genética.</b> A ocorrência antes dos 35 anos foi apresentada como rara. A predisposição hereditária participa de um processo multifatorial.',
 '<b>Sexo e hormônios.</b> A queda do estrogênio após a menopausa interfere no metabolismo dos condrócitos, que possuem receptores hormonais. Alterações do osso subcondral também podem contribuir indiretamente.',
 '<b>Traumas e displasias.</b> Uma fratura consolidada com deformidade ou uma articulação com desenvolvimento anormal modifica a distribuição da carga.',
 '<b>Peso e atividade física.</b> A aula discutiu obesidade, excesso de exercício e inatividade como possíveis participantes, com ressalvas sobre essa relação. Na conduta, a perda de peso e a atividade de baixo impacto receberam destaque.'])+
 box('Complemento: fora da aula','A osteoartrite é hoje compreendida como uma doença de toda a articulação, incluindo cartilagem, osso subcondral e sinóvia. A obesidade é um fator de risco estabelecido, especialmente para a artrose do joelho. Isso não muda o foco didático da aula na perda de cartilagem.','purple')+
 h('Por que dói se a cartilagem não tem nervos?')+
 p('A cartilagem normal é <b>aneural e avascular</b>. A dor decorre das consequências de sua lesão e do comprometimento das estruturas vizinhas. Sua matriz extracelular contém muita água, fibras colágenas e proteoglicanos, incluindo sulfato de condroitina. Elasticidade e compressibilidade permitem distribuir a carga; o ambiente articular também participa da nutrição e das trocas metabólicas.')+
 p('Na articulação, cartilagem, osso subcondral, líquido e membrana sinoviais interagem. Água, ácido hialurônico, oxigênio, nutrientes e enzimas fazem parte do ambiente articular descrito. A agressão pode ser traumática, inflamatória, imune ou idiopática. Os condrócitos tentam reparar a matriz, mas a síntese e a degradação entram em desequilíbrio, com proliferação desorganizada, morte celular e perpetuação da lesão.')+
 p('A progressão envolve inflamação, exposição e remodelamento do osso subcondral, esclerose, cistos e formação de osteófitos. O osteófito é o crescimento ósseo conhecido como “bico de papagaio”; integra uma tentativa de adaptação e redistribuição de carga, sem restaurar a cartilagem normal.')+
 fig('cartilagem.svg','Sequência da deterioração da cartilagem: amolecimento, fibrilação, destacamento e erosão.')+
 box('Aprofundamento para residência','As metaloproteinases são enzimas que degradam proteínas colágenas e não colágenas da matriz. A interleucina-1 foi destacada como citocina inflamatória, e fatores de crescimento, como o fator de crescimento transformador beta e o fator de crescimento semelhante à insulina 1, participam da tentativa de reparo. Esse detalhamento molecular foi explicitamente dispensado para a prova da disciplina.')
))

sections.append(sec(2,'Clínica, exame e alinhamento',
 'A queixa típica aparece ao usar a articulação: andar ou apoiar o peso provoca dor. Além de ouvir o paciente, observe como ele entra, anda e movimenta o membro.',
 h('Dor mecânica e perda de movimento')+
 p('Nos membros inferiores, a dor costuma depender da carga: <b>“pisa e dói”</b>. O uso durante o dia pode deixar o paciente mais dolorido no fim do dia ou à noite. A rigidez matinal tem menor destaque do que nas artropatias inflamatórias, nas quais a dor em repouso também merece atenção. A intensidade da dor e a limitação funcional precisam ser avaliadas individualmente.')+
 h('Varo e valgo',True)+
 p('O nome da deformidade depende do segmento e de seu alinhamento. No joelho, o varo corresponde às pernas em “alicate”; no valgo, os joelhos se aproximam. No quadril, a comparação é feita com o ângulo entre o colo e a diáfise do fêmur.')+
 compare(['Varo','Valgo'],[
 ('Joelho','Joelhos mais afastados, aspecto de pernas arqueadas.','Joelhos voltados para dentro, aspecto em “X”.'),
 ('Quadril','Ângulo do colo com a diáfise menor que o padrão de referência.','Ângulo maior; o colo fica mais vertical em relação à diáfise.')])+
 '<div class="ref"><div class="txt"><div class="kick">Referência apresentada para o quadril</div><p>Ângulo do colo femoral com a diáfise.</p></div><div class="val">125 a 130°</div></div>'+
 box('Pegadinha do professor','Não decorar apenas a aparência do joelho e aplicar a mesma imagem ao quadril. Compare o eixo e o ângulo com o padrão normal daquela articulação.','red')+
 box('Complemento: fora da aula','Na nomenclatura geral, o desvio em varo ou valgo pode ser descrito pela orientação do segmento distal em relação ao proximal. Evite transformar a ideia de “afastar da linha média” em uma regra única para todo osso ou articulação.','purple')+
 h('Quadril: a rotação interna se perde primeiro',True)+
 flow(['<b>Posicione o paciente deitado de barriga para cima.</b> Flexione o quadril e o joelho para avaliar as rotações.',
 '<b>Desloque a perna para fora.</b> Esse movimento produz rotação interna do quadril; é a primeira a ficar comprometida.',
 '<b>Desloque a perna para dentro.</b> Isso produz rotação externa, apresentada como o segundo movimento perdido. Observe limitação e dor.'])+
 h('Testes e observação da marcha')+
 rows([
 ('Thomas','Pesquisa contratura em flexão. Ao flexionar o quadril do lado oposto, o membro avaliado não permanece estendido sobre a maca e tende a se elevar.'),
 ('Trendelenburg','Indica insuficiência dos abdutores, especialmente do glúteo médio. Ao apoiar o peso no lado insuficiente, a pelve cai do lado contrário.'),
 ('Na chegada','Observe claudicação, inclinação e queda pélvica enquanto o paciente entra no consultório. A inspeção começa antes das manobras.')])+
 quote('Quando estiverem lá no posto de saúde, no consultório de vocês, levanta da cadeira, vai lá e chama você o paciente. Isso aí já entrega muita coisa sem nem perguntar.','o exame começa na chegada')
))

sections.append(sec(3,'Quatro sinais radiográficos',
 'A radiografia mostra indiretamente a perda de cartilagem e a reação do osso. Fazer a imagem com o paciente apoiando o peso pode revelar um desgaste que parece menor quando ele está deitado.',
 h('Comece pela radiografia',True)+
 p('Na investigação discutida em aula, a radiografia é o exame inicial e complementa a avaliação clínica. Para joelho e bacia, prefira, quando possível, <b>radiografias com carga, em pé</b>. O apoio aproxima as superfícies e evidencia melhor o estreitamento do espaço articular. Uma imagem sem carga pode subestimar a alteração.')+
 box('Duas incidências', 'Na avaliação do quadril, pedir incidências de frente e de perfil. A insistência em duas incidências foi um dos recados práticos da aula.')+
 h('Os quatro achados que serão cobrados',True)+
 rows([
 ('Estreitamento','Redução do espaço articular, também chamada pinçamento. Representa a perda de espessura da cartilagem; foi destacado como sinal precoce e relevante.'),
 ('Esclerose','Aumento da densidade do osso subcondral. Com a cartilagem comprometida, o osso recebe e suporta mais carga.'),
 ('Cistos','Cavidades subcondrais. A explicação da aula relaciona a lesão da cartilagem à entrada de líquido sinovial no osso e à tentativa de encapsulá-lo.'),
 ('Osteófitos','Projeções ósseas marginais, os “bicos de papagaio”. Aumentam a área de contato como tentativa de distribuir a carga.')])+
 p('A esclerose pode ser entendida pela <b>Lei de Wolff</b>: o osso adapta sua estrutura às cargas a que é submetido. Se a cartilagem amortece menos, o osso abaixo dela precisa lidar com uma transmissão de carga maior.')+
 box('Pegadinha do professor','Os sinais estão no osso e no espaço articular, mas o processo não deve ser confundido com uma doença primária da densidade do osso.','red')+
 h('Quando a ressonância ou a tomografia ajudam')+
 compare(['Ressonância magnética','Tomografia computadorizada'],[
 ('Objetivo','Avaliar situações em que a radiografia não responde à dúvida: lesões iniciais selecionadas, osteonecrose, tumores e partes moles.','Avaliar melhor a estrutura e o estoque ósseos, especialmente no planejamento cirúrgico.'),
 ('Exemplo','No ombro, examinar o manguito rotador para orientar o tipo de prótese.','Planejar uma osteotomia ou artroplastia, sobretudo quando há perda óssea.')])+
 p('Uma artrose avançada e evidente na radiografia <b>não exige automaticamente ressonância</b>. O exame adicional deve responder a uma pergunta clínica ou cirúrgica. A incidência de Rosenberg, com o joelho parcialmente flexionado, foi apenas citada como curiosidade, sem prioridade de estudo para esta prova.')+
 box('Complemento: fora da aula','A indicação de radiografia depende do contexto clínico; a recomendação enfática da aula se refere ao raciocínio ortopédico apresentado. Não significa solicitar imagem indiscriminadamente para qualquer dor musculoesquelética.','purple')
))

sections.append(sec(4,'Tratamento: dor e função',
 'O objetivo é aliviar a dor e permitir que a pessoa use melhor a articulação. Comece pelas medidas conservadoras e ajuste o plano conforme a resposta, as expectativas e a limitação no dia a dia.',
 h('Trate o paciente, não apenas a radiografia',True)+
 p('A gravidade da imagem <b>não é diretamente proporcional à intensidade dos sintomas</b>. Uma artrose radiograficamente importante pode ser tolerável com analgesia simples; uma alteração menor pode acompanhar dor intensa. A indicação cirúrgica depende da repercussão clínica, e não de uma imagem isolada.')+
 quote('Você não vai tratar o raio-X, você vai tratar o paciente.','indicação de tratamento')+
 h('A progressão do cuidado',True)+
 flow(['<b>Educação, atividade e controle da dor.</b> Explique a evolução, combine metas realistas, incentive perda de peso quando apropriada e exercício de baixo impacto. Associe analgesia conforme a avaliação.',
 '<b>Reavalie a resposta.</b> Se a dor está controlada e a função é aceitável, mantenha o plano. A boa resposta não obriga a avançar para procedimentos.',
 '<b>Considere medidas locais e opções preservadoras.</b> Fisioterapia, outras modalidades e infiltrações podem ser utilizadas em situações selecionadas. Avalie se alguma correção da deformidade ou procedimento específico faz sentido.',
 '<b>Discuta substituição articular quando indicada.</b> Dor incapacitante persistente, perda funcional e falha do cuidado conservador levam à avaliação para artroplastia. A decisão é compartilhada com o paciente.'])+
 h('Medidas conservadoras')+
 rows([
 ('Movimento','Natação, bicicleta, musculação orientada e pilates foram exemplos de atividades de menor impacto. Fisioterapia, hidroterapia e acupuntura também foram mencionadas.'),
 ('Adesão','Mudar hábitos de uma vida inteira é difícil. A consulta deve ajudar o paciente a sair da inatividade e estabelecer objetivos possíveis.'),
 ('Medicação','Analgésicos, como dipirona e paracetamol, e anti-inflamatórios foram citados. O uso prolongado de anti-inflamatórios e corticoides exige considerar efeitos adversos.')])+
 h('Infiltração e suplementação: limites da proposta')+
 p('As possibilidades mencionadas incluem corticoide, ácido hialurônico e medicação analgésica em aplicação local. Dexametasona e lidocaína apareceram como exemplos na discussão. A infiltração é uma <b>alternativa selecionada</b>, não uma aplicação mensal automática nem uma etapa obrigatória para todos.')+
 p('Glicosamina, condroitina e colágeno foram citados como suplementos ou condroprotetores. O benefício da suplementação oral foi descrito como controverso, com custo mensal exemplificado em <b>R$ 150 a R$ 200</b>. Também foram mencionados plasma rico em plaquetas e aspirado de medula óssea. Não foi estabelecido um esquema de dose, frequência ou duração para essas opções.')+
 box('Complemento: fora da aula','Essas opções não têm eficácia equivalente nem garantia de regenerar a cartilagem. Suplementos podem ter contraindicações e interações; não se deve assumir que “na pior das hipóteses não funcionam”. Infiltrações exigem indicação, técnica e avaliação de riscos. A lista de exemplos não constitui uma prescrição.','purple')+
 quote('Não dá para prometer nem condenar, tem que cuidar com o que você fala, com o que você promete.','expectativas e relação com o paciente')+
 h('Três palavras que não são sinônimas',True)+
 rows([
 ('Artroplastia','Reconstrução ou substituição articular; na aula, principalmente a colocação de uma prótese.'),
 ('Artrodese','Fusão cirúrgica da articulação: elimina o movimento daquele segmento.'),
 ('Anquilose','Fusão ou rigidez articular estabelecida sem a intenção cirúrgica de uma artrodese. Na explicação da aula, corresponde à união não cirúrgica das superfícies.')])+
 box('Complemento: fora da aula','A anquilose não é um destino inevitável de toda artrose. O termo também pode descrever rigidez por união fibrosa ou óssea; a distinção central aqui é entre a fusão operatória e a não operatória.','purple')
))

sections.append(sec(5,'Quadril: coxartrose',
 'No quadril, o desgaste pode causar dor, dificuldade para girar a perna e alteração da marcha. É preciso distinguir o que vem da própria articulação de problemas da coluna ou das estruturas ao redor.',
 h('Apresentação e causas secundárias')+
 p('A coxartrose associa deterioração da cartilagem, neoformação óssea, dor, restrição de movimento, incapacidade funcional e claudicação. A perda de rotação interna é uma pista de exame físico; a <b>repercussão dos sintomas</b> orienta a necessidade de tratamento.')+
 p('O panorama epidemiológico apresentado incluiu acometimento de 5 a 10% da população mundial, maior frequência em mulheres acima dos 55 anos e menor frequência em asiáticos. Foi também mencionada a necessidade de cirurgia em cerca de metade dos casos do panorama discutido. Essas estimativas devem ser entendidas dentro da população considerada, sem prever a evolução de um paciente individual.')+
 rows([
 ('Displasia','Alteração do desenvolvimento do quadril, destacada como importante causa de artrose secundária; sua participação foi descrita como próxima ou superior à metade.'),
 ('Epifisiólise','Sequela de alteração da região de crescimento do fêmur proximal. Foi citada a proporção de 39% no conjunto de causas secundárias apresentado.'),
 ('Perthes','A doença de Legg-Calvé-Perthes foi citada com 2,2% nesse mesmo panorama. Coxa profunda e coxa vara também apareceram entre as condições associadas.')])+
 box('Complemento: fora da aula','Os percentuais de displasia, epifisiólise e doença de Perthes não devem ser somados ou aplicados a toda a população: o denominador e a população de referência precisam ser conhecidos. São números do panorama de causas secundárias apresentado.','purple')+
 h('O que pode parecer artrose do quadril')+
 ul(['<b>Bursite trocantérica e tendinopatia do glúteo médio.</b> Podem produzir dor e coexistir com a doença articular.',
 '<b>Doenças da coluna.</b> Uma síndrome compressiva lombar pode simular problema do quadril; a confusão também ocorre no sentido inverso.',
 '<b>Tumores e osteonecrose.</b> Manifestações atípicas exigem investigação. A osteonecrose envolve comprometimento do suprimento sanguíneo da cabeça femoral e pode levar a artrose secundária.'])+
 p('A radiografia de frente e perfil é a base. A ressonância magnética pode ajudar na suspeita de osteonecrose e em situações selecionadas de tumor; a tomografia auxilia a investigação óssea e o planejamento. A história e o exame devem explicar os achados.')+
 h('Da preservação à substituição articular')+
 rows([
 ('Artroscopia','Em casos selecionados, sobretudo alterações leves e lesões de cartilagem ou do lábio articular, permite tratar estruturas por vídeo.'),
 ('Osteotomia','Corrige deformidades angulares. É uma possibilidade em pacientes jovens, com bom estoque ósseo, para tentar adiar a artroplastia.'),
 ('Artrodese','Opção de fusão para situações muito selecionadas, cada vez menos utilizada no quadril.'),
 ('Artroplastia','Substituição articular diante de dor incapacitante e perda funcional, quando o cuidado conservador já não oferece resultado aceitável.')])+
 box('Pegadinha do professor','Idade e imagem, sozinhas, não decidem a cirurgia. O ponto destacado foi a dor incapacitante e o limite funcional que o paciente já não consegue tolerar.','red')+
 p('Os tipos de prótese e os acessos são repertório para residência e formação futura. A prioridade da disciplina permanece nos quatro sinais radiográficos e nos conceitos clínicos centrais.')+
 h('Próteses: noções para residência')+
 rows([
 ('Total','Modelo tradicional de substituição do quadril. Permite tratar os dois lados da articulação.'),
 ('Parcial','Foi associada principalmente a fraturas em idosos muito frágeis e com expectativa de sobrevida limitada. Não deve ser generalizada como tratamento habitual da coxartrose.'),
 ('Recobrimento','Preserva maior estoque ósseo ao recobrir a superfície. A possibilidade de revisão futura é considerada, embora o uso tenha diminuído com a evolução das próteses convencionais.')])+
 h('Acessos do quadril: guardar para residência')+
 rows([
 ('Smith-Petersen','Anterior. Plano superficial entre sartório e tensor da fáscia lata; plano profundo entre reto femoral e glúteo médio. O mnemônico da aula associa o “S” e o “T” ao plano superficial.'),
 ('Hardinge','Lateral, através do glúteo médio.'),
 ('Kocher-Langenbeck','Posterior, nome apresentado para o acesso posterior na aula. Foram citados posicionamento lateral e apoios para estabilizar a pelve.')])
))

sections.append(sec(6,'Joelho e polegar',
 'No joelho, o alinhamento, os meniscos e os ligamentos ajudam a explicar os sintomas. No polegar, a localização na base do dedo é a pista para reconhecer a rizartrose.',
 h('Gonartrose: além da cartilagem')+
 p('A artrose do joelho é multifatorial. Predisposição genética e deformidades prévias se somam à participação dos <b>meniscos</b>, que ajudam a distribuir e amortecer a carga. A degeneração ligamentar pode acrescentar frouxidão e instabilidade.')+
 p('São frequentes dor mecânica à marcha, limitação funcional, claudicação e deformidade em varo ou valgo. A instabilidade pode produzir episódios de “flambagem”: o joelho parece falhar ou desviar bruscamente durante o apoio.')+
 h('Compartimento medial e varo',True)+
 p('O compartimento medial recebe aproximadamente <b>60% da carga</b>, segundo o número apresentado. É o local de maior desgaste habitual, e a deformidade mais comum da gonartrose é o varo. A alteração do eixo também modifica a distribuição da carga e participa da progressão.')+
 h('O que procurar na radiografia do joelho')+
 p('Reveja os quatro sinais clássicos: estreitamento, esclerose subcondral, cistos e osteófitos. Observe também <b>alteração do eixo e corpos livres intra-articulares</b>. Fragmentos de cartilagem podem se desprender, calcificar e causar irritação ou sensação de algo solto dentro da articulação.')+
 h('Quando considerar artroplastia')+
 ul(['<b>Dor intensa persistente.</b> Não melhora de modo aceitável com o tratamento conservador.',
 '<b>Perda da capacidade funcional.</b> Pode justificar avaliação inclusive em pacientes mais jovens com comprometimento importante.',
 '<b>Deformidades progressivas.</b> Principalmente quando uma osteotomia já não é uma opção adequada.'])+
 p('A base conservadora é a mesma do quadril: educação, expectativas realistas, fortalecimento, fisioterapia e atividade de menor impacto, com medicação e medidas locais conforme o caso. Se o plano controla a dor e preserva função, ele pode ser mantido.')+
 h('Preservar osso pensando na revisão futura')+
 p('Na doença restrita a um compartimento, com o outro preservado, pode ser considerada a <b>prótese unicompartimental</b>. Essa alternativa preserva estruturas e estoque ósseo. A cirurgia atual já leva em conta uma possível revisão em 15 a 20 anos, além de disponibilidade de material, enxerto e custo. Esse intervalo é uma perspectiva de planejamento, não um prazo obrigatório de falha da prótese.')+
 p('Os acessos pela linha média e subvasto foram citados para guardar, sem prioridade de estudo agora. O subvasto passa sob a musculatura do vasto e pode ser mais trabalhoso ou limitar algumas etapas da cirurgia. Os tipos de prótese foram lembrados como assunto de residência.')+
 h('Rizartrose: onde fica?',True)+
 p('É a artrose da <b>primeira articulação carpometacarpiana, na base do polegar</b>, envolvendo o trapézio. Foi apresentada como a forma mais comum de artrose da mão, com estimativa de 10% na população com idade mais avançada e maior ocorrência em asiáticos que em caucasianos.')+
 compare(['Procedimento','Efeito e limite'],[
 ('Artrodese','Fusão cirúrgica.','Pode aliviar a dor, com perda de movimento e repercussão na pinça.'),
 ('Artroplastia','Substituição por componente protético.','Na comparação apresentada, tem resultados menos favoráveis que no quadril e no joelho.'),
 ('Trapeziectomia','Ressecção do trapézio.','Retira o osso envolvido na articulação doente como alternativa de tratamento.')])+
 box('Complemento: fora da aula','A escolha cirúrgica para a rizartrose depende de idade, demanda, estabilidade e articulações envolvidas. A artrodese foi destacada na aula; isso não a torna a operação mais frequente ou preferida em todos os contextos. A trapeziectomia, com suas variações, é uma alternativa amplamente utilizada.','purple')+
 p('Na rizartrose, o encaminhamento ao cirurgião pode ser considerado quando o controle clínico da dor falha. O efeito sobre a pinça precisa entrar na escolha do procedimento. A discussão deve considerar que a rigidez cirúrgica pode limitar movimentos úteis da mão.')
))

sections.append(sec(7,'Ombro e manguito rotador',
 'Os tendões do manguito ajudam a manter a cabeça do úmero funcionando no lugar certo. Se eles deixam de cumprir essa função, a mecânica muda, e a escolha da prótese também pode mudar.',
 h('Artrose glenoumeral e lesão crônica do manguito')+
 p('O processo degenerativo pode ser primário ou secundário a trauma, inflamação e alteração do manguito rotador. Na <b>artropatia do manguito</b>, a lesão crônica modifica a sustentação e a biomecânica do ombro, favorecendo degeneração e instabilidade. A aula relacionou diferenças de frequência entre países aos esportes de arremesso e ao uso dos membros superiores.')+
 h('Imagem e planejamento')+
 rows([
 ('Radiografia','Exame inicial. O osteófito inferior ou inferomedial da cabeça do úmero, em “barba de bode”, é um achado característico apresentado na aula.'),
 ('Ressonância','Avalia o manguito rotador e ganha especial importância para definir a estratégia de artroplastia.'),
 ('Tomografia','Ajuda a avaliar perda e estoque ósseos. O estoque disponível pode ser limitado, especialmente para planejar a reconstrução.')])+
 h('Manguito funcional ou insuficiente?',True)+
 fig('ombro.svg','Relação entre função do manguito rotador e escolha entre artroplastia anatômica e reversa.')+
 p('Na prótese anatômica, o componente umeral mantém a forma de cabeça e o componente glenoidal mantém a forma de cavidade. Na reversa, a esfera fica na glenoide e a cavidade no úmero; a mudança permite que o <b>deltoide tenha papel central no movimento</b> quando o manguito não funciona adequadamente.')+
 box('Pegadinha do professor','A importância da ressonância no ombro não é apenas confirmar desgaste. Ela investiga o manguito, cuja função modifica a decisão terapêutica.','red')+
 h('Outras possibilidades')+
 rows([
 ('Artroscopia','O debridamento, ou “toalete”, pode retirar corpos livres e fragmentos que irritam a articulação. O benefício pode ser parcial ou temporário, adiando uma intervenção maior em casos selecionados.'),
 ('Recobrimento','Recapeia a superfície e busca preservar estoque ósseo.'),
 ('Artrodese','Opção de fusão com indicação mais restrita no ombro.')])+
 p('A artroscopia é uma cirurgia realizada por vídeo. A lista de técnicas é repertório; o ponto enfatizado para avaliação foi a <b>relação entre o manguito e a escolha da prótese</b>.')
))

sections.append(sec(8,'Coluna e sinais neurológicos',
 'Na coluna, a dor pode vir de várias estruturas. O ponto que muda a urgência é saber se existe compressão de nervos, principalmente quando aparecem alterações da sensibilidade do períneo ou do controle urinário e intestinal.',
 h('Estruturas e segmentos mais envolvidos')+
 p('Discos, facetas articulares, ossos e ligamentos participam da degeneração. Dor facetária, doença discal, hérnia de disco, trauma e fratura também entram no raciocínio. O aprofundamento das patologias da coluna ficou previsto para outra aula.')+
 rows([
 ('Lombar','Entre a quarta e a quinta vértebras lombares e entre a quinta lombar e a primeira sacral.'),
 ('Cervical','Entre a quinta e a sexta vértebras cervicais e entre a sexta e a sétima cervicais.')])+
 p('Esses níveis têm grande mobilidade, o que ajuda a explicar sua maior exposição a alterações degenerativas e hérnias. Na avaliação, <b>o exame neurológico ganha prioridade</b>: a radiografia isolada não explica toda queixa nem exclui compressão radicular.')+
 h('Dor irradiada e sintomas radiculares')+
 p('Dor cervical com formigamento no braço ou dor lombar com queimação irradiada para a perna sugerem comprometimento de raízes nervosas. A interpretação depende do exame: localização, sensibilidade, força e evolução do quadro orientam a investigação.')+
 fig('coluna.svg','Três situações que orientam a prioridade na dor de coluna: suspeita de cauda equina, déficit progressivo e outras indicações cirúrgicas.')+
 h('Síndrome da cauda equina: urgência',True)+
 box('Interrompa a rotina e providencie atendimento urgente','Anestesia em sela, na região do períneo, associada a perda ou alteração do controle esfincteriano exige suspeitar de compressão das raízes da cauda equina. Acione o atendimento de urgência e o encaminhamento especializado. Não conduza como uma lombalgia comum.','red')+
 p('Anestesia em sela e alterações urinárias ou intestinais exigem ação imediata. Acione o <b>Serviço de Atendimento Móvel de Urgência</b> para obter o suporte adequado.')+
 h('Pergunte, examine e registre',True)+
 p('Em toda avaliação de lombalgia, investigue sintomas perineais e esfincterianos. O prontuário deve documentar o que o paciente informou e o que foi efetivamente examinado. A evolução posterior pode mudar o quadro e precisa ser considerada na orientação.')+
 box('Complemento: fora da aula','Não copie automaticamente “nega anestesia em sela” ou “nega descontrole esfincteriano”. Registre a negativa apenas após investigar o sintoma. A suspeita de cauda equina não depende de esperar que todos os sinais apareçam juntos.','purple')+
 h('Quando a cirurgia deixa de depender apenas da dor',True)+
 p('<b>Déficit neurológico progressivo</b>, dor refratária, instabilidade e estenose podem indicar cirurgia. Conforme o caso, descomprime-se, retiram-se estruturas compressivas e estabiliza-se por artrodese. A indicação não depende apenas da dor.')
))

ess=[
 ('01 · Conceito','Artrose: foco na cartilagem; densitometria não é o exame de investigação.'),
 ('02 · Eixos','Joelho varo em alicate; valgo em “X”. Quadril: referência de 125 a 130°, menor no varo e maior no valgo.'),
 ('02 · Exame','No quadril, rotação interna se perde primeiro; a externa vem depois. Trendelenburg: queda pélvica contralateral ao apoio insuficiente.'),
 ('03 · Imagem','Radiografia inicial; com carga quando possível; frente e perfil no quadril.'),
 ('03 · Quatro sinais','Estreitamento do espaço articular, esclerose subcondral, cistos subcondrais e osteófitos.'),
 ('04 · Conduta','Tratamento conservador primeiro. A imagem não mede sozinha a dor; cirurgia depende de limitação e resposta ao cuidado.'),
 ('04 · Termos','Artrodese: fusão cirúrgica. Anquilose: fusão ou rigidez não produzida como artrodese.'),
 ('05 e 06 · Carga','Quadril: decisão guiada pela repercussão clínica. Joelho: cerca de 60% da carga medial e varo mais frequente.'),
 ('06 · Polegar','Rizartrose fica na primeira carpometacarpiana, na base do polegar.'),
 ('07 · Ombro','Manguito funcional favorece prótese anatômica; insuficiente pode exigir reversa, com participação central do deltoide.'),
 ('08 · Urgência','Anestesia em sela e alteração esfincteriana: suspeitar de cauda equina e agir com urgência. Déficit progressivo também pesa na cirurgia.')]
essential='<section id="s09" class="vesp"><div class="sec-head"><span class="num">09</span><h2>O essencial da aula</h2></div><p class="revisao-intro">Página de véspera · siga a trilha e recupere as decisões principais.</p>'
for a,b in ess:
    essential+='<div class="item"><span class="prova">PROVA</span><p><b>'+a+'.</b> '+b+'</p></div>'
essential+=p('<b>Outros números:</b> rara antes dos 35 anos; forma primária mais comum nas mulheres após 55 anos; quadril com estimativa de 5 a 10%; rizartrose com 10% na população mais velha. Não confundir estimativas de grupos com indicação individual de cirurgia.')+'</section>'
sections.append(essential)

terms=[('Artroscopia','Cirurgia por vídeo dentro de uma articulação.'),('Claudicação','Alteração da marcha, geralmente com mancar.'),('Condrócito','Célula responsável por produzir e manter a matriz da cartilagem.'),('Contratura','Limitação persistente do movimento por encurtamento ou rigidez dos tecidos.'),('Coxa profunda','Configuração em que o encaixe do quadril é mais profundo.'),('Debridamento','Retirada de fragmentos ou tecidos que provocam irritação ou não estão viáveis.'),('Displasia','Desenvolvimento anormal de uma estrutura; no quadril, altera a forma e o encaixe da articulação.'),('Estoque ósseo','Quantidade e qualidade de osso disponível para sustentar uma reconstrução.'),('Estenose','Estreitamento de um espaço; na coluna, pode comprimir estruturas nervosas.'),('Lábio articular','Anel de tecido que contorna o encaixe da articulação, também chamado labrum.'),('Osso subcondral','Osso que fica logo abaixo da cartilagem articular.'),('Osteonecrose','Morte de tecido ósseo por comprometimento de seu suprimento sanguíneo.'),('Osteotomia','Corte cirúrgico do osso para corrigir alinhamento ou deformidade.'),('Proteoglicanos','Moléculas da matriz que ajudam a reter água e resistir à compressão.'),('Sinóvia','Membrana que reveste internamente a articulação e participa da produção do líquido sinovial.'),('Trapeziectomia','Retirada cirúrgica do osso trapézio, na base do polegar.')]
sections.append('<section id="s10"><div class="sec-head"><span class="num">10</span><h2>Palavras da aula</h2></div>'+rows(terms,True)+box('Recado da disciplina','Ao final da aula, foi anunciada uma revisão da prova em grupos aleatórios e uma possibilidade de recuperar pontuação. Não foi definida aqui uma regra completa de valor ou composição dos grupos.')+'{{NOTAS}}</section>')

style='''
.sec-head { align-items:center; break-after:avoid; }
.sec-head h2 { flex:1 1 auto; min-width:0; font-size:18pt; line-height:1.5; padding:4pt 8pt; }
.sec-head .num { flex:0 0 38pt; width:38pt; background:linear-gradient(140deg,#0B5BD3,#5659A7); color:white; display:flex; align-items:center; justify-content:center; border-radius:9pt; font-size:18pt; line-height:1.5; padding:4pt; }
.simples { background:#FFF; border:1px solid #C3D8F8; border-left:4pt solid #0B5BD3; border-radius:12pt; padding:9pt 14pt 10pt; margin:9pt 0 10pt; break-inside:avoid; }
.simples p { font-size:10.2pt; line-height:1.5; color:#1F2933; margin:0; }
.aqui { display:flex; margin-top:7pt; margin-bottom:8pt; break-after:avoid; }
.aqui span { flex:1; border-top:3pt solid #DCDCE2; padding-top:2.5pt; margin-right:2.5pt; font-family:"Inter Medium"; font-size:6pt; line-height:1.5; color:#6C6C70; }
.aqui span.feito { border-top-color:#A9C4EE; }
.aqui span.on { border-top-color:#0B5BD3; color:#0B5BD3; font-family:"Inter SemiBold"; }
.cover .toc a { padding:3pt 0; }
.cover .author span:not(.av) { font-size:8.5pt; }
.vesp { break-before:page; }
.vesp .item { display:flex; align-items:baseline; background:#FFF; border:1px solid #E3E3E8; border-radius:10pt; padding:6pt 10pt; margin:0 0 5pt; break-inside:avoid; }
.vesp .item .prova { flex:none; margin:0 8pt 0 0; font-size:6pt; }
.vesp .item p { margin:0; font-size:8.6pt; line-height:1.5; }
.revisao-intro { margin-bottom:8pt; }
.figure img { max-width:100%; }
'''
toc_titles=['O que é a artrose','Clínica, exame e alinhamento','Imagem: os quatro sinais clássicos','Tratamento: dor e função orientam','Quadril: coxartrose','Joelho e polegar','Ombro: o manguito muda a prótese','Coluna e comprometimento neurológico','O essencial da aula','Palavras da aula em linguagem simples']
cover='''<div class="cover"><div class="kicker">Ortopedia · Aula 2 · Artrose</div><h1>Artrose</h1><p class="sub">Da perda de cartilagem à decisão de tratar: quadril, joelho, polegar, ombro e coluna.</p><div class="author"><span class="av">C</span><div><b>Dr. Gustavo Alves Colombo</b><span>Ortopedista e traumatologista · Cirurgia do quadril<br>8 de outubro de 2026</span></div></div><div class="keynums"><div class="kick">Três números para levar</div><div class="kn-grid"><div class="kn"><div class="n">4</div><div class="l">sinais radiográficos clássicos</div></div><div class="kn"><div class="n">125 a 130°</div><div class="l">referência angular do quadril</div></div><div class="kn"><div class="n">60%</div><div class="l">da carga no compartimento medial do joelho</div></div></div></div><div class="toc"><div class="kick">Nesta apostila</div>'''
for i,title in enumerate(toc_titles,1): cover+=f'<a href="#s{i:02d}"><span class="tn">{i:02d}</span><span class="tt">{title}</span><span class="pg">{{{{s{i:02d}}}}}</span></a>'
cover+='</div></div>'
legend='<div class="legend"><div class="kick">Como ler esta apostila</div><div class="lg-grid">'
for sw,text in [('blue','Azul: conteúdo e raciocínio da aula.'),('green','Verde: números e valores de referência.'),('red','Vermelho: alerta ou pegadinha.'),('orange','Laranja: fala do professor.'),('purple','Roxo: complemento fora da aula.')]:
    legend+='<div class="lg"><span class="sw '+sw+'"></span><div>'+text+'</div></div>'
legend+='<div class="lg"><span class="prova">PROVA</span><div>Ponto enfatizado para estudar.</div></div><div class="lg"><span class="sw blue"></span><div>“Em palavras simples”: ideia central do capítulo.</div></div><div class="lg"><span class="sw blue"></span><div>A faixa superior mostra a etapa da trilha.</div></div></div></div>'
bio='<div class="prof"><div class="kick">Sobre o professor · Dr. Gustavo Colombo</div>'+rows([
('Especialidade','Ortopedia e traumatologia, com subespecialização em cirurgia do quadril.'),
('Formação','Medicina pelo Centro Universitário Fundação Assis Gurgacz; residência no Hospital São Lucas de Cascavel; subespecialização no Hospital Universitário Cajuru, Curitiba.'),
('Atuação','Grupo de Cirurgia do Quadril do Centro Especializado em Ortopedia e Traumatologia, em Cascavel, Paraná.'),
('Sociedades','Sociedade Brasileira de Ortopedia e Traumatologia; membro em formação da sociedade internacional de preservação do quadril, The Hip Preservation Society.')])+'</div>'
intro='<div class="box"><div class="kick">Trilha da aula</div>'+p('Da cartilagem à conduta: a decisão depende da articulação, da dor e da função.')+fig('trilha.svg','Trilha em oito etapas, dos conceitos gerais à coluna.')+'</div>'
html='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Ortopedia · Aula 2 · Artrose</title><meta name="rodape" content="Mauricio Faria · Ortopedia · Aula 2 — Artrose"><link rel="stylesheet" href="apostila.css"><style>'+style+'</style></head><body>'+cover+legend+bio+intro+''.join(sections)+'</body></html>'
(ROOT/'apostila.html').write_text(html,encoding='utf-8')
print('HTML e quatro figuras gerados; palavras:',len(re.findall(r'\w+',re.sub('<[^>]*>',' ',html))))
