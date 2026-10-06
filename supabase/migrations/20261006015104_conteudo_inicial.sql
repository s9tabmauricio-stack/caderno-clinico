-- Conteúdo inicial (o mesmo do protótipo)
insert into public.materias (id, nome, descricao, ordem, cor_inicio, cor_fim) values
  ('nefro', 'Nefrologia', 'Lesão renal aguda e distúrbios do potássio.', 1, '#0B5BD3', '#3B4FC9'),
  ('uro', 'Urologia', 'Infecção do trato urinário e litíase urinária.', 2, '#4A3FC0', '#7E36A8');

insert into public.aulas (id, materia_id, ordem, titulo, resumo, apostila_html) values
  ('lra', 'nefro', 1, 'Lesão renal aguda', 'Definição, os três mecanismos e quando dialisar.',
$apostila$<h3>O que é</h3>
<p>Queda rápida da função dos rins, em horas a dias. O diagnóstico usa a creatinina e a diurese; basta um dos critérios abaixo.</p>
<ul>
<li><b>Creatinina:</b> aumento de 0,3 mg/dL ou mais em até 48 horas.</li>
<li><b>Creatinina:</b> valor 1,5 vez ou mais o de base, nos últimos 7 dias.</li>
<li><b>Diurese:</b> menos de 0,5 mL/kg por hora durante 6 horas.</li>
</ul>
<div class="ref"><div class="txt"><div class="kick"><span class="dot"></span>Critério de diurese</div><p>Vale para quem tem a diurese medida, com sonda ou coleta controlada.</p></div><div class="val">&lt; 0,5 mL/kg/h<small>por 6 horas</small></div></div>
<h3>Três mecanismos</h3>
<div class="grid">
<div class="card"><span class="tag">Pré-renal</span><h4>Falta fluxo</h4><p>Desidratação, hemorragia, insuficiência cardíaca. O rim está íntegro e segura sódio e água.</p></div>
<div class="card"><span class="tag">Renal</span><h4>Lesão do próprio rim</h4><p>A mais comum é a necrose tubular aguda, por isquemia prolongada ou por drogas tóxicas, como aminoglicosídeos e contraste iodado.</p></div>
<div class="card"><span class="tag">Pós-renal</span><h4>Obstrução da saída</h4><p>Hiperplasia da próstata, cálculos, tumores pélvicos. O ultrassom mostra hidronefrose.</p></div>
</div>
<h3>Pré-renal ou necrose tubular aguda?</h3>
<div class="cmp-wrap"><table class="cmp"><thead><tr><th></th><th>Pré-renal</th><th>Necrose tubular aguda</th></tr></thead><tbody>
<tr><td>Sódio urinário</td><td>&lt; 20 mEq/L</td><td>&gt; 40 mEq/L</td></tr>
<tr><td>Fração de excreção de sódio</td><td>&lt; 1%</td><td>&gt; 2%</td></tr>
<tr><td>Osmolalidade urinária</td><td>&gt; 500 mOsm/kg</td><td>&lt; 350 mOsm/kg</td></tr>
<tr><td>Sedimento</td><td>Sem alterações ou cilindros hialinos</td><td>Cilindros granulosos castanho-escuros</td></tr>
</tbody></table></div>
<div class="box red"><div class="kick"><span class="dot"></span>Armadilha</div><p>Diurético nas últimas 24 horas aumenta a fração de excreção de sódio e engana. Use a fração de excreção de ureia: abaixo de 35% sugere pré-renal.</p></div>
<h3>Quando dialisar com urgência</h3>
<p>Quando a complicação não responde ao tratamento clínico. Um valor isolado de creatinina não indica diálise.</p>
<ul>
<li><b>Acidose metabólica</b> grave e refratária.</li>
<li><b>Hipercalemia</b> refratária ao tratamento clínico.</li>
<li><b>Hipervolemia</b> refratária, como edema agudo de pulmão sem resposta a diurético.</li>
<li><b>Uremia</b> com complicação: pericardite, encefalopatia ou sangramento.</li>
<li><b>Intoxicação</b> por substância dialisável: lítio, metanol, etilenoglicol, salicilatos.</li>
</ul>$apostila$);

