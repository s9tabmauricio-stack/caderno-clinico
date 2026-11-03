export type SessaoCards = { fila: string[]; atual: string | null; virado: boolean; feitos: number; erros: number }

// Um card errado pode ter voltado para a fila: remova todas as ocorrências,
// sem registrar avaliação nem mexer nos contadores de revisões e erros.
export function avancarSemCard(sessao: SessaoCards, cardId: string): SessaoCards {
  const fila = sessao.fila.filter((id) => id !== cardId)
  return { ...sessao, fila: fila.slice(1), atual: fila[0] ?? null, virado: false }
}
