// Lê os rascunhos de flashcards e de questões (formato dos agentes em .claude/agents/)
// e monta as linhas do banco. Só funções puras: quem grava é scripts/gravar-rascunho.mjs.

/** "gastro-a4" → "gastro". */
export function materiaDaAula(aulaId) {
  const m = /^([a-z0-9]+)-a\d+$/.exec(aulaId)
  if (!m) throw new Error(`Id de aula fora do padrão <materia>-a<N>: ${aulaId}`)
  return m[1]
}

/** Número do card ou da questão no id: 1 → "01", 99 → "99", 100 → "100" (nunca corta). */
export function numeroId(n) {
  return n < 100 ? String(n).padStart(2, '0') : String(n)
}

// Partes do rascunho que não são itens: dúvidas e o relatório do revisor.
const FIM = /^##\s+(Dúvidas|Revisão)\b/i

function linhasUteis(md) {
  const linhas = md.replace(/\r\n?/g, '\n').split('\n')
  const fim = linhas.findIndex((l) => FIM.test(l))
  return fim === -1 ? linhas : linhas.slice(0, fim)
}

function confereSequencia(itens, tipo) {
  itens.forEach((item, i) => {
    if (item.n !== i + 1) throw new Error(`${tipo}: esperava o número ${i + 1} e achei ${item.n}. Renumere o rascunho de 1 até o fim.`)
  })
}

/**
 * Flashcards: cada card é "**N.** frente" e, abaixo, "↳ verso".
 * Devolve [{ n, frente, verso }].
 */
