import type { ClassificacaoQuestao } from '@/lib/classificacao-questoes'

const SIMBOLOS = {
  rever: <><path d="M12 5v9" /><circle cx="12" cy="18" r="1" fill="currentColor" stroke="none" /></>,
  complicado: <path fill="currentColor" stroke="none" d="M13 2c1 5-3 6-2 10 2-1 3-3 3-5 4 3 6 6 5 10a7 7 0 0 1-14-1c0-4 3-6 4-8-1 4 0 5 1 5-1-5 3-7 3-11Z" />,
  se_der_tempo: <><circle cx="12" cy="12" r="8" /><path d="M12 7v5l3 2" /></>,
  basico: <path d="m5 12 5 5L20 7" />,
}

// A descrição vem do botão que contém a placa; o desenho é decorativo.
export function PlacaPrioridade({ valor }: { valor: ClassificacaoQuestao }) {
  return (
    <span className={`placa-prioridade placa--${valor}`} aria-hidden="true">
      <svg viewBox="0 0 24 24">{SIMBOLOS[valor]}</svg>
    </span>
  )
}
