from pathlib import Path
import json, re, html

ROOT = Path(__file__).resolve().parent
meta = json.loads((ROOT/'identificacao.json').read_text())
disc = meta['disciplina']
aula = (' · Aula ' + str(meta['numero'])) if meta.get('numero') else ''
prof = meta['professor']
data = (' · ' + meta['data_extenso']) if meta.get('data_extenso') else ''
titulo = 'Tabagismo e cigarros eletrônicos'
rotulos = ['Dependência','Abordagem','Dia D','Medicamentos','Seguimento','Dispositivos','Riscos','Prevenção']
capitulos = ['Por que é difícil parar?', 'Abordar e avaliar', 'Apoio comportamental e Dia D', 'Medicamentos: indicação e diferenças', 'Cessação, recaída e seguimento', 'Cigarros eletrônicos e a conta do rótulo', 'Lesão pulmonar e redução de danos', 'Prevenção e cuidado compartilhado']
aberturas = [
'Parar de fumar envolve o que o corpo pede, o que a pessoa sente e o que ela se acostumou a fazer. Por isso, tratar só a nicotina deixa parte do problema sem cuidado.',
'Toda consulta pode abrir espaço para ajudar quem fuma. Antes de combinar o tratamento, é preciso entender a vontade de parar, as dificuldades e as tentativas anteriores.',
'O plano precisa caber na vida da pessoa. Marcar uma data, reconhecer os gatilhos e mudar a rotina ajuda a tirar o cigarro dos momentos em que ele aparecia automaticamente.',
'A medicação pode aliviar o desconforto de ficar sem nicotina e a vontade de fumar. A escolha depende da história, dos riscos e das necessidades de cada pessoa.',
'Parar traz benefícios mesmo depois de muitos anos fumando. Se a pessoa voltar a fumar, é preciso entender o que aconteceu e ajustar o plano para a próxima tentativa.',
'O pod produz um aerossol e pode concentrar muita nicotina. Para entender o consumo, peça a embalagem e verifique a concentração, o volume do refil e quanto tempo ele dura.',
'Produtos inalados podem causar lesão pulmonar aguda grave. Uma estratégia de redução de danos usada em outro país não transforma qualquer vape em um medicamento aprovado.',
'Cuidar do tabagismo também é evitar que outras pessoas comecem e proteger quem convive com a fumaça. Escutar, combinar mudanças e acompanhar faz parte do tratamento.'
]

def cab(n,t):
    return f'<div class="sec-head"><div class="lado"><span class="k">Seção</span><span class="num">{n:02d}</span></div><div class="corpo"><h2>{t}</h2></div></div>'

def section(n, body):
    faixa='<div class="aqui" aria-label="Você está aqui">'+''.join(f'<span class="{"on" if i==n-1 else "feito" if i<n-1 else ""}">{r}</span>' for i,r in enumerate(rotulos))+'</div>'
    return f'<section id="s{n:02d}"><div class="chapter-start">{cab(n,capitulos[n-1])}{faixa}<div class="simples"><div class="kick">Em palavras simples</div><p>{aberturas[n-1]}</p></div></div>{body}</section>'

def box(t,body,cor=''):
    return f'<div class="box {cor}"><div class="kick">{t}</div>{body}</div>'
def quote(t):
    return f'<div class="quote"><p>“{t}”</p><div class="who">Dr. Cássio</div></div>'
def fig(nome,alt,leg=''):
    return f'<div class="figure fig-{nome}"><img src="fig/{nome}.svg" alt="{html.escape(alt)}">'+(f'<p class="leg">{leg}</p>' if leg else '')+'</div>'
def rows(items,cl=''):
    return '<div class="rows '+cl+'">'+''.join(f'<div class="row"><div class="k">{k}</div><div class="v">{v}</div></div>' for k,v in items)+'</div>'
def note(t,ref):
    return f'<div class="livros"><b>Complemento: fora da aula.</b> {t} <a href="#fontes">[{ref}]</a></div>'

