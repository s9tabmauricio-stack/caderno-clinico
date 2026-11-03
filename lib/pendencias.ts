type ProgressoCards = {
  total_cards: number
  cards_estudados: number
  cards_vencidos: number
  cards_suspensos?: number
  cards_suspensos_estudados?: number
  cards_suspensos_vencidos?: number
}

// O histórico continua nos totais; só a fila do dia desconta os suspensos.
export function contarPendentes(progresso: ProgressoCards[]) {
  let novos = 0
  let vencidos = 0
  let emDia = 0
  for (const p of progresso) {
    const estudadosAtivos = p.cards_estudados - (p.cards_suspensos_estudados ?? 0)
    const vencidosAtivos = p.cards_vencidos - (p.cards_suspensos_vencidos ?? 0)
    novos += p.total_cards - (p.cards_suspensos ?? 0) - estudadosAtivos
    vencidos += vencidosAtivos
    emDia += estudadosAtivos - vencidosAtivos
  }
  return { vencidos, novos, hoje: vencidos + novos, emDia }
}
