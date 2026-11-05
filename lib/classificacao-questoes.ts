export const CLASSIFICACOES_QUESTAO = [
  { valor: 'rever', rotulo: 'Tenho que ver isso aí cara' },
  { valor: 'complicado', rotulo: 'Complicado isso ai cara' },
  { valor: 'se_der_tempo', rotulo: 'Não custa nada ver de novo cara' },
  { valor: 'basico', rotulo: 'Essa é ensino básico' },
] as const

export type ClassificacaoQuestao = (typeof CLASSIFICACOES_QUESTAO)[number]['valor']
export type FiltroClassificacao = 'todas' | 'marcadas' | ClassificacaoQuestao
export type FiltrosQuestoes = {
  tema: string | null
  prova: string | null
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

type QuestaoFiltravel = {
  tema: string | null
  prova: string | null
  resposta: { acertou: boolean } | null
  classificacao: ClassificacaoQuestao | null
}

export function filtrarQuestoes<T extends QuestaoFiltravel>(lista: T[], f: FiltrosQuestoes): T[] {
  return lista.filter((q) =>
    (!f.tema || q.tema === f.tema) &&
    (!f.prova || q.prova === f.prova) &&
    (f.situacao === 'todas' || (f.situacao === 'abertas' ? !q.resposta : q.resposta && !q.resposta.acertou)) &&
    (f.classificacao === 'todas' || (f.classificacao === 'marcadas' ? q.classificacao !== null : q.classificacao === f.classificacao)),
  )
}