molde=(ROOT/'apostila-molde.md').read_text()
css=re.search(r'```css\n(.*?)```',molde,re.S).group(1)
custom='''
@font-face { font-family: Inter; src: url(fonts/Inter-Regular.ttf); font-weight:400; }
@font-face { font-family: Inter; src: url(fonts/Inter-Bold.ttf); font-weight:700; }
@font-face { font-family: "Inter Medium"; src: url(fonts/Inter-Medium.ttf); font-weight:500; }
@font-face { font-family: "Inter SemiBold"; src: url(fonts/Inter-SemiBold.ttf); font-weight:600; }
.cover .keynums { margin-top:12mm; }
.cover h1 { font-size:30pt; }
.cover .sub { margin-bottom:14pt; }
.cover .toc a { font-size:8.9pt; padding:3.1pt 0; }
.cover .note { font-size:7.6pt; }
.cover .toc { padding-top:10pt; padding-bottom:10pt; }
.chapter-start { break-inside:avoid; }
.aqui { margin-bottom:9pt; }
.aqui span { color:#6C6C70; }
.src,.figure .leg { color:#6C6C70; }
.simples .kick { font-size:6.8pt; margin-bottom:3pt; }
.simples p { font-size:9.8pt; }
.livros a { color:#6E3AA7; }
.livros { font-size:8pt; line-height:1.5; }
.reg { line-height:1.5; }
.compact p { margin-bottom:3pt; }
.formula { font-family:"Inter SemiBold"; color:#16315C; font-size:11.5pt; text-align:center; margin:10pt 0; }
.fig-conta-pod { padding-top:13pt; padding-bottom:13pt; }
.vesp .item { display:block; padding:9pt 12pt; margin-bottom:6pt; }
.vesp .item p { font-size:10.2pt; line-height:1.5; }
.vesp .item b { color:#16315C; }
.vesp .sec-head { margin-top:0; margin-bottom:8pt; }
.glossario { break-before:page; }
.glossario .sec-head { margin-top:0; }
.source-list { font-size:7.8pt; line-height:1.5; }
.source-list a { color:#0B5BD3; text-decoration:none; }
.source-list li { margin-bottom:5pt; }
'''
head=f'<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><title>{disc}{aula} · {titulo}</title><meta name="rodape" content="Mauricio Faria · {disc}{aula} — Tabagismo"><link rel="stylesheet" href="apostila.css"><style>{css}\n{custom}</style></head><body>'
toc=[(0,'Recados da disciplina')]+list(enumerate(capitulos,1))+[(9,'Página de véspera'),(10,'Glossário, fontes e anotações')]
cover=f'''<div class="cover"><div class="kicker">{disc}{aula} · Tabagismo</div><h1>Tabagismo e<br>cigarros eletrônicos</h1><p class="sub">Da dependência à cessação: abordagem, tratamento e riscos dos novos produtos.</p><div class="author"><span class="av">C</span><div><b>{prof}</b><span>Professor de {disc}{data}</span></div></div><div class="keynums"><div class="kick">Três números para levar</div><div class="kn-grid"><div class="kn"><div class="n">3</div><div class="l">dimensões da dependência</div></div><div class="kn"><div class="n">7–30 dias</div><div class="l">intervalo para combinar o Dia D</div></div><div class="kn"><div class="n">5%</div><div class="l">50 mg/mL no exemplo do rótulo</div></div></div></div><div class="toc"><div class="kick">Nesta apostila</div>'''+''.join(f'<a href="#s{n:02d}"><span class="tn">{n:02d}</span><span class="tt">{t}</span><span class="pg">{{{{s{n:02d}}}}}</span></a>' for n,t in toc)+'''<p class="note">Entenda a dependência, organize o cuidado e revise as decisões que fazem diferença para o paciente.</p></div></div>'''
legend='''<div class="legend"><div class="kick">Como ler esta apostila</div><div class="lg-grid">
<div class="lg"><span class="sw blue"></span><div><b>Azul</b> conteúdo e raciocínio da aula</div></div><div class="lg"><span class="sw green"></span><div><b>Verde</b> dose ou valor de referência</div></div>
<div class="lg"><span class="sw red"></span><div><b>Vermelho</b> pegadinha ou alerta</div></div><div class="lg"><span class="sw orange"></span><div><b>Laranja</b> fala do professor</div></div>
<div class="lg"><span class="sw purple"></span><div><b>Roxo</b> complemento fora da aula</div></div><div class="lg"><span class="prova">PROVA</span><div><b>Prova</b> destaque do professor</div></div>
<div class="lg"><span class="sw simples-sw"></span><div><b>Em palavras simples</b> abertura do capítulo</div></div><div class="lg"><span class="sw aqui-sw"></span><div><b>Você está aqui</b> posição na trilha</div></div></div></div>'''
professor=f'<div class="prof"><div class="kick">Sobre o professor · {prof}</div>'+rows([('Atuação',f'Professor de {disc}, com experiência em grupo de tratamento do tabagismo na Unimed.')])+'</div>'
recados='<section id="s00">'+cab(0,'Recados da disciplina')+rows([('Avaliação','11 questões em formato de casos clínicos, valendo <b>5,0 pontos no total</b>.'),('Formato','Alternativas A, B, C e D, sem combinações de assertivas do tipo “I e II corretas”.'),('Organização','A possibilidade de ampliação do tempo da prova depende de confirmação pela disciplina.')])+'</section>'+fig('trilha','Oito etapas do cuidado, da dependência à prevenção','Siga a trilha: entender o problema, combinar o cuidado e acompanhar a mudança.')+'<p>A lógica do cuidado é entender por que a pessoa fuma, construir um plano que faça sentido para ela e acompanhar o que acontece depois. O medicamento é uma parte desse processo.</p>'+quote('Se você não tem tempo e paciência para escutar o tabagista, você não vai conseguir chegar a lugar nenhum.')

