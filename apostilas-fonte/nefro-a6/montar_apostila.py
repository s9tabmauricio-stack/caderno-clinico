"""Texto e composição da apostila. O CSS e os renderizadores oficiais não são alterados."""
from pathlib import Path
from html import escape

ROOT=Path(__file__).resolve().parent

def p(s):return '<p>'+s+'</p>'
def h(s):return '<h3>'+s+'</h3>'
def box(title,body,color=''):
    return f'<div class="box {color}"><div class="kick"><span class="dot"></span>{title}</div>{body}</div>'
def note(body,ref):return box('Complemento: fora da aula',p(body)+f'<p class="fonte">Referência: <a href="#refs">{ref}</a>.</p>','purple')
def quote(s,context):return f'<div class="quote"><p>“{s}”</p><div class="who">Dra. Andressa, {context}</div></div>'
def ul(items):return '<ul>'+''.join('<li>'+s+'</li>' for s in items)+'</ul>'
def rows(items):
    return '<div class="rows">'+''.join(f'<div class="row"><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in items)+'</div>'
def table(head,items,widths=None):
    cols=''
    if widths:cols='<colgroup>'+''.join(f'<col style="width:{w}%">' for w in widths)+'</colgroup>'
    return '<table class="estudo">'+cols+'<thead><tr>'+''.join('<th>'+x+'</th>' for x in head)+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+v+'</td>' for v in row)+'</tr>' for row in items)+'</tbody></table>'
def figure(name,alt,caption,look=None):
    return f'<div class="figure"><img src="fig/{name}.svg" alt="{escape(alt)}"'+(' style="width:90%;display:block;margin:0 auto"' if name=='decisao' else '')+'>'+(f'<div class="olhar"><div class="kick">O que olhar</div>{ul(look)}</div>' if look else '')+f'<p class="leg">{caption}</p></div>'

chapters=[('A paciente','Da bexiga ao rim'),('Os exames','Ler os exames de urina'),('A cistite','Reconhecer a cistite'),('O tratamento','Tratar a cistite'),('O rim','Pielonefrite e gravidade'),('A conduta','Tratar e reavaliar'),('O risco','Infecção complicada'),('A gestação','Cuidar na gestação')]
def chapter(n,simple,body):
    bar=''.join(f'<span class="{"on" if i==n else "feito" if i<n else ""}">{i:02d} {name}</span>' for i,(name,_) in enumerate(chapters,1))
    return f'<section id="s{n:02d}"><div class="sec-head"><span class="num">{n:02d}</span><h2>{chapters[n-1][1]}</h2></div><div class="aqui" aria-label="Você está aqui">{bar}</div><div class="simples"><div class="kick">Em palavras simples</div>{p(simple)}</div>{body}</section>'

style='''
/* Componentes do molde aprovado, aplicados apenas a esta apostila. */
.simples {background:#FFF;border:1px solid #C3D8F8;border-left:4pt solid #0B5BD3;border-radius:12pt;padding:9pt 14pt 10pt;margin:9pt 0 10pt;break-inside:avoid}
.simples p {font-size:10.2pt;line-height:1.5;color:#1F2933;margin:0}
.aqui {display:flex;margin-top:7pt;margin-bottom:9pt;break-after:avoid}
.aqui span {flex:1;border-top:3pt solid #DCDCE2;padding-top:2.5pt;margin-right:2.5pt;font-family:"Inter Medium";font-size:6pt;line-height:1.25;color:#6C6C70}
.aqui span:last-child {margin-right:0}
.aqui span.feito {border-top-color:#A9C4EE;color:#6C6C70}
.aqui span.on {border-top-color:#0B5BD3;color:#0B5BD3;font-family:"Inter SemiBold"}
.figure img {max-width:100%;height:auto}
.figure .olhar {margin-top:8pt}.figure .olhar .kick{margin-bottom:3pt}
.figure .olhar ul {margin:0}.figure .olhar li{padding-left:0;font-size:8.7pt;line-height:1.5;margin-bottom:2pt}.figure .olhar li::before{display:none}
.figure .leg{font-size:7.8pt;line-height:1.5;color:#6C6C70;margin:5pt 0 0}
.estudo {width:100%;border-collapse:collapse;margin:8pt 0 12pt;font-size:9pt;line-height:1.5;table-layout:fixed}
.estudo th{background:#E8F0FE;color:#16315C;font-family:"Inter SemiBold";font-weight:600;text-align:left;padding:7pt 9pt;border:1px solid #C3D8F8}
.estudo td{background:#FFF;color:#3A3A3C;vertical-align:top;padding:7pt 9pt;border:1px solid #DCDCE2;overflow-wrap:anywhere}
.estudo tr{break-inside:avoid}.estudo thead{display:table-header-group}
.fonte {font-size:7.8pt!important;line-height:1.5!important;margin-top:4pt!important;color:#6E3AA7!important}
.fonte a,.refs a{color:#6E3AA7;text-decoration:none}
.compact {font-size:8.5pt;line-height:1.5;color:#6C6C70}
.cover .toc a{padding:3.6pt 0}.cover .sub{max-width:440pt}
.sec-head {display:table;table-layout:fixed;width:100%;border-spacing:0;break-after:avoid}
.sec-head .num {display:table-cell;width:38pt;min-width:38pt;vertical-align:middle;font-family:"Inter SemiBold";font-size:18pt;line-height:1.5;color:#0B5BD3;text-align:center}
.sec-head h2 {display:table-cell;width:auto;min-width:0;max-width:none;vertical-align:middle;margin:0;padding:4pt 8pt 4pt 0;font-size:19pt;line-height:1.3;color:#16315C}
.vesp {break-before:page;break-after:page}
.vesp .item {background:#FFF;border:1px solid #E3E3E8;border-radius:10pt;padding:8pt 11pt;margin:0 0 5pt;break-inside:avoid}
.vesp .item p{margin:0;font-size:9.2pt;line-height:1.5}
.vesp .item b{color:#16315C}
.vesp .intro{font-size:8.7pt;line-height:1.5;margin:0 0 9pt}
.refs {font-size:8pt;line-height:1.5}
.prof .rows{margin-bottom:0}.legend .lg-grid{row-gap:7pt}
.simples .kick{font-size:7.5pt;margin-bottom:4pt;color:#0B5BD3}
'''

