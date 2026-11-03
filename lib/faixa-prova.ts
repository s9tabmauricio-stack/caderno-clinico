// Quando a questão ganha a faixa PROVA em volta da caixa:
// - o professor disse ou deu a entender que o ponto cai na prova (cai_na_prova), ou
// - a questão veio de uma prova antiga do próprio curso (P1, P2, P2 da turma 19, exame…).
// Revalida, Residência e outras bancas não ganham a faixa: o campo prova delas traz o nome da banca.
const PROVA_DO_CURSO = /^(p\d+(-t\d+)?|exame)$/i

export function temFaixaProva(q: { cai_na_prova: boolean; prova: string | null }): boolean {
  return q.cai_na_prova || PROVA_DO_CURSO.test(q.prova?.trim() ?? '')
}

// Flashcards: a marca é o "PROVA · " no começo da frente (o professor disse ou deu a entender que cai).
// Por enquanto a faixa só aparece em Pneumo, a matéria em que a marca já foi conferida aula por aula.
const MARCA_CARD = /^\s*PROVA\s*·\s*/
const MATERIAS_COM_FAIXA_NO_CARD = new Set(['pneumo'])

export function cardDeProva(c: { frente: string; materia_id: string }): { faixa: boolean; frente: string } {
  if (!MATERIAS_COM_FAIXA_NO_CARD.has(c.materia_id) || !MARCA_CARD.test(c.frente)) return { faixa: false, frente: c.frente }
  return { faixa: true, frente: c.frente.replace(MARCA_CARD, '') }
}