b1='''<p>O tabagismo é um <b>transtorno crônico relacionado ao uso e à dependência de nicotina</b>, associado à exposição a produtos inalados e a danos agudos e crônicos. A nicotina permanece no centro do problema, mesmo com a diversidade de produtos: cigarro convencional, narguilé, cigarros eletrônicos e outras formas de tabaco.</p>
<p>O dano não aparece apenas depois de muitos anos. Os cigarros eletrônicos também podem estar associados à lesão pulmonar aguda. Entre os danos de longo prazo estão câncer, infarto e doença pulmonar obstrutiva crônica.</p>
<div class="reg"><b>Uma distinção importante.</b> A dependência é crônica; os danos à saúde podem ser agudos ou crônicos. Uma exposição recente não garante ausência de risco.</div>
<h3>Uma doença evitável que continua relevante</h3>
<p>Como dimensão do problema, o Dr. Cássio apresenta estimativas de 1,2 bilhão de pessoas que fumam, mais de 7 milhões de mortes relacionadas ao tabagismo e 1,5 milhão relacionadas à exposição passiva. A carga de doença vai além do pulmão e inclui alterações cardíacas e vasculares.</p>
<div class="reg"><b>Panorama epidemiológico.</b> São estimativas de ordem de grandeza. A redução do consumo de cigarros convencionais convive com o crescimento dos cigarros eletrônicos, o que exige atenção à mudança dos produtos e dos padrões de uso.</div>
<h3>As três dimensões da dependência</h3>'''+fig('dependencia','Dimensões física, psicológica e comportamental da dependência')+'''
<p>Na dimensão física, a nicotina chega rapidamente ao cérebro — cerca de <b>4 segundos</b>, na explicação do Dr. Cássio — e ativa receptores ligados à sensação de recompensa. Quando o efeito passa, surge a busca por nova exposição.</p>
<p>A dimensão psicológica aparece na relação do cigarro com ansiedade, estresse, concentração e emoções. A pessoa pode associá-lo tanto a um momento difícil quanto a uma comemoração.</p>
<p>A dimensão comportamental é sustentada pela repetição: entrar no carro, terminar o almoço, tomar café ou ir à padaria passam a lembrar o cigarro. Essa parte pode ser esquecida tanto pelo paciente quanto pelo médico, embora seja decisiva para romper a associação com a rotina.</p>'''+quote('Como é que eu vou tirar o meu cigarro do meu dia a dia se eu fizer as mesmas coisas na minha rotina de sempre?')+box('Pegadinha do professor','<p>Achar que tratar a nicotina resolve tudo. A rotina e a relação emocional com o cigarro também precisam entrar no plano.</p>','red')

b2='''<p>Todo usuário deve ser abordado, mesmo quando ainda não está pronto para parar. O objetivo é oferecer ajuda e explicar benefícios, sem impor uma decisão nem transformar a consulta em repreensão. Uma consulta por tosse ou por outro motivo também pode abrir essa conversa.</p>'''+quote('Eu posso te ajudar a parar se você quiser.')+'''
<h3>Cinco passos para organizar a consulta</h3><ol class="flow">
<li><b class="t">Perguntar.</b> Investigar se usa tabaco ou nicotina e qual produto utiliza, incluindo vape e pod.</li>
<li><b class="t">Aconselhar.</b> Recomendar a cessação de forma clara e personalizada, enfatizando benefícios e oferecendo ajuda.</li>
<li><b class="t">Avaliar.</b> Explorar motivação, dependência, tentativas prévias, comorbidades e o momento de vida.</li>
<li><b class="t">Ajudar.</b> Construir com a pessoa um plano de ação para parar.</li>
<li><b class="t">Acompanhar.</b> Verificar dificuldades, sustentar a mudança e prevenir recaídas.</li></ol>
<p>A sequência organiza o cuidado sem transformar a consulta em um roteiro rígido. Duas perguntas orientam o início: <b>“Você quer parar?” e “Este é um bom momento para você?”</b>. Um paciente motivado, mas vivendo demissões e insegurança no trabalho, pode precisar de um plano que leve esse contexto em conta.</p>
<p>Também é necessário diferenciar quem não consegue interromper o uso de quem para, mas volta depois. Nesse segundo cenário, o plano precisa dar atenção especial à manutenção da cessação e aos gatilhos da recaída.</p>'''+box('Pegadinha do professor','<p>Tratar a ambivalência como falta de vontade ou de caráter. O tabagismo é uma doença, e a dependência tem componentes físicos, psicológicos e comportamentais.</p>','red')+'''
<h3>Fagerström: um instrumento dentro da avaliação</h3><p>O teste ajuda a avaliar a dependência de nicotina. Duas perguntas têm especial importância clínica: <b>quanto tempo passa até o primeiro cigarro ao acordar e quantos cigarros a pessoa fuma por dia</b>.</p>'''+rows([('0–2 pontos','Dependência muito baixa.'),('3–4 pontos','Dependência baixa.'),('5 pontos','Dependência média.')])+'''
<p class="small">Faixas iniciais da classificação: o escore é parte da avaliação, não uma decisão de tratamento isolada.</p>
<p>O resultado precisa ser interpretado junto do padrão atual de uso, da história de abstinência e das tentativas anteriores: o que a pessoa sentiu, por que voltou e o que atrapalhou o tratamento. O instrumento integra a avaliação do tabagismo, mas não substitui a história clínica.</p>'''+quote('Existe uma doença que é tabagismo e a gente precisa tratar você.')