toc=''.join(f'<a href="#s{i:02d}"><span class="tn">{i:02d}</span><span class="tt">{t}</span><span class="pg">{{{{s{i:02d}}}}}</span></a>' for i,(_,t) in enumerate(chapters,1))
toc+='<a href="#s09"><span class="tn">09</span><span class="tt">Página de véspera</span><span class="pg">{{s09}}</span></a><a href="#s10"><span class="tn">10</span><span class="tt">Glossário e anotações</span><span class="pg">{{s10}}</span></a>'
cover='''<div class="cover"><div class="kicker">Nefrologia · Aula 6 · Infecção urinária</div>
<h1>Da bexiga<br>ao rim</h1><p class="sub">Como reconhecer, investigar e tratar a infecção urinária na mulher adulta e na gestação.</p>
<div class="author"><span class="av">A</span><div><b>Dra. Andressa</b><span>Professora de Nefrologia · 21 de outubro de 2026</span></div></div>
<div class="keynums"><div class="kick">Três números para levar</div><div class="kn-grid">
<div class="kn"><div class="n">11%</div><div class="l">das mulheres com cistite por ano, na estimativa da aula</div></div>
<div class="kn"><div class="n">48 horas</div><div class="l">sem febre no critério de transição apresentado</div></div>
<div class="kn"><div class="n">1 semana</div><div class="l">para a cultura de controle na gestante, no seguimento da aula</div></div>
</div></div><div class="toc"><div class="kick">Nesta apostila</div>'''+toc+'''<p class="note">Foco na mulher adulta: sintomas, exames, escolhas de tratamento e situações que exigem mais cuidado. A legenda de leitura está na página 2.</p></div></div>'''

legend='''<div class="legend"><div class="kick">Como ler esta apostila</div><div class="lg-grid">
<div class="lg"><span class="sw blue"></span><div><b>Azul</b> conteúdo e raciocínio da aula</div></div>
<div class="lg"><span class="sw green"></span><div><b>Verde</b> dose ou valor de referência</div></div>
<div class="lg"><span class="sw red"></span><div><b>Vermelho</b> alerta, erro comum ou armadilha</div></div>
<div class="lg"><span class="sw orange"></span><div><b>Laranja</b> fala ou parêntese da professora</div></div>
<div class="lg"><span class="sw purple"></span><div><b>Roxo</b> complemento: fora da aula</div></div>
<div class="lg"><span class="prova">PROVA</span><div><b>Marca de prova</b> reservada à indicação de cobrança</div></div>
<div class="lg"><span class="sw blue"></span><div><b>Em palavras simples</b> a ideia de cada capítulo</div></div>
<div class="lg"><span class="sw red"></span><div><b>Pegadinha</b> atenção no ponto em que se erra</div></div>
<div class="lg"><span class="sw blue"></span><div><b>Você está aqui</b> etapa atual na trilha da aula</div></div>
</div></div>
<div class="prof"><div class="kick">Sobre a professora · Dra. Andressa</div>'''+rows([('Atuação','Professora de Nefrologia nesta aula.')])+'''</div>
<h3>A trilha da aula</h3>'''+figure('trilha','Oito etapas: paciente, exames, cistite, tratamento, rim, conduta, risco e gestação.','Siga a sequência e use a faixa azul dos capítulos para localizar a etapa atual.')

references='''<div class="refs" id="refs"><h3>Referências dos complementos</h3>
<p>As notas roxas distinguem esclarecimentos clínicos do conteúdo da aula. Consulta das diretrizes: 5 de novembro de 2026.</p>
<p><a href="https://uroweb.org/guidelines/urological-infections/chapter/the-guideline">Associação Europeia de Urologia. Diretrizes de infecções urológicas.</a> Diagnóstico, esquemas e classificações.</p>
<p><a href="https://uroweb.org/guidelines/urolithiasis/chapter/guidelines">Associação Europeia de Urologia. Diretrizes de litíase urinária, seção 3.4.2.</a> Obstrução infectada e descompressão.</p>
<p><a href="https://www.idsociety.org/practice-guideline/complicated-urinary-tract-infections/">Sociedade Americana de Doenças Infecciosas. Diretriz de infecção urinária complicada, 2025.</a> Transição oral e duração.</p>
<p><a href="https://www.acog.org/clinical/clinical-guidance/clinical-consensus/articles/2023/08/urinary-tract-infections-in-pregnant-individuals">Colégio Americano de Obstetras e Ginecologistas. Infecções urinárias na gestação, 2023.</a> Investigação e antibióticos.</p>
<p><a href="https://medlineplus.gov/lab-tests/nitrites-in-urine/">Biblioteca Nacional de Medicina dos Estados Unidos. MedlinePlus: nitritos na urina.</a> Limites da interpretação do nitrito.</p>
</div>'''
body=''
body+=chapter(1,'Uma infecção pode ficar na bexiga ou alcançar os rins. Reconhecer onde ela está ajuda a entender os sintomas, a gravidade e o tipo de cuidado necessário.',
p('O foco desta aula é a <b>mulher adulta</b>, com infecção urinária complicada ou não complicada. Crianças, pessoas idosas e homens têm particularidades abordadas em outras áreas. No homem, merece atenção a associação com comprometimento da próstata.')+
figure('anatomia','Dois rins conectados por ureteres à bexiga; uretra curta na saída. Destaque para mucosa da bexiga e um rim inflamados.','Ilustração didática original; as áreas vermelhas localizam a inflamação. Não representa um exame clínico.',[
'<b>Bexiga:</b> a infecção localizada nessa região recebe o nome de cistite.',
'<b>Rim e pelve renal:</b> a infecção do tecido renal e do sistema coletor caracteriza a pielonefrite.',
'<b>Ureteres:</b> conectam os rins à bexiga; a infecção pode ascender por essa via.'])+
h('Por que a via ascendente importa')+
p('A Escherichia coli vive no intestino e é o agente mais frequente da infecção urinária. A proximidade entre região anal, entrada da vagina e abertura da uretra favorece a colonização ao redor da uretra e a entrada das bactérias na via urinária. A anatomia masculina mantém maior distância entre essas regiões.')+
p('A constipação crônica favorece a proliferação de bactérias na região perineal. A baixa ingestão de água e o hábito de adiar a micção reduzem a eliminação frequente de urina e favorecem a permanência dos microrganismos.')+
rows([('Atividade sexual','O atrito pode produzir microtraumas e favorecer a ascensão de bactérias. Isso ajuda a entender episódios depois da relação sexual.'),('Hipoestrogenismo','A redução do estrogênio, especialmente no período ao redor da menopausa, associa-se a ressecamento vaginal e maior vulnerabilidade local.'),('Esvaziamento','Cistocele, enterocele e bexiga neurogênica podem alterar a anatomia ou dificultar a eliminação da urina.')])+
rows([('Cálculo','A litíase pode favorecer persistência de bactérias e, quando obstrui a drenagem, aumentar o risco de complicação.'),('Hábito miccional','A orientação da aula é não segurar a urina por tempo excessivo e manter micções frequentes.')])+
box('Números apresentados em aula',p('A cistite acomete cerca de <b>11% das mulheres por ano</b>; quase 50% terão ao menos um episódio na vida. A estimativa de capacidade vesical feminina citada foi de 350 a 360 mL, com estímulo a urinar aproximadamente a cada 1h30 a 1h40.'))+
note('Capacidade vesical e intervalo entre micções variam entre pessoas e com a ingestão de líquidos. Os intervalos citados são orientações da aula, não metas rígidas de diagnóstico.','avaliação clínica individual'))

