export const CLASSIFICACOES_QUESTAO = [
  { valor: 'rever', rotulo: 'Estudar isso aí cara!' },
  { valor: 'complicado', rotulo: 'Ver isso aí cara' },
  { valor: 'se_der_tempo', rotulo: 'É bom rever cara' },
  { valor: 'basico', rotulo: 'Tranquilo isso aí cara' },
] as const

export type ClassificacaoQuestao = (typeof CLASSIFICACOES_QUESTAO)[number]['valor']
export type FiltroClassificacao = 'todas' | 'marcadas' | ClassificacaoQuestao
export type FiltrosQuestoes = {
  tema: string | null
  fonte: FonteQuestao | null
  situacao: 'todas' | 'abertas' | 'erradas'
  classificacao: FiltroClassificacao
}

export function classificacaoValida(valor: unknown): ClassificacaoQuestao | null {
  return CLASSIFICACOES_QUESTAO.find((c) => c.valor === valor)?.valor ?? null
}

export function filtroClassificacaoValido(valor: unknown): FiltroClassificacao {
  return valor === 'marcadas' ? valor : classificacaoValida(valor) ?? 'todas'
}

export function rotuloClassificacao(valor: ClassificacaoQuestao): string {
  return CLASSIFICACOES_QUESTAO.find((c) => c.valor === valor)!.rotulo
}

// De onde veio a questão: as três fontes do filtro "Fonte" do Banco (regra do Mauricio, 08/11/2026).
// O grupo sai dos campos prova e fonte, sem mudar nada no banco; o detalhe (ex.: "P2 T23 · nº 9")
// continua escrito na própria questão.
export const FONTES_QUESTAO = [
  { valor: 'apostila', rotulo: 'Apostila' },
  { valor: 'concursos', rotulo: 'Residência e concursos' },
  { valor: 'fag', rotulo: 'Provas da FAG' },
] as const

export type FonteQuestao = (typeof FONTES_QUESTAO)[number]['valor']

// Provas do próprio curso (P1, P2, P2 da turma 23, exame) e o material da turma que está no Drive da FAG
const PROVA_DA_FAG = /^(p\d+(-t\d+)?|exame)$/i
const MATERIAL_DA_FAG = /material da turma|guia de estudo|compilados? da turma/i

export function fonteDaQuestao(q: { prova: string | null; fonte: string | null }): FonteQuestao {
  const prova = q.prova?.trim() ?? ''
  const fonte = q.fonte?.trim() ?? ''
  if (PROVA_DA_FAG.test(prova) || MATERIAL_DA_FAG.test(fonte)) return 'fag'
  // Sem prova: feita pela aula (fonte "Montada (aula 2026)" ou vazia)
  if (!prova && (!fonte || /^montada \(aula/i.test(fonte))) return 'apostila'
  // Residência, Revalida e outras bancas
  return 'concursos'
}

export function fonteValida(valor: unknown): FonteQuestao | null {
  return FONTES_QUESTAO.find((f) => f.valor === valor)?.valor ?? null
}

export function rotuloFonte(valor: FonteQuestao): string {
  return FONTES_QUESTAO.find((f) => f.valor === valor)!.rotulo
}

type QuestaoFiltravel = {
  tema: string | null
  prova: string | null
  fonte: string | null
  resposta: { acertou: boolean } | null
  classificacao: ClassificacaoQuestao | null
}

export function filtrarQuestoes<T extends QuestaoFiltravel>(lista: T[], f: FiltrosQuestoes): T[] {
  return lista.filter((q) =>
    (!f.tema || q.tema === f.tema) &&
    (!f.fonte || fonteDaQuestao(q) === f.fonte) &&
    (f.situacao === 'todas' || (f.situacao === 'abertas' ? !q.resposta : q.resposta && !q.resposta.acertou)) &&
    (f.classificacao === 'todas' || (f.classificacao === 'marcadas' ? q.classificacao !== null : q.classificacao === f.classificacao)),
  )
}