b3='''<h3 data-bm="Apoio comportamental">Apoio comportamental <span class="prova">PROVA</span></h3>
<p>Os dois eixos do tratamento são o apoio comportamental e o tratamento farmacológico. Para a prova, adote a expressão <b>apoio comportamental</b>, como orientado pelo Dr. Cássio. A associação com medicação, quando indicada, é mais eficaz do que cada abordagem isolada.</p>'''+quote('Tirei na nossa prova o “cognitivo” porque senão fica um negócio muito psicológico.')+'''
<p>Esse apoio inclui aconselhamento estruturado, identificação de gatilhos, estratégias para lidar com eles, plano de cessação e prevenção de recaídas. Há quem pare sozinho ou com apenas uma das abordagens; a escolha precisa considerar a pessoa, sem perder de vista o benefício da combinação.</p>
<h3>O plano começa na primeira conversa</h3><p>A anamnese explora onde e quando a pessoa fuma, há quanto tempo, se outras pessoas em casa fumam, o que já tentou e como foram as experiências anteriores. A preparação se organiza em quatro medidas:</p>
<ol class="flow"><li><b class="t">Marcar o Dia D.</b> Combinar uma data para parar, entre 7 e 30 dias. Um intervalo de cerca de 15 dias permite preparar a mudança.</li>
<li><b class="t">Iniciar atividade física.</b> Incluí-la na preparação e na mudança de rotina.</li>
<li><b class="t">Reconhecer os gatilhos.</b> Observar os momentos ligados ao cigarro: café, sacada, pós-almoço e saída para o trabalho.</li>
<li><b class="t">Preparar a redução do uso.</b> Perceber quais cigarros podem ser evitados e reduzir o consumo até a data combinada.</li></ol>'''+fig('plano','Preparação, Dia D e acompanhamento')+'''
<p>Entre os exemplos de preparação estão diminuir de 20 para 19, 18 e 17 cigarros, adiar um cigarro que não parece necessário ou não fumá-lo inteiro. Para o pod, a contagem é menos simples; uma possibilidade é reduzir de duas tragadas para uma. Essas estratégias preparam a cessação e precisam ser adaptadas a cada pessoa.</p>
<h3>Três dicas que o professor repete</h3><ol class="flow"><li><b class="t">Querer parar.</b> A vontade e o momento de vida entram na conversa.</li><li><b class="t">Marcar a data.</b> O Dia D transforma a intenção em um compromisso concreto.</li><li><b class="t">Fazer diferente nesse dia.</b> Mudar a rotina que ligava o cigarro ao café, ao almoço e aos outros hábitos.</li></ol>'''+box('Pegadinha do professor','<p>Esperar que apenas a medicação faça a pessoa parar de fumar. Ela ajuda com a abstinência e a fissura; a mudança de rotina e o acompanhamento continuam necessários.</p>','red')+'''
<h3>Uma linguagem que acolhe</h3><p>Evite a palavra “vício”, por seu peso moral, e converse sobre hábito e dependência. Uma linguagem respeitosa não retira o caráter de doença nem a necessidade de cuidado.</p>'''+quote('A gente não usa mais a palavra vício, a gente usa o hábito.')