body+=chapter(2,'O exame de urina mostra alterações; a cultura identifica o microrganismo; o antibiograma ajuda a escolher o antibiótico. Cada um responde a uma pergunta diferente.',
figure('exames','Fluxo dos três exames: exame de urina, urocultura e antibiograma.','Três perguntas complementares para o raciocínio clínico.')+
h('O que procurar no exame de urina')+
p('O exame de urina também é chamado de parcial de urina ou urina tipo I. A leitura reúne aspecto físico, substâncias dissolvidas e elementos do sedimento. Um resultado isolado precisa ser interpretado junto dos sintomas e do contexto clínico.')+
table(['Parâmetro','Relação explorada na aula'],[
('Densidade e cor','Ajudam a observar a concentração da urina e o estado de hidratação.'),
('Acidez da urina','O potencial hidrogeniônico apresentado como normal ficou entre 4,5 e 7,5.'),
('Proteína','Sua presença levanta a possibilidade de alteração renal, inclusive glomerular.'),
('Glicose e cetonas','Glicose pode sugerir alteração do metabolismo da glicose. Cetonas podem aparecer no diabetes e no jejum.'),
('Pigmentos biliares e urobilinogênio','Podem contribuir para investigar alterações do fígado e das vias biliares.'),
('Nitrito','Pode indicar atividade de bactérias capazes de produzi-lo na urina.'),
('Leucócitos','Sugerem inflamação; são interpretados com os demais achados e o quadro clínico.'),
('Hemoglobina e hemácias','Apontam para sangue ou pigmento sanguíneo na amostra.'),
('Cristais','Participam da avaliação de condições associadas à formação de cálculos.')],[29,71])+
note('Nitrito negativo não exclui infecção urinária: nem todas as bactérias o produzem. Da mesma forma, ausência de glicose ou de proteína na urina não descarta, sozinha, diabetes ou doença renal.','MedlinePlus; interpretação clínica dos exames')+
h('O exemplo sem alterações')+
p('No exemplo normal, a densidade é compatível com boa hidratação, a acidez está no intervalo citado e não há proteína, glicose, cetonas ou sinais de sangramento. Nitrito e leucócitos não sugerem infecção naquela amostra. O valor do exercício é ler o conjunto, em vez de olhar apenas uma linha do laudo.')+
h('Bacterioscopia e urocultura')+
p('A bacterioscopia procura bactérias na amostra. A urocultura verifica o crescimento, identifica o microrganismo e informa sua quantidade. No exemplo negativo, não houve identificação de bactéria nem crescimento na cultura.')+
p('No exemplo positivo, cresceu <b>Escherichia coli</b>, com 100.000 unidades formadoras de colônia, valor equivalente a 10 elevado à quinta potência. Esse foi o número destacado para reconhecer bacteriúria significativa no exemplo discutido.')+
note('O laudo expressa habitualmente a contagem por mL. O significado depende de sintomas, método de coleta e população: contagens menores também podem ser relevantes. Uma contagem maior, sozinha, não mede a gravidade clínica.','Associação Europeia de Urologia, infecções urológicas')+
h('Antibiograma: sensibilidade não é uma escolha automática')+
p('O antibiograma testa a resposta do microrganismo a diferentes antibióticos. Uma bactéria polissensível é sensível à maior parte dos fármacos avaliados. Entre as classes citadas estão os aminoglicosídeos, como amicacina e gentamicina, e as cefalosporinas.')+
p('O exemplo da cefuroxima mostrou um resultado intermediário para a apresentação endovenosa e sensibilidade para a oral. A mensagem é conferir o medicamento, a apresentação e a via descritos no laudo, sem transferir automaticamente um resultado para outra situação.')+
box('Pegadinha: laboratório não substitui a paciente',p('Não concluir que a ausência de nitrito elimina a hipótese, nem usar a contagem de colônias como escala isolada de gravidade. Sintomas, sinais sistêmicos e condições da paciente mudam a interpretação.'),'red'))

