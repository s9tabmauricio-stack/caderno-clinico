/** Ordena pela próxima prova válida; sem prova futura mantém a ordem original ao final. */
export function ordenarMateriasPorProva<T extends { id: string }>(
  materias: T[],
  provas: { materia: string | null; data: string; inicio: string | null; cancelado: boolean }[],
  agora: number,
): T[] {
  const datas = new Map<string, number>()
  for (const prova of provas) {
    const inicio = Date.parse(`${prova.data}T${(prova.inicio ?? '00:00').slice(0, 5)}:00-03:00`)
    if (!prova.materia || prova.cancelado || inicio <= agora || !Number.isFinite(inicio)) continue
    datas.set(prova.materia, Math.min(datas.get(prova.materia) ?? Infinity, inicio))
  }
  return [...materias].sort((a, b) => (datas.get(a.id) ?? Infinity) - (datas.get(b.id) ?? Infinity))
}