insert into public.aulas (id, materia_id, ordem, titulo, resumo, apostila_html) values
  ('potassio', 'nefro', 2, 'Distúrbios do potássio', 'Hipercalemia, hipocalemia e o eletrocardiograma de cada uma.',
$apostila$<div class="ref"><div class="txt"><div class="kick"><span class="dot"></span>Potássio sérico</div><p>Faixa normal no adulto.</p></div><div class="val">3,5 a 5,0<small>mEq/L</small></div></div>
<h3>Hipercalemia</h3>
<p>Potássio acima de 5,0 mEq/L. Um valor alto e inesperado em paciente estável pode ser hemólise da amostra; com alteração no eletrocardiograma, trate primeiro e confirme depois.</p>
<p>Causas frequentes: lesão renal, drogas que retêm potássio (inibidores da enzima conversora de angiotensina, bloqueadores do receptor de angiotensina, espironolactona), acidose e rabdomiólise.</p>
<p class="label">O eletrocardiograma piora nesta ordem</p>
<ol class="flow">
<li><b>Onda T apiculada,</b> alta e estreita.</li>
<li><b>Onda P achatada</b> até desaparecer, com intervalo PR longo.</li>
<li><b>QRS alargado.</b></li>
<li><b>Padrão sinusoidal,</b> que antecede fibrilação ventricular ou assistolia.</li>
</ol>
<h3>Tratamento em três tempos</h3>
<div class="grid">
<div class="card"><span class="tag">1 · Proteger o coração</span><p>Gluconato de cálcio 10%, intravenoso em 2 a 3 minutos. Age em minutos e não baixa o potássio.</p></div>
<div class="card"><span class="tag">2 · Levar para a célula</span><p>Insulina regular com glicose e salbutamol inalatório; bicarbonato se houver acidose.</p></div>
<div class="card"><span class="tag">3 · Retirar do corpo</span><p>Diurético de alça, resina de troca (poliestirenossulfonato de cálcio) ou diálise.</p></div>
</div>
<div class="ref"><div class="txt"><div class="kick"><span class="dot"></span>Doses do primeiro atendimento</div><p>A glicose vai junto com a insulina para evitar hipoglicemia, a não ser que o paciente já esteja hiperglicêmico.</p></div><div class="vals"><div class="val"><small>Gluconato de cálcio 10%</small>10 mL</div><div class="val"><small>Insulina regular</small>10 unidades</div></div></div>
<h3>Hipocalemia</h3>
<p>Potássio abaixo de 3,5 mEq/L. Causas comuns: diuréticos, vômitos, diarreia e uso de insulina. No eletrocardiograma: onda T achatada, onda U proeminente e infradesnivelamento do segmento ST.</p>
<p>Prefira a reposição oral quando possível. Em veia periférica, a reposição costuma ficar em torno de 10 mEq por hora, sempre diluída e nunca em bolus.</p>
<div class="box red"><div class="kick"><span class="dot"></span>Erro comum</div><p>Repor potássio sem olhar o magnésio. Com hipomagnesemia, o rim continua perdendo potássio e a reposição não funciona.</p></div>$apostila$);