body+=chapter(3,'Ardor para urinar, vontade frequente e desconforto no baixo ventre sugerem infecção na bexiga. A história clínica orienta a hipótese, mas sangue e dor também podem ter outras causas.',
p('A <b>cistite</b> é uma infecção bacteriana aguda da bexiga, também chamada de infecção urinária baixa. Os sintomas podem ser intensos e piorar rapidamente ao longo do mesmo dia. Acomete especialmente mulheres jovens, mas também pode ocorrer ao redor da menopausa.')+
h('Os sintomas se organizam em três grupos')+
table(['Grupo','Como aparece'],[
('Durante a micção','Disúria: dor ou ardor para urinar. Pode haver hematúria, que é sangue na urina.'),
('Frequência e urgência','Polaciúria: urinar muitas vezes. Nictúria: acordar à noite para urinar. Urgência: dificuldade de adiar a micção.'),
('Bexiga e pelve','Sensação de esvaziamento incompleto, desconforto suprapúbico e dor pélvica. A sensação de peso pode ser descrita como um “tijolo” no baixo ventre.')],[31,69])+
h('Quais agentes aparecem')+
p('A principal bactéria é a Escherichia coli. Também foram citados Proteus, Enterobacter, Klebsiella, Pseudomonas e Staphylococcus saprophyticus. Conhecer o agente e a sensibilidade torna-se especialmente importante quando o quadro se repete ou a resposta ao tratamento é inadequada.')+
note('A lista de agentes é ampla: Pseudomonas e Staphylococcus não pertencem ao mesmo grupo taxonômico das enterobactérias, embora todos possam participar de infecções urinárias.','classificação microbiológica')+
h('Exame de urina e cultura')+
p('A abordagem apresentada utiliza a história clínica e solicita exame de urina. A professora pede urocultura em todas as mulheres atendidas por infecção urinária, inclusive no primeiro episódio. Essa é uma conduta pessoal explicitamente distinguida das situações em que os protocolos citados tornam a cultura obrigatória.')+
quote('Eu faço urocultura em todas as mulheres que me procuram com infecção urinária, mesmo na primeira vez.','sobre sua rotina de investigação')+
rows([('Gestação','Urocultura obrigatória na abordagem discutida.'),('Dispositivos','História de cateter, cateter ureteral duplo J ou sonda exige atenção e cultura.'),('Imunossupressão','Cultura quando há infecção durante o início de tratamento imunossupressor, como em doenças autoimunes ou transplante.')])+
h('Quando ampliar a investigação')+
p('O ultrassom pode ser acrescentado conforme a necessidade. Persistência de sintomas depois de tratar a cistite exige rever o diagnóstico. A cistoscopia, quando indicada, fica para depois da fase aguda.')+
quote('Nem toda disúria e hematúria é igual a infecção urinária.','sobre diagnóstico diferencial')+
table(['Outra hipótese','Por que lembrar'],[
('Cálculo na bexiga','Pode produzir dor, sangue e ardor ao urinar.'),
('Divertículo vesical','Uma alteração da parede da bexiga pode causar desconforto e participar do diagnóstico diferencial.'),
('Tumor de bexiga','Pode causar hematúria, dor e desconforto. Sangramento não deve ser atribuído automaticamente à infecção.')],[31,69])+
box('Pegadinha: intensidade da dor não define o local',p('A cistite pode doer muito. Febre, calafrios, dor lombar e repercussão geral mudam o raciocínio e exigem investigar infecção renal ou outra complicação.'),'red'))

body+=chapter(4,'O antibiótico trata a infecção da bexiga; medidas para dor e espasmo aliviam o sofrimento. A gestação muda as opções e será tratada em um capítulo próprio.',
h('Esquemas apresentados para a mulher não grávida')+
p('As opções abaixo reproduzem os esquemas discutidos na aula. A seleção considera o quadro, os resultados microbiológicos quando disponíveis e as características da paciente. As apresentações com dois componentes devem ser lidas na ordem dos nomes dos medicamentos.')+
table(['Medicamento','Dose e frequência apresentadas','Duração'],[
('Nitrofurantoína','100 mg, três vezes ao dia.','5 dias'),
('Sulfametoxazol + trimetoprim','800 mg + 160 mg, duas vezes ao dia. Nome comercial citado: Bactrim.','3 dias'),
('Fosfomicina','3 g, em uma tomada. Nome comercial citado: Monuril.','Dose única'),
('Amoxicilina + clavulanato','500 mg + 125 mg por tomada.','7 dias'),
('Cefalosporina de segunda geração','Classe apresentada como alternativa.','7 dias')],[31,47,22])+
p('Amoxicilina com clavulanato foi apresentada na dose de 500 mg + 125 mg, diferenciando-a da dose maior empregada na discussão da pielonefrite. Para prescrever, a frequência, a formulação e os ajustes precisam ser conferidos em uma referência apropriada.')+
note('O intervalo da nitrofurantoína depende da formulação. A diretriz europeia descreve 100 mg a cada 12 horas para monoidratada/macrocristais e outros intervalos para macrocristais. Conferir função renal e bula.','Associação Europeia de Urologia, infecções urológicas')+
h('Fosfomicina: sequência de administração discutida')+
'<ol class="flow"><li><b class="t">Esvaziar a bexiga.</b> A orientação foi tomar o medicamento depois da última micção da noite.</li><li><b class="t">Preparar a dose.</b> Higienizar as mãos e dissolver o conteúdo do sachê em água, conforme a apresentação.</li><li><b class="t">Tomar a dose única.</b> O horário noturno foi escolhido para favorecer a permanência do medicamento na urina.</li></ol>'+
note('A dose não exige forçar retenção urinária: se houver vontade de urinar, não é necessário segurar a urina durante toda a noite. Seguir as instruções da bula da apresentação utilizada.','orientação de uso do medicamento')+
h('Alívio dos sintomas')+
p('Antiespasmódicos e analgésicos foram citados como adjuvantes. Anti-inflamatórios aparecem em situações selecionadas. O alívio da dor acompanha o tratamento da infecção e não substitui o antibiótico quando ele está indicado.')+
box('Pegadinha: a quinolona muda de lugar',p('Ciprofloxacino e levofloxacino foram retirados do esquema habitual de cistite apresentado. Eles reaparecem entre as opções de pielonefrite. Não transportar o tratamento da infecção renal para uma cistite simples.'),'red')+
box('Uma pergunta que muda o caminho',p('A paciente está grávida? Se estiver, não aplicar automaticamente os esquemas desta seção. O capítulo 08 reúne a abordagem específica discutida para a gestação.')))

