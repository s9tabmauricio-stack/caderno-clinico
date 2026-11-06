/** Sem matéria vinculada, nunca voltar aos totais gerais. */
export function daProximaProva<T extends { materia_id: string }>(itens: T[], materia: string | undefined): T[] {
  return materia ? itens.filter((item) => item.materia_id === materia) : []
}

/** Reserva os dias anteriores à prova; hoje e amanhã exigem concluir hoje. */
export function ritmoDiario(restantes: number, diasAteProva: number): number {
  return Math.ceil(Math.max(0, restantes) / Math.max(1, diasAteProva))
}