b4='''<h3>Quando considerar farmacoterapia</h3><p>Os critérios práticos enfatizados pelo Dr. Cássio são sintomas relevantes de abstinência, consumo maior que 5 cigarros por dia, primeiro cigarro em menos de 1 hora após acordar e Fagerström maior que 4. A decisão é <b>individualizada</b>, considerando preferências, contraindicações, comorbidades e tentativas anteriores.</p>'''+note('A linha de cuidado do Ministério da Saúde inclui os valores de fronteira: 5 ou mais cigarros/dia, primeiro cigarro em até 1 hora e Fagerström igual ou maior que 4.','1')+'''
<p>O Dr. Cássio adota a prescrição para adultos e não utiliza medicação em menores de 18 anos, embora reconheça situações de exceção. Mesmo quem reduziu para 2 ou 3 cigarros por dia e não consegue cessar pode precisar de ajuda, como a goma em situações selecionadas. O número de cigarros não encerra a avaliação.</p>
<h3>Reposição de nicotina: lenta e pontual</h3><div class="cmp"><div class="r h"><div class="k">Comparação</div><div class="c">Adesivo</div><div class="c">Goma</div></div>
<div class="r"><div class="k">Perfil</div><div class="c">Liberação lenta ao longo do dia.</div><div class="c">Uso pontual para a fissura, com ação mais rápida que o adesivo.</div></div>
<div class="r"><div class="k">Apresentações</div><div class="c">7 mg, 14 mg e 21 mg.</div><div class="c">2 mg por unidade.</div></div>
<div class="r"><div class="k">Cuidado</div><div class="c">Troca diária, alternando os locais; observar reação na pele.</div><div class="c">Mastigar de forma intermitente e manter no canto da boca.</div></div></div>
<p>Adesivo e goma são as formas de reposição usadas como referência neste material. Pastilhas e spray nasal são outras apresentações mencionadas na prática do tratamento; a disponibilidade precisa ser confirmada para cada produto e local.</p>
<h3>Adesivo: o exemplo de quem fuma um maço por dia</h3><p>Para alguém que fuma 20 cigarros por dia, um exemplo de esquema é começar com 21 mg e reduzir a dose mês a mês, durante três meses. A lógica é repor nicotina enquanto a pessoa deixa de fumar e trabalha os componentes psicológicos e comportamentais.</p>
<p>A orientação do Dr. Cássio é aplicar o adesivo da cintura para cima, com troca diária e rodízio entre locais, considerando a absorção. Se aparecer vermelhidão, é preciso mudar de local; em caso de reação intensa ou persistente, a goma pode ser considerada como alternativa.</p>'''+fig('adesivos','Exemplo de redução progressiva dos adesivos de nicotina','Exemplo para quem fuma 20 cigarros/dia; a escolha e os ajustes dependem da avaliação individual.')+'''
<div class="reg"><b>Comparação usada no exemplo.</b> O Dr. Cássio utiliza 0,8–1 mg de nicotina por cigarro para explicar a reposição.</div>'''+note('A quantidade total de nicotina de um produto e a quantidade absorvida não são intercambiáveis; comparações entre cigarro, goma, adesivo e líquido exigem considerar a via e o padrão de uso.','2')+'''
<h3>Goma: alívio da fissura</h3><p>A goma de 2 mg permite uso pontual para a fissura. Entre os exemplos clínicos estão quem ainda fuma 1 ou 2 cigarros por dia e quem está há 5–7 dias sem fumar, mas apresenta vontade intensa. Nessa segunda situação, o Dr. Cássio prefere avaliar a goma antes de iniciar um adesivo, atento ao risco de náusea, tontura e mal-estar.</p>
<ol class="flow"><li><b class="t">Mastigar de forma intermitente.</b> A explicação alterna a mastigação com pausas.</li><li><b class="t">Manter junto à bochecha.</b> A goma fica no canto da boca entre os períodos de mastigação.</li><li><b class="t">Reavaliar a necessidade.</b> O uso deve fazer sentido diante da fissura, sem se tornar um gesto automático depois que ela passou.</li></ol>
<p>Na experiência clínica do Dr. Cássio, o alívio da fissura pode ocorrer em cerca de 5 minutos, e alguns pacientes utilizam 3–5 gomas por dia. A comparação informal de uma goma de 2 mg com dois cigarros ajuda a explicar o uso, mas não estabelece uma equivalência exata de absorção.</p>'''+note('A técnica de mastigar e manter junto à bochecha dura cerca de 30 minutos. O tempo até aliviar a fissura é diferente da duração do uso; 3–5 unidades/dia não definem uma dose máxima universal.','5')+'''
<p>Um caso ilustra a revisão do tratamento: um médico continuava usando goma seis meses depois de parar, sem sentir vontade de fumar. Ao conversar sobre a necessidade real, percebeu que podia interromper esse uso. O ponto didático é reavaliar, não presumir a necessidade indefinida de reposição.</p>
<h3>Bupropiona: perfil clínico e risco de convulsão</h3><p>A bupropiona é um antidepressivo atípico com eficácia para cessação independente do efeito antidepressivo. Atua em vias dopaminérgicas e noradrenérgicas relacionadas à dependência e integra as opções de primeira linha indicadas pela Organização Mundial da Saúde.</p>
<p><b>História de crise convulsiva e traumatismo cranioencefálico são contraindicações</b> destacadas pelo Dr. Cássio. Antes de prescrever, revise também interações que aumentem o risco de convulsão, o perfil clínico e as medicações em uso.</p>
<div class="ref"><div class="txt"><div class="kick">Apresentação de liberação lenta</div><p>Liberação ao longo do dia. A escolha da formulação depende do esquema de tratamento prescrito.</p></div><div class="val">300 mg<small>bupropiona</small></div></div>'''+note('A apresentação de 300 mg não define a dose inicial. Formulação, titulação e intervalos precisam seguir a bula e o protocolo da apresentação prescrita.','6')+'''
<p>Entre os nomes comerciais estão Zyban, Zetron, Wellbutrin e Bup. Ao selecionar o paciente, pergunte como ele ficou nas tentativas anteriores: irritabilidade e agitação merecem atenção, enquanto o relato de humor rebaixado leva a outra avaliação.</p>
<div class="box orange"><div class="kick">Aprendizado da prática · observar a tolerância</div><p>O Dr. Cássio teve uma experiência pessoal de agitação com a bupropiona. Seu aprendizado é considerar o perfil do paciente e observar a resposta, sem presumir que todos terão a mesma reação: a maioria de seus pacientes tolera bem o medicamento.</p></div>
<h3>Ansiedade: tratar a pessoa, não só o cigarro</h3><p>A sertralina não é um medicamento específico para cessação. Diante de ansiedade, depressão ou transtorno de déficit de atenção e hiperatividade, avalie a condição associada e considere o contato com o profissional que já acompanha a pessoa. Um clínico com competência para esse manejo pode avaliar e tratar a comorbidade; reconhecer quando buscar apoio especializado faz parte do cuidado.</p>'''+quote('Eu é que não passo porque não é mais da minha área.')+box('Pegadinha do professor','<p>Usar bupropiona automaticamente em qualquer pessoa ansiosa. Ela pode causar agitação; a escolha depende do perfil clínico e da revisão de riscos.</p>','red')+'''
<h3>Vareniclina: agonismo parcial</h3><p>A vareniclina, lembrada pelo nome Champix, foi desenvolvida especificamente para a cessação. Liga-se ao receptor nicotínico alfa-4 beta-2 como <b>agonista parcial</b>: produz ativação parcial e reduz a ação reforçadora da nicotina quando a pessoa fuma.</p>
<p>A ideia é oferecer parte do estímulo e, ao mesmo tempo, reduzir a recompensa obtida ao fumar. A expressão “30%–40% do prazer”, usada pelo Dr. Cássio, é uma analogia para o agonismo parcial; não representa eficácia clínica ou ocupação dos receptores.</p>
<div class="reg"><b>Disponibilidade.</b> Antes de considerar a prescrição, confirme a situação comercial da apresentação. A experiência do Dr. Cássio inclui um período de indisponibilidade da vareniclina no mercado brasileiro.</div>
<p>Como comparação ilustrativa, o Dr. Cássio apresenta valores aproximados de cessação de 17% com placebo, 30% com bupropiona e 47% com vareniclina. Em seu grupo, relata 90% de sucesso associando vareniclina e apoio comportamental.</p>
<div class="reg"><b>Como interpretar os resultados.</b> Os 90% representam a experiência de um grupo conduzido pelo Dr. Cássio. Não constituem uma taxa garantida nem devem ser comparados diretamente com percentuais de outros grupos.</div>'''+quote('Eu paro de fumar; o que o remédio vai me ajudar? A não ter as crises de abstinência.')