body+=chapter(5,'Quando a infecção alcança o rim, podem surgir febre, dor nas costas e sintomas gerais. O próximo passo é medir a gravidade, procurar obstrução e decidir se a paciente precisa de internação.',
p('A <b>pielonefrite</b> é a invasão microbiana do parênquima, o tecido funcional do rim, e da pelve renal, parte do sistema coletor. A inflamação aumenta o volume do órgão e pode causar dor na região lombar.')+
note('A cápsula fibrosa que envolve diretamente o rim e a fáscia de Gerota são estruturas diferentes. A distensão da cápsula renal participa da dor; a fáscia de Gerota envolve o espaço perirrenal.','anatomia renal')+
h('Dimensão do problema e fatores de risco')+
p('Foram apresentadas estimativas de 200 mil hospitalizações por ano nos Estados Unidos, com referência a dados de 2023, e mortalidade ao redor de 10%. A relação citada foi de cinco mulheres para cada homem, e a frequência na gestação, de 1% a 2%.')+
note('A mortalidade varia amplamente com a população, a gravidade e a presença de sepse. A estimativa citada não deve ser aplicada a toda paciente com pielonefrite.','interpretação epidemiológica')+
rows([('Exposição recente','Maior frequência de relações sexuais nos últimos 30 dias, novo parceiro no ano anterior e uso de espermicida foram associados ao risco.'),('Antecedentes','Infecção urinária recente, diabetes e incontinência urinária recente também foram citados.'),('História familiar','História materna de infecção urinária apareceu como associação observada; o mecanismo não foi definido.')])+
h('O quadro clínico clássico')+
table(['Manifestação','Como reconhecer'],[
('Dor lombar','Dor no ângulo costovertebral, a região de encontro entre costelas e coluna.'),
('Repercussão geral','Febre e calafrios; náuseas e vômitos podem acompanhar.'),
('Sintomas urinários','Disúria e polaciúria podem coexistir com os sintomas renais.'),
('Sinal de Giordano','Dor provocada pela percussão cuidadosa da região lombar.')],[31,69])+
quote('Bem gentilzinho com a mão nas costinhas da mulher. Não precisa espancar.','sobre o cuidado ao pesquisar o sinal de Giordano')+
note('Febre integra a apresentação clássica enfatizada na aula. Sua ausência, especialmente em apresentações atípicas, não exclui uma infecção renal.','Associação Europeia de Urologia, infecções urológicas')+
h('História, exame físico e laboratório')+
p('A investigação inclui hemograma, ureia, creatinina e marcadores inflamatórios, com destaque para a proteína C reativa. O exame de urina deve vir acompanhado de <b>urocultura e antibiograma</b> na suspeita de pielonefrite.')+
p('A imagem procura causas que mudam a conduta. O ultrassom ajuda a avaliar obstrução urinária; a tomografia pode investigar cálculo, abscesso perirrenal e infecção focal. A radiografia simples do abdome também foi mencionada entre os exames possíveis.')+
box('Pegadinha: infecção em rim obstruído',p('A associação de infecção com obstrução pode evoluir rapidamente para sepse urinária e exige avaliação urológica urgente. Não basta escolher outro antibiótico se a drenagem está comprometida.'),'red')+
note('Na obstrução infectada, sobretudo com sepse, antibiótico e descompressão urgente fazem parte do mesmo atendimento. Não se aguarda a infecção desaparecer para drenar. A retirada definitiva do cálculo costuma ficar para depois do controle da sepse.','Associação Europeia de Urologia, litíase urinária')+
h('Indicações absolutas de internação apresentadas')+
table(['Situação','Motivo prático'],[
('Febre persistente ou sinais de sepse','Enchimento capilar lento, frequência cardíaca elevada e respiração acelerada levantam preocupação com repercussão sistêmica.'),
('Vômitos persistentes','A paciente pode não conseguir tomar ou manter o antibiótico oral.'),
('Obstrução da via urinária','Cálculo, tumor ou outra causa de bloqueio exige cuidado hospitalar e avaliação para drenagem.'),
('Diagnóstico incerto','A internação permite investigar outras causas, como doença da vesícula ou processo intestinal.'),
('Progressão da infecção','Na abordagem da aula, cistite que evolui para pielonefrite é indicação de internação.')],[35,65])+
h('Indicações relativas: avaliar o conjunto')+
table(['Condição','O que ponderar'],[
('Idade acima de 60 anos','A idade, sozinha, não resume a condição funcional ou a gravidade.'),
('Imunossupressão','A intensidade, o tempo e os achados laboratoriais ajudam a decidir.'),
('Alteração do trato urinário','Nem toda alteração anatômica implica internação automática.'),
('Condições sociais e econômicas','Acesso ao remédio, possibilidade de aplicação injetável e acompanhamento mudam a viabilidade do tratamento fora do hospital.'),
('Leucocitose isolada','Leucócitos elevados no hemograma, sem outros sinais, não definem internação; sinais de sepse mudam essa decisão.')],[35,65])+
figure('decisao','Fluxo de avaliação dos sintomas, suspeita de cistite ou pielonefrite, gravidade e internação.','Organização do raciocínio clínico da aula; a gestação tem indicação própria de internação na pielonefrite.')+
p('Uma paciente clinicamente estável pode ser avaliada para tratamento ambulatorial, com acesso efetivo à medicação e possibilidade de reavaliação. Esse raciocínio não se aplica à gestante com pielonefrite, para quem a internação foi enfatizada.'))