insert into public.aulas (id, materia_id, ordem, titulo, resumo, apostila_html) values
  ('itu', 'uro', 1, 'Infecção do trato urinário', 'Cistite, pielonefrite e a bacteriúria que não se trata.',
$apostila$<h3>Quem causa</h3>
<p><b>Escherichia coli</b> responde pela grande maioria das cistites adquiridas na comunidade. Outros agentes: Staphylococcus saprophyticus em mulheres jovens, Klebsiella e Proteus.</p>
<h3>Cistite ou pielonefrite?</h3>
<div class="cmp-wrap"><table class="cmp"><thead><tr><th></th><th>Cistite</th><th>Pielonefrite</th></tr></thead><tbody>
<tr><td>Quadro</td><td>Disúria, polaciúria, urgência, dor suprapúbica; sem febre</td><td>Febre, calafrios, dor lombar, sinal de Giordano positivo, náuseas</td></tr>
<tr><td>Urocultura</td><td>Dispensável na cistite não complicada da mulher</td><td>Sempre, colhida antes do antibiótico</td></tr>
<tr><td>Tratamento</td><td>Oral e curto</td><td>7 a 14 dias; internar se houver vômitos, sepse ou gestação</td></tr>
</tbody></table></div>
<div class="ref"><div class="txt"><div class="kick"><span class="dot"></span>Cistite não complicada na mulher</div><p>Primeira linha.</p></div><div class="vals"><div class="val"><small>Nitrofurantoína, 6 em 6 horas</small>100 mg por 5 a 7 dias</div><div class="val"><small>Fosfomicina</small>3 g dose única</div></div></div>
<div class="box red"><div class="kick"><span class="dot"></span>Erro comum</div><p>Tratar bacteriúria assintomática. Urocultura positiva sem sintomas só se trata em gestantes e antes de procedimento urológico com sangramento de mucosa. Idosos, diabéticos e pacientes com sonda não entram nessa lista.</p></div>
<h3>Pielonefrite que não melhora</h3>
<p>Febre que persiste após 48 a 72 horas de antibiótico adequado pede exame de imagem para procurar obstrução ou abscesso. Obstrução com infecção precisa ser desobstruída.</p>$apostila$);

insert into public.aulas (id, materia_id, ordem, titulo, resumo, apostila_html) values
  ('litiase', 'uro', 2, 'Litíase urinária', 'Tipos de cálculo, cólica renal e a urgência que não espera.',
$apostila$<h3>Do que são feitos</h3>
<div class="grid">
<div class="card"><span class="tag">Mais comum</span><h4>Oxalato de cálcio</h4><p>Cerca de 70 a 80% dos cálculos. Aparece na radiografia simples.</p></div>
<div class="card"><span class="tag">Radiotransparente</span><h4>Ácido úrico</h4><p>Não aparece na radiografia simples, mas aparece na tomografia. Ligado a gota e urina ácida.</p></div>
<div class="card"><span class="tag">Infecção</span><h4>Estruvita</h4><p>Fosfato de amônio e magnésio, formado por bactérias produtoras de urease, como Proteus. Pode virar cálculo coraliforme.</p></div>
<div class="card"><span class="tag">Rara</span><h4>Cistina</h4><p>Doença genética. Aparece em pessoas jovens e recidiva muito.</p></div>
</div>
<h3>Cólica renal</h3>
<p>Dor lombar intensa, em cólica, que irradia para o flanco, a região inguinal e a genitália. O paciente fica inquieto, sem posição de alívio. Hematúria microscópica é comum.</p>
<ul>
<li><b>Exame de escolha:</b> tomografia computadorizada sem contraste. Em gestantes, ultrassom.</li>
<li><b>Dor:</b> anti-inflamatório não esteroide é a primeira escolha, se não houver contraindicação.</li>
<li><b>Cálculos de até 5 mm</b> costumam ser eliminados sozinhos.</li>
<li><b>Terapia expulsiva:</b> tansulosina, um alfa-bloqueador, ajuda cálculos de 5 a 10 mm no ureter distal.</li>
</ul>
<div class="box red"><div class="kick"><span class="dot"></span>Urgência urológica</div><p>Cálculo obstrutivo com febre é infecção em via urinária fechada. Desobstruir logo, com cateter duplo J ou nefrostomia, e começar antibiótico. A retirada do cálculo fica para depois.</p></div>
<h3>Prevenção</h3>
<div class="ref"><div class="txt"><div class="kick"><span class="dot"></span>Meta de hidratação</div><p>Beber água o bastante para urinar acima disso.</p></div><div class="val">&gt; 2,5 L<small>de urina por dia</small></div></div>
<p>Reduzir sal e proteína animal. Não restringir o cálcio da dieta: com menos cálcio no intestino, mais oxalato é absorvido e o risco de cálculo aumenta.</p>$apostila$);

