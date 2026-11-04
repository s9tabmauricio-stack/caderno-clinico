---
name: "bula-padrao"
description: "Use quando o usuário pedir a bula, informações ou resumo de um medicamento: apresenta a bula no chat, em linguagem técnica, com seções fixas e fonte oficial."
---

# Bula padrão

Apresentar a bula de um medicamento direto no chat, para leitor estudante/profissional da saúde, com estrutura fixa, visual limpo e fonte verificável. O resultado deve parecer uma ficha técnica bem diagramada, fácil de escanear no celular.

## 1. Buscar a fonte (sempre, antes de escrever)

- Nunca responder de memória. Pesquisar a bula atual.
- Ordem de preferência:
  1. Bulário Eletrônico da ANVISA (consultas.anvisa.gov.br) — **bula do profissional** do medicamento de referência.
  2. PDF oficial da bula do profissional publicado pelo fabricante ou hospedado por terceiros (conferir versão/data no rodapé ou no histórico de alterações).
  3. Bula do paciente da ANVISA, se a do profissional não estiver acessível.
  4. Rótulo FDA (DailyMed) ou EMA (SmPC) — só se não houver bula brasileira; avisar que a fonte é estrangeira.
- Se o usuário citar nome comercial, usar a bula daquela marca; se citar só o princípio ativo, usar o medicamento de referência e dizer qual é.
- Se houver várias apresentações/vias (ex.: oral e injetável), cobrir a mais usual e citar as outras em uma linha.
- Preferir a versão mais recente da bula; se a página de farmácia mostrar texto antigo (ex.: sem indicações novas), buscar o PDF atualizado.

## 2. Identidade visual (aplicar sempre)

- **Ícones fixos por seção** (um emoji no título, nunca no meio do texto):
  - 💊 cabeçalho · 🎯 Para que serve e como age · 💉 Posologia · 🚫 Contraindicações e interações · ⚠️ Efeitos colaterais e alertas · 📌 Pontos-chave · 📚 Fontes
- **Separador** `---` entre todas as seções.
- **Títulos de seção** em `###`. Dentro da seção, usar rótulos em negrito no início do bullet (ex.: `**Mecanismo:**`) em vez de subtítulos.
- **Negrito** só para números-chave (doses, t½, % de redução) e termos que caem em prova. No máximo 1–2 por bullet.
- **Bullets curtos**: até ~2 linhas no celular; no máximo 2 níveis de aninhamento.
- **Semáforo de gravidade** nas interações: 🔴 grave/evitar · 🟡 monitorar/ajustar · 🟢 sem relevância clínica.
- **Blockquote de alerta** para boxed warning ou risco grave principal: `> ⚠️ **Alerta:** ...` (no máximo 2 por resposta).
- **Tabelas** (máx. 3 colunas, células curtas) apenas para: ficha do cabeçalho, esquema de doses e frequência de efeitos adversos.
- Nada de introdução, fechamento ou frases de transição. Começar direto pelo cabeçalho.

## 3. Estrutura da resposta (nesta ordem, usando o modelo)

```
## 💊 NOME® · princípio ativo (DCB)
*Classe terapêutica · Laboratório*

| | |
|---|---|
| **Tarja / receita** | ex.: vermelha · retenção de receita / Portaria 344 B1 |
| **Apresentações** | formas e doses, em uma linha |
| **Via / uso** | ex.: SC · adulto e pediátrico ≥ 10 anos |

---

### 🎯 Para que serve e como age
- **Indicações:** ... (sub-bullets se houver várias)
- **Mecanismo:** 1–3 frases.
- **Farmacocinética:** F · Tmáx · t½ · ligação proteica · metabolismo (CYP) · excreção — numa linha, separados por " · ".

---

### 💉 Posologia
| Indicação | Início / titulação | Manutenção · máx. |
|---|---|---|
| ... | ... | ... |

- **Populações especiais:** pediatria, idosos, IR, IH.
- **Modo de uso:** alimento, horário, local de aplicação, não partir/mastigar.
- **Dose esquecida:** ...
- **Armazenamento:** só se for relevante (refrigerado, fotossensível).

---

### 🚫 Contraindicações e interações
- **Contraindicações:** ...

> ⚠️ **Alerta:** boxed warning ou risco grave principal, se houver.

- **Advertências:** rótulo em negrito + frase curta para cada uma.
- **Gestação e lactação:** categoria de risco + conduta.
- **Interações:**
  - 🔴 ...
  - 🟡 ...
  - 🟢 ...
  - **Alimento / álcool / exames:** ... (ou "não informado em bula")

---

### ⚠️ Efeitos colaterais e alertas
| Frequência | Reações |
|---|---|
| Muito comum (> 1/10) | ... |
| Comum (1/100–1/10) | ... |
| Incomum (1/1.000–1/100) | ... |
| Rara / muito rara | ... |

- **Sinais de alarme:** quando suspender ou procurar atendimento.
- **Superdose:** quadro + conduta + antídoto (se houver).

---

### 📌 Pontos-chave
- ✅ 3 a 5 itens que mais caem em prova ou mais importam na prática (ex.: interação clássica, ajuste renal obrigatório, efeito adverso característico).

---

### 📚 Fontes
- [Título](URL) — *Profissional · atualizada em dd/mm/aaaa*
```

- Omitir linhas da tabela ou bullets sem conteúdo em bula, em vez de deixar vazios. Se o item for obrigatório (ex.: álcool, gestação), escrever "não informado em bula".
- Tabela de frequência: agrupar reações pela frequência da bula; quando variar por indicação, indicar entre parênteses (ex.: "vômito (peso/AOS)").

## 4. Regras de conteúdo

- Português, linguagem técnica (termos farmacológicos sem explicação didática excessiva).
- Dose adulta usual e dose máxima exatamente como na bula; nunca extrapolar ou calcular doses que a bula não traz.
- Indicações: só as aprovadas em bula (marcar off-label só se o usuário perguntar).
- Parafrasear a bula; não copiar parágrafos.
- Se algo não constar na bula, escrever "não informado em bula" em vez de completar de memória.
- Comparação entre dois ou mais medicamentos: mesma identidade visual, com uma tabela resumida por seção (colunas = medicamentos, máx. 3).
- Se a pergunta for sobre o uso pessoal do usuário (quanto eu tomo, posso misturar com X), responder com o que a bula diz e lembrar em uma linha que a decisão é do médico ou farmacêutico.

## 5. Checagem final (antes de enviar)

- Todas as seções presentes, na ordem, com ícone e separador.
- Nenhuma tabela com mais de 3 colunas; nenhum bullet com mais de ~2 linhas.
- Números conferidos contra a fonte (doses, t½, frequências).
- Fonte indica tipo de bula e data de atualização.