body+=chapter(6,'A paciente estável pode ter opções fora do hospital; a paciente grave precisa de suporte e tratamento hospitalar. Em ambos os casos, a resposta clínica e o antibiograma orientam a reavaliação.',
h('As opções dependem do cenário')+
table(['Cenário','Antibióticos citados'],[
('Ambulatório, com estabilidade','Ciprofloxacino ou levofloxacino; sulfametoxazol com trimetoprim; cefalosporinas; amoxicilina com clavulanato; aminoglicosídeos. A ampicilina com sulbactam também foi mencionada entre as possibilidades parenterais.'),
('Hospital','Quinolonas endovenosas; aminoglicosídeos; cefalosporinas de segunda ou terceira geração; ampicilina com sulbactam; piperacilina com tazobactam; ampicilina associada a aminoglicosídeo; carbapenêmicos, como imipenem e meropenem.')],[29,71])+
p('Entre as possibilidades de aplicação fora do hospital, foram discutidos ceftriaxona por via intramuscular e aminoglicosídeos por via intramuscular ou endovenosa, desde que exista estrutura para o cuidado. A escolha da via não elimina a necessidade de observar a evolução.')+
note('A ceftriaxona é uma cefalosporina de terceira geração. Antibiótico, via e dose dependem de sensibilidade, gravidade, função renal e disponibilidade de acompanhamento. Nitrofurantoína e fosfomicina oral não atingem níveis adequados no tecido renal para tratar pielonefrite.','Associação Europeia de Urologia, infecções urológicas')+
box('A dose que muda na comparação da aula',p('Para a pielonefrite, a amoxicilina com clavulanato foi apresentada como <b>875 mg + 125 mg</b>, por via oral. Para a cistite, foi discutida a apresentação de 500 mg + 125 mg. Conferir frequência e ajustes na referência de prescrição.'))+
p('Piperacilina com tazobactam foi citada como preferência habitual da professora no contexto hospitalar. Trata-se de uma preferência de prática, não de uma escolha automática para qualquer paciente.')+
h('Duração e transição no esquema ensinado')+
'<ol class="flow"><li><b class="t">Iniciar a via adequada à gravidade.</b> No cenário hospitalar discutido, o início é endovenoso.</li><li><b class="t">Reavaliar a estabilidade.</b> O esquema da aula utiliza pelo menos 7 dias de tratamento e pode chegar a 14 dias nos casos mais graves.</li><li><b class="t">Considerar transição.</b> Depois de 7 dias, paciente estável, sem febre por 48 horas, hemograma normal e sem complicação pode passar ao tratamento oral.</li><li><b class="t">Completar e acompanhar.</b> O exemplo foi de 7 dias endovenosos seguidos de 7 dias por via oral, com retorno ambulatorial a cada 2 dias depois da alta.</li></ol>'+
note('Diretrizes atuais admitem transição oral mais precoce quando há melhora, tolerância oral e opção eficaz; não exigem sempre 7 dias endovenosos. Duração total depende da situação clínica, do agente e de complicações.','Sociedade Americana de Doenças Infecciosas, 2025')+
h('Quando é preciso intervir na via urinária')+
p('Obstrução por cálculo ou tumor pode perpetuar a infecção e se associar a lesão renal aguda. As situações destacadas para intervenção foram obstrução, pionefrose e abscesso renal. Antibiótico e avaliação da necessidade de drenagem devem ser pensados em conjunto.')+
table(['Situação','Ideia central'],[
('Obstrução','Há um obstáculo à passagem de urina; controlar o foco exige avaliar a drenagem.'),
('Pionefrose','Infecção purulenta do sistema coletor, geralmente associada à obstrução. É uma complicação que pode exigir drenagem urológica.'),
('Abscesso renal ou perirrenal','Coleção localizada de pus no rim ou ao redor dele; a localização e as características orientam o cuidado especializado.')],[32,68])+
note('Pionefrose e abscesso perirrenal não são sinônimos. Pus ao redor do rim indica uma coleção perirrenal; pus no sistema coletor caracteriza pionefrose. Drenagem de uma obstrução infectada é urgente; a cirurgia definitiva da causa é outra etapa.','anatomia clínica; Associação Europeia de Urologia, litíase urinária')+
box('Pegadinha: drenar e operar definitivamente não são a mesma coisa',p('Não confundir o controle urgente de um sistema infectado e obstruído com a retirada definitiva do cálculo. Adiar a cirurgia definitiva não significa adiar a drenagem necessária.'),'red')+
h('O que foi dito sobre a tabela de antibióticos')+
quote('Vocês não precisam decorar, mas precisam saber que existe.','sobre a tabela de apoio com doses e efeitos adversos')+
quote('Não cai a tabela na prova. É só para vocês terem como um apoio.','delimitando a cobrança da tabela')+
p('O objetivo é reconhecer as possibilidades e saber consultar uma referência apropriada. A seleção de um antibiótico exige mais do que memorizar uma lista de nomes.'))

body+=chapter(7,'A mesma infecção pode ser mais difícil de controlar quando há gestação, doença associada, dispositivo ou obstáculo à saída da urina. Esses fatores mudam a avaliação e o acompanhamento.',
p('A classificação apresentada considera complicada a infecção que ocorre em condições com maior chance de persistência, falha terapêutica ou repercussão sistêmica. Ela reúne características da paciente, do episódio e da via urinária.')+
rows([('Paciente','Diabetes ou gestação.'),('Tempo e origem','Sintomas por mais de 7 dias ou infecção adquirida durante internação, frequentemente relacionada à sonda vesical.'),('Função renal','Evolução com falência renal, entendida clinicamente como comprometimento importante da função dos rins.')])+
rows([('Drenagem','Obstrução ou bexiga neurogênica, que pode dificultar o esvaziamento.'),('Dispositivos','Cateter uretral, sonda vesical, cateter ureteral, stent ou nefrostomia na via urinária.')])+
h('A pergunta útil em cada episódio')+
p('Existe algo que favoreça a permanência da bactéria ou dificulte que o tratamento funcione? Um cálculo obstrutivo, um dispositivo e uma alteração funcional exigem atenção além da escolha do antibiótico.')+
note('Classificações variam entre diretrizes. Algumas organizam a infecção como localizada ou sistêmica e avaliam fatores de risco separadamente. Esta seção preserva a classificação apresentada na aula.','Associação Europeia de Urologia, infecções urológicas')+
box('Conecte com a decisão de internação',p('Ter um fator complicador não substitui a avaliação de gravidade. Obstrução infectada e sepse exigem ação urgente; outras condições pedem análise individual de estabilidade, acesso à medicação e seguimento.'))+h('Da classificação à conduta')+p('Verifique se a urina consegue sair, se há um dispositivo na via urinária e se a função renal piorou. Essas três observações ligam a classificação ao problema que precisa ser resolvido, além da escolha do antibiótico.'))