b5='''<h3>Recaída é informação para ajustar o plano</h3><p>Se a pessoa volta a fumar, o primeiro passo é entender o que aconteceu. Pergunte sobre fissura, álcool, estresse, festas e outros acontecimentos. Avalie quantos cigarros fumou e se voltou ao padrão anterior ou a uma quantidade menor.</p>
<ol class="flow"><li><b class="t">Reconstruir o contexto.</b> O que aconteceu antes de voltar a fumar?</li><li><b class="t">Identificar o gatilho.</b> Qual situação ou dificuldade ficou sem resposta no plano?</li><li><b class="t">Combinar uma nova tentativa.</b> Ajustar a estratégia e retomar o acompanhamento.</li></ol>'''+quote('Recaída não é o fim do tratamento.')+'''
<h3>Parar vale a pena em qualquer idade</h3><p>A função pulmonar diminui ao longo dos anos, mas o tabagismo acelera a perda. O Dr. Cássio utiliza a ideia de uma perda “três vezes maior” para destacar esse efeito. Ao cessar, a velocidade de perda volta a se aproximar da de quem não fuma; o que já se perdeu não é automaticamente recuperado.</p>
<p>Quanto mais cedo a pessoa para, maior o benefício acumulado. A redução de riscos cardiovasculares, respiratórios e oncológicos é progressiva. Na experiência de consultório do Dr. Cássio, a melhora da aparência pode ser percebida em cerca de 15 dias, embora esse prazo varie entre pessoas.</p>
<p>Em uma pessoa de 85 anos com doença pulmonar obstrutiva crônica, irritação brônquica, secreção e infecções de repetição precisam ser consideradas junto do conforto e dos objetivos de cuidado. A decisão exige ponderação compartilhada; a idade isolada não define quando parar deixa de valer a pena.</p>'''+fig('funcao-pulmonar','Curvas qualitativas de perda da função pulmonar com continuidade do tabagismo e após cessação','Esquema qualitativo: cessar modifica a trajetória de perda, sem recuperar automaticamente a função anterior.')+'''
<h3>A família e o tempo de acompanhamento</h3><p>A cessação beneficia também quem estava exposto à fumaça. Avisar a família ajuda a construir apoio durante a mudança: a irritabilidade não deve virar motivo para estimular o retorno ao cigarro.</p>
<p>Uma estimativa usada pelo Dr. Cássio é de 30% de recaída até nove meses. Sua orientação é acompanhar por <b>9 meses a 1 ano</b>, buscando cessação sustentada, com prevenção e manejo de recaídas.</p>'''+box('Pegadinha do professor','<p>Achar que parar apaga toda a perda pulmonar ou que a recaída representa fracasso moral. O benefício está em mudar a trajetória; o acompanhamento deve responder às dificuldades que surgem.</p>','red')+'''<div class="reg"><b>Seguimento individualizado.</b> O período de acompanhamento não significa que o risco de voltar a fumar desapareça depois de um ano. O plano deve acompanhar as necessidades da pessoa.</div>'''

b6='''<h3>O produto mudou; a dependência continua</h3><p>Vape, pod e cigarro eletrônico são formatos de dispositivos eletrônicos para fumar. Entre seus componentes estão bateria, sensor, reservatório e atomizador. A energia gera um aerossol a partir do produto utilizado; não se trata apenas de vapor de água.</p>
<p>Há apresentações com ou sem nicotina, sais de nicotina, refis aromatizados e produtos de tabaco aquecido. Design discreto, tecnologia, sabores, facilidade de uso, curiosidade e socialização ajudam a explicar o apelo entre jovens.</p>
<h3>Por que o sal de nicotina importa?</h3><p>Ele permite formulações com concentrações elevadas e menor aspereza na boca e na garganta. Isso pode facilitar tragadas repetidas e mais profundas em alguns dispositivos. A sensação de menor irritação não significa menor risco.</p>
<p>A quantidade de nicotina e o padrão de exposição variam entre marcas, dispositivos e formas de uso. Na consulta, peça a caixa do produto, confira a concentração e o volume e pergunte quanto tempo o refil dura.</p>
<h3>Como calcular o conteúdo de nicotina</h3><p>Na convenção usada no exemplo, multiplica-se a porcentagem por 10 para obter a concentração em mg/mL. Depois, multiplica-se pelo volume e divide-se pelos dias de duração:</p>
<div class="formula">[(porcentagem × 10) × volume em mL] ÷ dias</div>'''+fig('conta-pod','Cálculo com 5%, 10mL e duração de 10 dias')+'''
<p>O exemplo considera um refil de 10 mL a 5% que dura 10 dias. São 50 mg/mL, 500 mg no refil inteiro e 50 mg por dia no líquido consumido. O Dr. Cássio utiliza uma comparação aproximada com 2,5 maços por dia para tornar o consumo perceptível ao paciente.</p>'''+note('A conversão assume porcentagem massa/volume: confira a convenção do rótulo. A conta estima nicotina no líquido consumido, não a dose absorvida. A passagem para o aerossol e a absorção variam; a comparação com 2,5 maços é uma analogia, não uma equivalência clínica validada.','2')+'''
<div class="box orange"><div class="kick">Aprendizado da prática · tornar o consumo visível</div><p>Em consultas, o Dr. Cássio chegou a comparações com 3,5 e 7 maços ao discutir o consumo de pacientes. Entender a dimensão do uso ajudou algumas pessoas a decidir parar. A utilidade da conta é abrir essa conversa, sem reduzir todos os dispositivos à mesma equivalência.</p></div>'''+box('Pegadinha do professor','<p>Usar uma equivalência fixa sem conhecer concentração, volume e duração. Marcas, dispositivos e padrões de uso variam.</p>','red')+'''
<h3>Aerossol e regras no Brasil</h3><p>O aerossol pode conter partículas irritantes, aromatizantes e metais, com efeitos respiratórios e cardiovasculares. Os efeitos de longo prazo continuam sendo estudados.</p>
<p>No Brasil, são proibidas fabricação, importação, comercialização, distribuição, armazenamento, transporte e propaganda desses dispositivos. O uso em ambientes coletivos fechados, incluindo avião e ônibus, também é proibido.</p>'''+note('A Agência Nacional de Vigilância Sanitária mantém as proibições na resolução de 2024. A norma não proíbe, por si só, o uso individual, mas proíbe o uso em recinto coletivo fechado.','3')

