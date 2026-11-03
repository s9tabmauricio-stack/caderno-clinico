// Quando a questão ganha a faixa PROVA em volta da caixa:
// - o professor disse ou deu a entender que o ponto cai na prova (cai_na_prova), ou
// - a questão veio de uma prova antiga do próprio curso (P1, P2, P2 da turma 19, exame…).
// Revalida, Residência e outras bancas não ganham a faixa: o campo prova delas traz o nome da banca.
const PROVA_DO_CURSO = /^(p\d+(-t\d+)?|exame)$/i

export function temFaixaProva(q: { cai_na_prova: boolean; prova: string | null }): boolean {
  return q.cai_na_prova || PROVA_DO_CURSO.test(q.prova?.trim() ?? '')
}