body+=chapter(8,'Na gravidez, bactérias na urina merecem cuidado mesmo quando não causam sintomas. O tratamento e o controle da resposta ajudam a evitar que a infecção alcance o rim e comprometa a gestação.',
h('Por que a gestação facilita a ascensão')+
p('Durante a gestação, há aumento do fluxo sanguíneo renal e mudanças de tamanho e dilatação na via urinária. O relaxamento da musculatura do ureter favorece a estase e a ascensão das bactérias da bexiga para a via superior.')+
p('A <b>bacteriúria assintomática</b> é a presença de bactérias na urina sem sintomas urinários. A aula enfatiza seu tratamento na gestante para reduzir o risco de progressão à pielonefrite.')+
h('O que está em risco')+
p('A infecção urinária pode afetar a mãe, o feto e a gestação. Foram mencionados prematuridade, baixo peso ao nascer, comprometimento do crescimento e aumento do risco de óbito fetal. A estimativa de mortalidade fetal apresentada foi de duas a quase duas vezes e meia.')+
note('O tamanho do risco depende da população, do tipo de infecção e do tratamento. O multiplicador citado na aula não é uma previsão individual para toda gestante com bacteriúria.','interpretação de risco obstétrico')+
note('Bactérias vistas apenas no exame de urina não confirmam, sozinhas, bacteriúria assintomática: a cultura orienta o diagnóstico. Na paciente sintomática, colher antes do antibiótico quando possível, sem atrasar tratamento necessário.','Colégio Americano de Obstetras e Ginecologistas, 2023')+
h('Investigar, tratar e conferir a resposta')+
'<ol class="flow"><li><b class="t">Colher a cultura.</b> A urocultura integra a investigação da gestante.</li><li><b class="t">Não atrasar a abordagem da infecção sintomática.</b> A conduta da aula é iniciar tratamento empírico e depois ajustá-lo conforme a resposta e a cultura.</li><li><b class="t">Reavaliar em 2 a 3 dias se não melhorar.</b> Rever sintomas, exame de urina e adequação do antibiótico; a falta de resposta exige nova decisão clínica.</li><li><b class="t">Fazer cultura de controle.</b> A orientação ensinada foi repetir a urocultura em uma semana depois de tratar, para verificar a eliminação bacteriana.</li><li><b class="t">Internar se houver pielonefrite.</b> A evolução para infecção renal na gestante exige internação na abordagem apresentada.</li></ol>'+
figure('gestacao','Três etapas do acompanhamento na gestação: identificar, tratar e observar, confirmar resposta.','Sequência de acompanhamento apresentada, com retorno e cultura de controle.')+
h('Medicamentos por situação, conforme a aula')+
table(['Situação','Opções citadas','Observação'],[
('Cistite','Amoxicilina; amoxicilina com clavulanato; cefalexina; cefpodoxima.','Escolher de acordo com sensibilidade e contexto.'),
('Pielonefrite','Ampicilina com gentamicina; cefalosporinas injetáveis: cefalotina, cefazolina, cefuroxima e ceftriaxona.','Tratamento hospitalar; avaliar resposta e função renal.'),
('Outras opções hospitalares','Meropenem, ertapenem e aztreonam foram citados.','Seleção especializada, conforme gravidade e resistência.'),
('Fosfomicina','Reservada, na abordagem da aula, para situações específicas de resistência.','Não foi apresentada como primeira escolha habitual.'),
('Nitrofurantoína e sulfametoxazol com trimetoprim','Uso condicionado ao trimestre e às características da gestação.','Não foram apresentadas como primeira escolha na aula.')],[25,45,30])+
note('A escolha empírica de amoxicilina ou ampicilina requer cautela pela resistência de Escherichia coli. Nitrofurantoína e fosfomicina podem ser opções para infecção baixa na gravidez, conforme contexto; não servem para pielonefrite. Aminoglicosídeos exigem avaliação específica, sem presumir segurança universal.','Colégio Americano de Obstetras e Ginecologistas, 2023')+
h('O papel do clavulanato')+
p('A associação da amoxicilina ao clavulanato foi discutida como forma de ampliar a ação contra algumas bactérias. O clavulanato atua sobre mecanismos bacterianos de resistência, permitindo que a amoxicilina mantenha atividade em determinadas situações.')+
note('A amoxicilina já tem atividade contra alguns microrganismos Gram-negativos. O clavulanato inibe determinadas beta-lactamases; ele não torna toda bactéria resistente sensível à associação.','farmacologia dos betalactâmicos')+
box('Pegadinha: não usar quinolonas na gestante',p('A orientação da aula é evitar ciprofloxacino e levofloxacino durante a gestação. A justificativa discutida foi a preocupação com efeitos sobre as cartilagens e articulações fetais; há outras classes disponíveis para as situações apropriadas.'),'red')+
note('O risco articular citado é uma preocupação de segurança, especialmente a partir de dados experimentais; não significa que uma exposição cause inevitavelmente fechamento das cartilagens ou disfunção fetal. A escolha é individualizada pela equipe assistente.','avaliação de segurança de medicamentos na gestação')+
h('Não misturar os dois cenários')+
box('Quatro diferenças para guardar',ul([
'<b>Fosfomicina:</b> opção habitual discutida para a cistite fora da gestação; reservada pela professora a situações selecionadas na gravidez.',
'<b>Bacteriúria sem sintomas:</b> na gestante, pesquisar e tratar foi uma prioridade.',
'<b>Pielonefrite:</b> estabilidade pode permitir avaliação ambulatorial fora da gravidez; na gestante, a orientação é internar.',
'<b>Cultura:</b> pedir para todas foi uma escolha pessoal fora da gestação; na gravidez, cultura e controle foram enfatizados.']))+p('Febre, dor lombar e vômitos pedem reavaliação imediata, sem esperar o prazo de retorno.'))

body+=h('Erros comuns para evitar')+ul(['Tratar a gestante como uma mulher não grávida.','Escolher o antibiótico sem distinguir bexiga de rim.','Confundir alívio dos sintomas com resolução da infecção.'])+references

