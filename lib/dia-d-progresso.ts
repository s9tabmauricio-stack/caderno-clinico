// Progresso dos Flashcards Dia D, guardado na conta do aluno (tabela progresso_dia_d), para ele sair
// da aula e continuar de onde parou, em qualquer aparelho (pedido do Mauricio, 10/11/2026).

export type ProgressoDiaD = {
  fila: string[] // cards que faltam, na ordem; vazia = baralho fechado
  erros: string[] // cards que ele não sabia em alguma volta
  feitos: number // cards marcados como "Sabia"
}

// Acerta o progresso guardado com os cards que existem hoje: card refeito ou apagado sai da fila.
// Se a fila guardada tinha cards e nenhum deles existe mais, o baralho mudou: começa do zero (null).
export function ajustarProgressoDiaD(
  salvo: { fila?: unknown; erros?: unknown; feitos?: unknown } | null | undefined,
  idsDosCards: Iterable<string>,
): ProgressoDiaD | null {
  if (!salvo || !Array.isArray(salvo.fila) || !Array.isArray(salvo.erros)) return null
  const existe = new Set(idsDosCards)
  const valido = (id: unknown): id is string => typeof id === 'string' && existe.has(id)
  const fila = salvo.fila.filter(valido)
  if (!fila.length && salvo.fila.length) return null
  const erros = [...new Set(salvo.erros.filter(valido))]
  const feitos = typeof salvo.feitos === 'number' && Number.isFinite(salvo.feitos) && salvo.feitos > 0 ? Math.floor(salvo.feitos) : 0
  return { fila, erros, feitos }
}

export function comecarDiaD(ids: string[]): ProgressoDiaD {
  return { fila: [...ids], erros: [], feitos: 0 }
}

// "Sabia": o card sai da fila. "Não sabia": volta no fim e fica marcado entre os erros.
export function responderDiaD(p: ProgressoDiaD, sabia: boolean): ProgressoDiaD {
  if (!p.fila.length) return p
  const [atual, ...resto] = p.fila
  return {
    fila: sabia ? resto : [...resto, atual],
    erros: sabia || p.erros.includes(atual) ? p.erros : [...p.erros, atual],
    feitos: p.feitos + (sabia ? 1 : 0),
  }
}