b7='''<h3>Lesão pulmonar associada ao uso de cigarro eletrônico</h3><p>Produtos inalados podem causar <b>dano pulmonar agudo grave</b>. Casos de jovens com opacidades intersticiais e alveolares extensas ilustram a importância de investigar a exposição a cigarros eletrônicos.</p>
<p>O dano pode envolver a membrana alvéolo-capilar. A lesão pulmonar associada ao uso desses produtos demonstra o risco agudo, mas não resume todos os efeitos possíveis dos dispositivos.</p>'''+note('“Pulmão em pipoca” é o nome popular da bronquiolite obliterante; não é sinônimo da lesão pulmonar associada ao uso de cigarro eletrônico.','4')+'''
<h3>O argumento de que “na Inglaterra é liberado”</h3><p>Em uma consulta, um paciente do Dr. Cássio usou a experiência inglesa como argumento de segurança. O aprendizado é distinguir regulamentação, redução de danos e ausência de risco: são questões diferentes.</p>
<div class="cmp"><div class="r h"><div class="k">Distinção</div><div class="c">Redução de danos</div><div class="c">Uso genérico de pod</div></div>
<div class="r"><div class="k">Contexto</div><div class="c">Pessoa que ainda mantém cigarros convencionais após tentativas de redução.</div><div class="c">Uso que não corresponde àquele plano específico de redução.</div></div>
<div class="r"><div class="k">Estratégia</div><div class="c">Concentração e horários definidos para uma situação delimitada.</div><div class="c">Produtos e padrões de consumo variáveis entre usuários e dispositivos.</div></div>
<div class="r"><div class="k">Conclusão</div><div class="c">Uma estratégia precisa ser entendida no contexto em que foi estudada.</div><div class="c">Não permite concluir que qualquer vape seja seguro ou um medicamento aprovado.</div></div></div>'''+box('Pegadinha do professor','<p>Concluir que a liberação em outro país prova que não faz mal. Priorize tratamentos com eficácia e segurança estabelecidas; nenhum cigarro eletrônico é aprovado no Brasil para tratar tabagismo.</p>','red')+note('A ausência de aprovação de cigarros eletrônicos para tratamento do tabagismo no Brasil é confirmada pela Agência Nacional de Vigilância Sanitária.','4')

b8='''<h3>Estratégias antigas em novos produtos</h3><p>A publicidade antiga do cigarro e o apelo atual dos dispositivos compartilham elementos: glamour, status, socialização, design, tecnologia, sabores e baixa percepção de risco. O produto fica discreto e atraente, enquanto a dependência continua no centro do problema.</p>
<h3>Três frentes de controle</h3><ol class="flow"><li><b class="t">Prevenir o início.</b> Proteger crianças e adolescentes da iniciação ao tabagismo.</li><li><b class="t">Proteger da exposição passiva.</b> Reduzir a exposição de familiares e de outras pessoas à fumaça.</li><li><b class="t">Oferecer cuidado.</b> Apoiar quem deseja parar, inclusive com grupos e acompanhamento.</li></ol>
<p>Para destacar o valor da ajuda, o Dr. Cássio utiliza uma comparação de 85% de pessoas que desejavam parar, 3% que conseguiam sozinhas e 60% com apoio. Esses percentuais ilustram seu argumento sobre a importância do cuidado; não representam uma promessa individual de resultado.</p>
<h3>A decisão precisa fazer sentido para a pessoa</h3><p>Na medicina centrada na pessoa, a mudança de hábito será feita por quem vive aquela rotina. O plano precisa de concordância, escuta e participação.</p>'''+rows([('Abordar','Todo usuário merece uma conversa, mesmo sem estar pronto para parar hoje. A oferta de ajuda mantém aberta a possibilidade de mudança.'),('Escutar','O cuidado envolve compreender o que a pessoa sente, como vive e o que a faz fumar. Sem tempo e paciência para escutar, parte do problema fica sem resposta.'),('Combinar','Apoio comportamental e farmacoterapia, quando indicada, entram em um plano compartilhado. O profissional ajuda a construir a mudança, em vez de apenas impor uma lista de ordens.')])+quote('É mudança de hábito de vida, e quem vai fazer é a pessoa, não é você; então ela precisa estar de acordo com aquilo que vai fazer.')