vesp_items=[
('01 · Paciente e hábitos','Cistite: 11% ao ano; quase 50% na vida. Capacidade vesical citada: 350–360 mL. Intervalo miccional sugerido: 1h30–1h40. Risco: frequência sexual nos últimos 30 dias e novo parceiro no último ano.'),
('02 · Exames','Acidez citada: 4,5–7,5. Cultura do exemplo: 100.000 unidades formadoras de colônia.'),
('03 · Cistite','Ardor, frequência, urgência, sangue e desconforto suprapúbico. Cultura nos grupos citados. Diferenciais: cálculo, divertículo e tumor.'),
('04 · Antibióticos','Nitrofurantoína: 100 mg, três vezes ao dia, 5 dias, na fala; conferir formulação. Sulfametoxazol + trimetoprim: 800 mg + 160 mg, duas vezes ao dia, 3 dias. Fosfomicina: 3 g, dose única.'),
('04 · Alternativas','Amoxicilina + clavulanato: 500 mg + 125 mg, 7 dias; cefalosporina de segunda geração: 7 dias. Conferir frequências. Quinolonas fora do esquema habitual de cistite ensinado.'),
('05 · Rim e gravidade','Estimativas citadas: 200 mil internações/ano nos Estados Unidos; mortalidade de 10% no dado apresentado; relação 5 mulheres:1 homem; 1–2% das gestantes.'),
('05 · Internação','Sepse, febre persistente, vômitos persistentes, obstrução, incerteza diagnóstica ou progressão, na abordagem da aula. Idade acima de 60 anos é um critério relativo.'),
('06 · Tratamento renal','Amoxicilina + clavulanato: 875 mg + 125 mg citados. Esquema ensinado: 7–14 dias; transição após 7 dias, estabilidade e 48 horas sem febre. Retorno a cada 2 dias.'),
('06–07 · Foco e risco','Obstrução, pionefrose e abscesso exigem avaliar intervenção. Complicadores incluem diabetes, gestação, sintomas acima de 7 dias, dispositivos e disfunção renal.'),
('08 · Gestação','Mortalidade fetal: estimativa citada de 2–2,5 vezes. Reavaliar sem resposta em 2–3 dias; cultura de controle em uma semana. Pielonefrite: internar. Evitar quinolonas.'),
]
body+='<section class="vesp" id="s09"><div class="sec-head"><span class="num">09</span><h2>Página de véspera</h2></div><p class="intro">Decisões e números na ordem da trilha. A tabela de apoio foi excluída da cobrança pela professora.</p>'+''.join('<div class="item"><p><b>'+a+'.</b> '+b+'</p></div>' for a,b in vesp_items)+note('Nitrito negativo não exclui infecção. Obstrução infectada pode exigir drenagem urgente junto ao antibiótico. Riscos e doses precisam do contexto clínico; os números da aula não são previsões individuais.','notas clínicas dos capítulos 02, 05 e 08')+'</section>'

gloss=[
('Abscesso','Coleção localizada de pus.'),('Angulo costovertebral','Região onde se encontram as últimas costelas e a coluna; local de pesquisa da dor renal.'),('Antiespasmódico','Medicamento que reduz espasmos de musculatura lisa.'),('Bacterioscopia','Observação de bactérias na amostra ao microscópio.'),('Beta-lactamase','Enzima bacteriana capaz de inativar certos antibióticos.'),('Cistocele','Descida da bexiga em direção à parede da vagina.'),('Cistoscopia','Exame do interior da bexiga por uma pequena câmera.'),('Constipação','Dificuldade persistente para evacuar.'),('Disúria','Dor ou ardor ao urinar.'),('Enterocele','Descida de uma porção do intestino em direção à região vaginal.'),('Esvaziamento incompleto','Sensação de que ainda resta urina depois de urinar.'),('Hematúria','Presença de sangue na urina.'),('Hipoestrogenismo','Redução dos níveis de estrogênio.'),('Imunossupressão','Redução da capacidade de defesa do organismo.'),('Leucocitose','Aumento do número de leucócitos no sangue.'),('Litíase','Presença ou formação de cálculos.'),('Nefrostomia','Drenagem do rim por um cateter que sai pela pele.'),('Bexiga neurogênica','Bexiga com alteração de funcionamento por problema neurológico.'),('Nictúria','Despertar durante a noite para urinar.'),('Pelve renal','Parte do sistema coletor que reúne a urina e continua no ureter.'),('Perirrenal','Situado ao redor do rim.'),('Pionefrose','Acúmulo de urina infectada e pus no sistema coletor, geralmente com obstrução.'),('Polaciúria','Aumento da frequência das micções.'),('Polissensível','Sensível à maior parte dos antibióticos testados.'),('Sepse','Disfunção de órgãos causada por resposta desregulada do organismo à infecção.'),('Stent ureteral','Dispositivo colocado no ureter para ajudar a manter a passagem da urina.'),('Suprapúbico','Localizado no baixo ventre, acima do osso púbico.'),('Tratamento empírico','Tratamento iniciado antes de conhecer o resultado microbiológico definitivo.')]
# Ordem alfabética com acentos normalizados apenas para ordenar.
import unicodedata
gloss.sort(key=lambda z:unicodedata.normalize('NFD',z[0]).encode('ascii','ignore').lower())
gloss=[('Ângulo costovertebral' if a=='Angulo costovertebral' else a,b) for a,b in gloss]
body+='<section id="s10"><div class="sec-head"><span class="num">10</span><h2>Palavras da aula</h2></div>'+p('Termos em linguagem simples, em ordem alfabética.')
for i in range(0,len(gloss),3):body+=rows(gloss[i:i+3])
body+='<h3>Anotações</h3>{{NOTAS}}</section>'

html='<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>Nefrologia · Aula 6 · Infecção urinária</title><meta name="author" content="Mauricio Faria"><meta name="rodape" content="Mauricio Faria · Nefrologia · Aula 6 — Infecção urinária"><link rel="stylesheet" href="apostila.css"><style>'+style+'</style></head><body>'+cover+legend+body+'</body></html>'
(ROOT/'apostila.html').write_text(html)
print('HTML gerado:',len(html),'caracteres')