export function lerFlashcards(md) {
  const cards = []
  let atual = null
  for (const linha of linhasUteis(md)) {
    const cab = /^\*\*(\d+)\.\*\*\s+(.*)$/.exec(linha.trim())
    if (cab) {
      atual = { n: Number(cab[1]), frente: cab[2].trim(), verso: '' }
      cards.push(atual)
      continue
    }
    const verso = /^↳\s?(.*)$/.exec(linha.trim())
    if (verso && atual) {
      if (atual.verso) throw new Error(`Card ${atual.n}: tem dois versos.`)
      atual.verso = verso[1].trim()
      continue
    }
    if (/^#/.test(linha) || !linha.trim()) { if (atual?.verso) atual = null; continue }
    // continuação de uma linha longa
    if (atual) {
      if (atual.verso) atual.verso += ' ' + linha.trim()
      else atual.frente += ' ' + linha.trim()
    }
  }
  for (const c of cards) {
    if (!c.frente) throw new Error(`Card ${c.n}: frente vazia.`)
    if (!c.verso) throw new Error(`Card ${c.n}: falta o verso (linha "↳ …").`)
  }
  confereSequencia(cards, 'Flashcards')
  return cards
}

/** Linhas do banco para os flashcards (id <aula>-f01…). */
export function linhasFlashcards(aulaId, cards) {
  return cards.map((c) => ({
    id: `${aulaId}-f${numeroId(c.n)}`,
    aula_id: aulaId,
    ordem: c.n,
    frente: c.frente,
    verso: c.verso,
  }))
}

/**
 * Questões: "### N · [PROVA ·] tema: …", enunciado, cinco "- A) …" (a certa com *),
 * "**Comentário:** …" e "**Por que as erradas:**" com uma linha por letra.
 * Devolve [{ n, prova, tema, enunciado, alternativas, correta, comentario, por_que_erradas }].
 */
export function lerQuestoes(md) {
  const questoes = []
  let q = null
  let parte = null
  const juntar = (texto, linha) => (texto ? texto + '\n' + linha : linha)

  for (const bruta of linhasUteis(md)) {
    const linha = bruta.trimEnd()
    const cab = /^###\s+(\d+)\s*·\s*(.*)$/.exec(linha)
    if (cab) {
      const resto = cab[2]
      const tema = /tema:\s*(.+)$/i.exec(resto)
      const substitui = /substitui:\s*([a-z0-9-]+)/i.exec(resto)
      q = {
        n: Number(cab[1]),
        ...(substitui ? { substitui: substitui[1] } : {}),
        prova: /(^|·)\s*PROVA\s*(·|$)/.test(resto),
        tema: tema ? tema[1].trim() : '',
        enunciado: '',
        alternativas: [],
        certas: [],
        comentario: '',
        por_que_erradas: '',
      }
      questoes.push(q)
      parte = 'enunciado'
      continue
    }
    if (/^##\s/.test(linha)) { q = null; parte = null; continue }
    if (!q) continue

    const alt = /^-\s+([A-E])(\*?)\)\s*(.*)$/.exec(linha)
    if (alt && (parte === 'enunciado' || parte === 'alternativas')) {
      if (alt[2]) q.certas.push(q.alternativas.length)
      q.alternativas.push(alt[3].trim())
      parte = 'alternativas'
      continue
    }
    const com = /^\*\*Comentário:\*\*\s*(.*)$/.exec(linha)
    if (com) { q.comentario = com[1].trim(); parte = 'comentario'; continue }
    const pq = /^\*\*Por que as erradas:\*\*\s*(.*)$/.exec(linha)
    if (pq) { q.por_que_erradas = pq[1].trim(); parte = 'porque'; continue }

    if (!linha.trim()) continue
    if (parte === 'enunciado') q.enunciado = juntar(q.enunciado, linha.trim())
    else if (parte === 'alternativas') q.alternativas[q.alternativas.length - 1] += ' ' + linha.trim()
    else if (parte === 'comentario') q.comentario = juntar(q.comentario, linha.trim())
    else if (parte === 'porque') q.por_que_erradas = juntar(q.por_que_erradas, linha.trim())
  }

  for (const x of questoes) {
    const erro = (m) => { throw new Error(`Questão ${x.n}: ${m}`) }
    if (!x.enunciado) erro('enunciado vazio.')
    if (x.alternativas.length !== 5) erro(`tem ${x.alternativas.length} alternativas (precisa de 5, de A a E).`)
    if (x.certas.length !== 1) erro(`tem ${x.certas.length} alternativas com * (precisa de uma só).`)
    if (!x.tema) erro('falta o "tema:" no título.')
    if (!x.comentario) erro('falta o **Comentário:**.')
    if (!x.por_que_erradas) erro('falta o **Por que as erradas:**.')
    x.correta = x.certas[0]
    delete x.certas
  }
  confereSequencia(questoes, 'Questões')
  return questoes
}

/** Linhas do banco para as questões, continuando a ordem da matéria e a numeração da aula. */
export function linhasQuestoes(aulaId, questoes, { ultimaOrdem, ultimoNumero, ano }) {
  const materia = materiaDaAula(aulaId)
  return questoes.map((x, i) => ({
    id: `${aulaId}-q${numeroId(ultimoNumero + x.n)}`,
    materia_id: materia,
    aula_id: aulaId,
    ordem: ultimaOrdem + i + 1,
    enunciado: x.enunciado,
    alternativas: x.alternativas,
    correta: x.correta,
    comentario: x.comentario,
    por_que_erradas: x.por_que_erradas,
    tema: x.tema,
    prova: null,
    fonte: `Montada (aula ${ano})`,
    origem: 'montada',
    cai_na_prova: x.prova,
  }))
}

/** Maior número de questão já usado na aula ("-q07", "-q07-v2" → 7). */
export function ultimoNumeroDosIds(ids) {
  let maior = 0
  for (const id of ids) {
    const m = /-q(\d+)/.exec(id)
    if (m) maior = Math.max(maior, Number(m[1]))
  }
  return maior
}

/** Texto para comparar enunciados (ignora espaços e maiúsculas). */
export function normalizar(texto) {
  return String(texto).toLowerCase().replace(/\s+/g, ' ').trim()
}

// ---------- SQL (para quem só tem o conector do Supabase) ----------

function sqlTexto(v) {
  if (v === null || v === undefined) return 'null'
  if (typeof v === 'boolean' || typeof v === 'number') return String(v)
  return "'" + String(v).replace(/'/g, "''") + "'"
}

// Quebras de linha viram chr(10), como manda a receita.
function sqlMultilinha(v) {
  return String(v).split('\n').map(sqlTexto).join(" || chr(10) || ")
}

export function sqlFlashcards(linhas) {
  const valores = linhas.map((l) => `(${[l.id, l.aula_id, l.ordem, l.frente, l.verso].map(sqlTexto).join(', ')})`)
  return `insert into public.flashcards (id, aula_id, ordem, frente, verso) values\n${valores.join(',\n')}\non conflict (id) do nothing returning id;\n`
}

export function sqlQuestoes(linhas) {
  const valores = linhas.map((l) => '(' + [
    sqlTexto(l.id), sqlTexto(l.materia_id), sqlTexto(l.aula_id), l.ordem,
    sqlMultilinha(l.enunciado), sqlTexto(JSON.stringify(l.alternativas)) + '::jsonb', l.correta,
    sqlMultilinha(l.comentario), sqlMultilinha(l.por_que_erradas), sqlTexto(l.tema),
    'null', sqlTexto(l.fonte), sqlTexto(l.origem), l.cai_na_prova,
  ].join(', ') + ')')
  return `insert into public.questoes (id, materia_id, aula_id, ordem, enunciado, alternativas, correta, comentario, por_que_erradas, tema, prova, fonte, origem, cai_na_prova) values\n${valores.join(',\n')}\non conflict (id) do nothing returning id;\n`
}

/** Divide em lotes de até n itens. */
export function lotes(lista, n) {
  const saida = []
  for (let i = 0; i < lista.length; i += n) saida.push(lista.slice(i, i + n))
  return saida
}

// ---------- Substituir questões que já estão no banco (versões -v2) ----------

/** Id da versão nova: "x-q07" → "x-q07-v2"; "x-q07-v2" → "x-q07-v3". */
export function idNovaVersao(id) {
  const m = /^(.*)-v(\d+)$/.exec(id)
  return m ? `${m[1]}-v${Number(m[2]) + 1}` : `${id}-v2`
}

/**
 * SQL para trocar questões do banco pelas do rascunho (título com "substitui: <id>"),
 * como manda o manual: inclui a versão nova copiando da antiga ordem, tema, fonte, origem,
 * prova e cai_na_prova; marca a antiga com substituida_por e leva os recados junto.
 * Só age se a antiga ainda estiver ativa e for montada (questão de prova real não se reescreve),
 * então rodar duas vezes não duplica nada.
 */
export function sqlSubstituicoes(questoes) {
  return questoes.map((q) => {
    if (!q.substitui) throw new Error(`Questão ${q.n}: falta o "substitui: <id>" no título.`)
    const velho = sqlTexto(q.substitui)
    const novo = sqlTexto(idNovaVersao(q.substitui))
    return `insert into public.questoes (id, materia_id, aula_id, ordem, enunciado, alternativas, correta, comentario, por_que_erradas, tema, prova, fonte, origem, cai_na_prova)
select ${novo}, materia_id, aula_id, ordem, ${sqlMultilinha(q.enunciado)}, ${sqlTexto(JSON.stringify(q.alternativas))}::jsonb, ${q.correta}, ${sqlMultilinha(q.comentario)}, ${sqlMultilinha(q.por_que_erradas)}, tema, prova, fonte, origem, cai_na_prova
from public.questoes where id = ${velho} and substituida_por is null and origem = 'montada'
on conflict (id) do nothing;
update public.questoes set substituida_por = ${novo} where id = ${velho} and substituida_por is null and exists (select 1 from public.questoes where id = ${novo});
update public.recados set questao_id = ${novo} where questao_id = ${velho} and exists (select 1 from public.questoes where id = ${novo});
`
  }).join('\n')
}