insert into public.questoes (id, aula_id, ordem, enunciado, alternativas, correta, comentario) values
  ('lra-1', 'lra', 1, 'Homem de 68 anos, internado por pneumonia, tinha creatinina de 1,0 mg/dL na admissão. Trinta e seis horas depois, a creatinina é 1,4 mg/dL e a diurese continua normal. Qual a interpretação correta?',
   '["Não há lesão renal aguda, porque o aumento foi menor que 50%.","Há lesão renal aguda: a creatinina subiu 0,3 mg/dL ou mais em menos de 48 horas.","Só é possível firmar o diagnóstico se a diurese cair.","O quadro indica doença renal crônica."]'::jsonb, 1,
   'Basta um critério. O aumento de 0,4 mg/dL em 36 horas cumpre o critério de 0,3 mg/dL em 48 horas, mesmo com diurese preservada. Diurese normal não afasta lesão renal aguda.'),
  ('lra-2', 'lra', 2, 'Mulher de 75 anos com vômitos há três dias chega com pressão de 90 x 60 mmHg. Exames: ureia 120 mg/dL, creatinina 2,4 mg/dL, sódio urinário 12 mEq/L e fração de excreção de sódio de 0,4%. Qual o mecanismo mais provável?',
   '["Pré-renal, por hipovolemia.","Necrose tubular aguda.","Nefrite intersticial aguda.","Pós-renal."]'::jsonb, 0,
   'Sódio urinário baixo e fração de excreção de sódio abaixo de 1% mostram um rim íntegro, economizando sódio. A relação ureia/creatinina de 50 reforça o quadro pré-renal. A conduta é repor volume.'),
  ('lra-3', 'lra', 3, 'Homem de 74 anos com jato urinário fraco há anos está há dois dias sem urinar, com dor suprapúbica. A bexiga é palpável e a creatinina é 3,1 mg/dL. Qual a primeira conduta?',
   '["Hidratação venosa vigorosa.","Sondagem vesical de demora.","Hemodiálise de urgência.","Biópsia renal."]'::jsonb, 1,
   'É lesão pós-renal por retenção urinária, provavelmente por hiperplasia da próstata. Desobstruir é o tratamento. Depois da sondagem, vigiar a diurese pós-obstrutiva.'),
  ('lra-4', 'lra', 4, 'Qual das situações abaixo NÃO é indicação de diálise de urgência?',
   '["Potássio de 7,2 mEq/L sem resposta ao tratamento clínico.","Edema agudo de pulmão sem resposta a diurético.","Pericardite urêmica.","Creatinina de 4,0 mg/dL em paciente estável e sem sintomas."]'::jsonb, 3,
   'A diálise de urgência é indicada por complicações refratárias, não por um número de creatinina. Paciente estável, sem acidose, hipercalemia, hipervolemia ou uremia sintomática, não precisa de diálise agora.'),
  ('k-1', 'potassio', 1, 'Paciente renal crônico chega com fraqueza. O potássio é 7,0 mEq/L e o eletrocardiograma mostra ondas T apiculadas e QRS alargado. Qual a primeira medida?',
   '["Gluconato de cálcio intravenoso.","Resina de troca por via oral.","Furosemida intravenosa.","Repetir o exame para afastar hemólise antes de tratar."]'::jsonb, 0,
   'Com alteração no eletrocardiograma, a prioridade é proteger o miocárdio, e o cálcio age em minutos. Em seguida vêm as medidas que levam o potássio para a célula e as que o retiram do corpo.'),
  ('k-2', 'potassio', 2, 'Qual destas medidas NÃO reduz o potássio sérico?',
   '["Insulina regular com glicose.","Salbutamol inalatório.","Gluconato de cálcio.","Hemodiálise."]'::jsonb, 2,
   'O cálcio só estabiliza a membrana do miocárdio. Insulina e salbutamol levam o potássio para dentro da célula; a hemodiálise retira o potássio do corpo.'),
  ('k-3', 'potassio', 3, 'Paciente com diarreia crônica tem hipocalemia que não corrige, apesar da reposição adequada. Qual eletrólito dosar?',
   '["Cálcio.","Magnésio.","Fósforo.","Sódio."]'::jsonb, 1,
   'A hipomagnesemia mantém a perda renal de potássio, e sem corrigir o magnésio a reposição não se sustenta. A diarreia crônica também faz perder magnésio.'),
  ('k-4', 'potassio', 4, 'Qual achado do eletrocardiograma é mais típico da hipocalemia?',
   '["Onda T apiculada.","Onda U proeminente.","Padrão sinusoidal.","Supradesnivelamento difuso do segmento ST."]'::jsonb, 1,
   'A hipocalemia achata a onda T, deixa a onda U proeminente e pode infradesnivelar o segmento ST. Onda T apiculada e padrão sinusoidal são da hipercalemia.'),
  ('itu-1', 'itu', 1, 'Mulher de 26 anos, não gestante, tem ardência ao urinar e aumento da frequência urinária há dois dias. Não tem febre nem dor lombar. Qual a conduta?',
   '["Pedir urocultura e aguardar o resultado para tratar.","Fosfomicina 3 g em dose única.","Ciprofloxacino por 14 dias.","Internação e antibiótico intravenoso."]'::jsonb, 1,
   'É cistite não complicada: o diagnóstico é clínico e a urocultura é dispensável. Fosfomicina em dose única ou nitrofurantoína são de primeira linha; fluoroquinolonas ficam reservadas para outras situações.'),
  ('itu-2', 'itu', 2, 'Qual é o principal agente da cistite adquirida na comunidade?',
   '["Proteus mirabilis.","Escherichia coli.","Enterococcus faecalis.","Pseudomonas aeruginosa."]'::jsonb, 1,
   'Escherichia coli responde pela grande maioria dos casos. Proteus importa mais na formação de cálculos de estruvita; Pseudomonas e Enterococcus aparecem mais em infecção hospitalar ou complicada.'),
  ('itu-3', 'itu', 3, 'Em qual paciente a bacteriúria assintomática deve ser tratada?',
   '["Idosa que vive em instituição de longa permanência.","Paciente com sonda vesical de demora.","Gestante.","Mulher com diabetes."]'::jsonb, 2,
   'Trata-se só em gestantes e antes de procedimento urológico com sangramento de mucosa. Nos outros grupos, tratar não traz benefício e aumenta a resistência bacteriana.'),
  ('itu-4', 'itu', 4, 'Mulher internada com pielonefrite segue com febre após 72 horas de antibiótico adequado ao antibiograma. Qual o próximo passo?',
   '["Trocar o antibiótico sem outra investigação.","Fazer exame de imagem para procurar obstrução ou abscesso.","Dar alta com antibiótico oral.","Indicar cistoscopia."]'::jsonb, 1,
   'Falha após 48 a 72 horas sugere complicação: obstrução ou abscesso renal ou perirrenal. Ultrassom ou tomografia orientam a conduta, e obstrução infectada precisa ser drenada.'),
  ('lit-1', 'litiase', 1, 'Na suspeita de cólica renal em adulto não gestante, qual é o exame de escolha?',
   '["Radiografia simples de abdome.","Ultrassom.","Tomografia computadorizada sem contraste.","Urografia excretora."]'::jsonb, 2,
   'A tomografia sem contraste tem a maior sensibilidade, mostra cálculos de qualquer composição e avalia complicações. O ultrassom é a escolha na gestante e uma alternativa para reduzir radiação.'),
  ('lit-2', 'litiase', 2, 'Homem de 40 anos tem cálculo de 4 mm no ureter distal. A dor está controlada, não há febre e a função renal é normal. Qual a conduta?',
   '["Ureteroscopia imediata.","Analgesia e acompanhamento, pois a chance de eliminação espontânea é alta.","Nefrolitotripsia percutânea.","Nefrostomia."]'::jsonb, 1,
   'Cálculos de até 5 mm costumam passar sozinhos. Sem infecção, dor refratária ou piora da função renal, a conduta é expectante, com analgesia.'),
  ('lit-3', 'litiase', 3, 'Paciente com cálculo obstrutivo no ureter tem febre de 39 °C e calafrios. Qual a conduta?',
   '["Litotripsia extracorpórea de urgência.","Desobstrução urgente com cateter duplo J ou nefrostomia, com antibiótico.","Terapia expulsiva com tansulosina.","Alta com analgesia e retorno em uma semana."]'::jsonb, 1,
   'É urgência: infecção atrás de uma obstrução pode evoluir para sepse. Drena-se a via urinária e trata-se a infecção; o cálculo é tratado depois.'),
  ('lit-4', 'litiase', 4, 'Para prevenir novos cálculos de oxalato de cálcio, qual orientação NÃO é recomendada?',
   '["Aumentar a ingestão de água.","Reduzir o sal da dieta.","Restringir o cálcio da dieta.","Reduzir a proteína animal."]'::jsonb, 2,
   'Restringir cálcio aumenta a absorção intestinal de oxalato e o risco de cálculo. Uma ingestão normal de cálcio protege.');