resumo=[
('Dependência','Física, psicológica e comportamental. A nicotina é central, mas a rotina também precisa mudar.'),
('Avaliação','Perguntar, aconselhar, avaliar, ajudar e acompanhar. Faixas iniciais de Fagerström: 0–2 muito baixa; 3–4 baixa; 5 média. Sempre junto da história clínica.'),
('Apoio comportamental <span class="prova">PROVA</span>','Expressão orientada pelo Dr. Cássio para a prova. Combinar Dia D entre 7 e 30 dias; reconhecer gatilhos, preparar a mudança e reorganizar a rotina.'),
('Farmacoterapia','Abstinência relevante; >5 cigarros/dia; primeiro cigarro <1 hora; Fagerström >4. Individualizar. Na prática do Dr. Cássio, medicação apenas para adultos.'),
('Reposição de nicotina','Exemplo: adesivo 21 mg, 14 mg e 7 mg, um mês em cada etapa, troca diária. Goma citada: 2 mg para situações de fissura. Não equivaler diretamente produtos.'),
('Outros medicamentos','Bupropiona: história de convulsão e traumatismo craniano são contraindicações; revisar interações e agitação. A apresentação de 300 mg não define o início. Vareniclina: agonista parcial alfa-4 beta-2.'),
('Seguimento','Recaída pede identificação de gatilhos e novo plano. Acompanhamento descrito: 9 meses a 1 ano. Parar reduz a velocidade de perda pulmonar; não apaga a perda anterior.'),
('Conta do pod','5% = 50 mg/mL; refil de 10 mL = 500 mg; duração de 10 dias = 50 mg/dia no líquido. A conta não determina dose absorvida nem equivalência exata com maços.'),
('Riscos e prevenção','Aerossol não é vapor de água. Pode haver lesão pulmonar aguda grave. O dispositivo não é tratamento aprovado no Brasil. Prevenir o início, proteger da exposição passiva e apoiar a cessação.')]
vespera='<section id="s09" class="vesp">'+cab(9,'Página de véspera')+'<p class="small">Revise na ordem da trilha: entender a dependência, planejar a cessação e acompanhar o cuidado. O selo PROVA destaca a orientação do professor.</p>'+''.join(f'<div class="item"><p><b>{k}.</b> {v}</p></div>' for k,v in resumo)+'<p class="small">Doses e critérios precisam ser interpretados junto da avaliação individual. Consulte os capítulos para as diferenças entre apresentações e as referências complementares.</p></section>'

gloss=[('Abstinência','Sintomas que aparecem após interromper ou reduzir o uso de uma substância à qual havia dependência.'),('Agonista parcial','Substância que ativa um receptor, mas produz resposta menor que a de um agonista pleno.'),('Alfa-4 beta-2','Tipo de receptor nicotínico envolvido na dependência e na ação da vareniclina.'),('Ambivalência','Ter, ao mesmo tempo, razões para mudar e razões para manter o comportamento.'),('Atomizador','Parte do dispositivo que participa da formação do aerossol a partir do produto utilizado.'),('Fissura','Vontade intensa de usar a substância, como a vontade intensa de fumar.'),('Gatilho','Situação, emoção ou hábito que desperta a vontade de fumar.'),('Membrana alvéolo-capilar','Barreira fina entre o ar dos alvéolos e o sangue dos capilares, onde ocorrem as trocas gasosas.'),('Noradrenérgico','Relacionado à noradrenalina, uma substância que participa da comunicação entre células do sistema nervoso.')]
glossario='<section id="s10" class="glossario">'+cab(10,'Palavras da aula em linguagem simples')+''.join(rows(gloss[i:i+3],'terms') for i in range(0,len(gloss),3))
glossario+='''<h3 id="fontes">Referências complementares</h3><p class="small">Leituras de apoio aos esclarecimentos clínicos destacados em roxo.</p><ol class="source-list">
<li>Ministério da Saúde. <a href="https://linhasdecuidado.saude.gov.br/portal/tabagismo/atencao-especializada/planejamento-terapeutico/">Linha de cuidado do tabagismo — planejamento terapêutico.</a></li>
<li>Blank e colaboradores, 2020. <a href="https://stacks.cdc.gov/view/cdc/105007">Estudo de entrega de nicotina: concentração, duração da tragada e exposição. Repositório dos Centros de Controle e Prevenção de Doenças dos Estados Unidos.</a></li>
<li>Agência Nacional de Vigilância Sanitária. <a href="https://www.gov.br/anvisa/pt-br/assuntos/tabaco/cigarro-eletronico">Cigarro eletrônico — regulamentação e informações oficiais.</a></li>
<li>Agência Nacional de Vigilância Sanitária. <a href="https://www.gov.br/anvisa/pt-br/acessoainformacao/perguntasfrequentes/tabaco/cigarro-eletronico-2">Perguntas frequentes — tratamento e riscos, itens 2 e 4.</a></li>
<li>Centros de Controle e Prevenção de Doenças dos Estados Unidos. <a href="https://www.cdc.gov/tobacco/campaign/tips/quit-smoking/quit-smoking-medications/how-to-use-quit-smoking-medicines/how-to-use-nicotine-gum.html">Orientações para uso da goma de nicotina.</a></li>
<li>DailyMed, Biblioteca Nacional de Medicina dos Estados Unidos. <a href="https://www.dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=8069c521-c49a-4b6d-baa8-4b0be897d585">Bula de bupropiona de liberação sustentada para cessação.</a></li></ol>{{NOTAS}}</section>'''

# Aproximar os alertas do raciocínio que ilustram, antes da figura alta.
alerta_perda=box('Pegadinha do professor','<p>Achar que parar apaga toda a perda pulmonar ou que a recaída representa fracasso moral. O benefício está em mudar a trajetória; o acompanhamento deve responder às dificuldades que surgem.</p>','red')
seguimento='<div class="reg"><b>Seguimento individualizado.</b> O período de acompanhamento não significa que o risco de voltar a fumar desapareça depois de um ano. O plano deve acompanhar as necessidades da pessoa.</div>'
b5=b5.replace(alerta_perda,'').replace(seguimento,'').replace('<h3>Parar vale a pena em qualquer idade</h3>',alerta_perda+seguimento+'<h3>Parar vale a pena em qualquer idade</h3>')
bodies=[b1,b2,b3,b4,b5,b6,b7,b8]
(ROOT/'apostila.html').write_text(head+cover+legend+professor+recados+''.join(section(n,b) for n,b in enumerate(bodies,1))+vespera+glossario+'</body></html>',encoding='utf-8')
print('HTML gerado: apostila.html')