insert into public.flashcards (id, aula_id, ordem, frente, verso) values
  ('lra-f1', 'lra', 1, 'Quais são os critérios de lesão renal aguda pela creatinina?', 'Aumento de 0,3 mg/dL ou mais em 48 horas, ou valor 1,5 vez ou mais o de base em 7 dias.'),
  ('lra-f2', 'lra', 2, 'Qual é o critério de lesão renal aguda pela diurese?', 'Menos de 0,5 mL/kg por hora durante 6 horas.'),
  ('lra-f3', 'lra', 3, 'Fração de excreção de sódio: pré-renal ou necrose tubular aguda?', 'Pré-renal: abaixo de 1%. Necrose tubular aguda: acima de 2%.'),
  ('lra-f4', 'lra', 4, 'Qual é o sedimento urinário típico da necrose tubular aguda?', 'Cilindros granulosos castanho-escuros e células do epitélio tubular.'),
  ('lra-f5', 'lra', 5, 'O paciente usou diurético. Que índice usar para sugerir pré-renal?', 'Fração de excreção de ureia abaixo de 35%.'),
  ('k-f1', 'potassio', 1, 'Qual é a faixa normal do potássio sérico?', '3,5 a 5,0 mEq/L.'),
  ('k-f2', 'potassio', 2, 'Qual é a primeira alteração do eletrocardiograma na hipercalemia?', 'Onda T apiculada, alta e estreita.'),
  ('k-f3', 'potassio', 3, 'Para que serve o gluconato de cálcio na hipercalemia?', 'Estabiliza a membrana do miocárdio. Não reduz o potássio.'),
  ('k-f4', 'potassio', 4, 'Quais medidas levam o potássio para dentro da célula?', 'Insulina com glicose, beta-2 agonista inalatório e bicarbonato, se houver acidose.'),
  ('k-f5', 'potassio', 5, 'Hipocalemia que não corrige com reposição: o que dosar?', 'Magnésio. A hipomagnesemia mantém a perda renal de potássio.'),
  ('itu-f1', 'itu', 1, 'Qual é o principal agente da cistite adquirida na comunidade?', 'Escherichia coli.'),
  ('itu-f2', 'itu', 2, 'Qual é a primeira linha na cistite não complicada da mulher?', 'Nitrofurantoína por 5 a 7 dias ou fosfomicina 3 g em dose única.'),
  ('itu-f3', 'itu', 3, 'Quando tratar bacteriúria assintomática?', 'Em gestantes e antes de procedimento urológico com sangramento de mucosa.'),
  ('itu-f4', 'itu', 4, 'O que diferencia a pielonefrite da cistite?', 'Febre, calafrios, dor lombar e sinal de Giordano positivo.'),
  ('itu-f5', 'itu', 5, 'Pielonefrite sem melhora em 48 a 72 horas: o que fazer?', 'Exame de imagem para procurar obstrução ou abscesso.'),
  ('lit-f1', 'litiase', 1, 'Qual é o tipo de cálculo urinário mais comum?', 'Oxalato de cálcio.'),
  ('lit-f2', 'litiase', 2, 'Qual cálculo é radiotransparente na radiografia simples?', 'Ácido úrico.'),
  ('lit-f3', 'litiase', 3, 'Cálculo coraliforme ligado a infecção é feito de quê?', 'Estruvita (fosfato de amônio e magnésio), formada por bactérias produtoras de urease, como Proteus.'),
  ('lit-f4', 'litiase', 4, 'Qual é o exame de escolha na suspeita de cólica renal?', 'Tomografia computadorizada sem contraste. Em gestantes, ultrassom.'),
  ('lit-f5', 'litiase', 5, 'Cálculo obstrutivo com febre: qual a conduta?', 'Desobstrução urgente com cateter duplo J ou nefrostomia, mais antibiótico.');
