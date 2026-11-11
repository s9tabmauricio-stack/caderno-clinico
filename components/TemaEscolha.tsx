'use client'

import { useSyncExternalStore } from 'react'
import { CHAVE_TEMA, type Escolha } from '@/lib/tema'

const OPCOES: { valor: Escolha; rotulo: string; dica: string; icone: React.ReactNode }[] = [
  {
    valor: 'auto',
    rotulo: 'Auto',
    dica: 'Automático: segue o modo do celular',
    icone: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="12" cy="12" r="8" />
        <path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor" />
      </svg>
    ),
  },
  {
    valor: 'dia',
    rotulo: 'Dia',
    dica: 'Sempre claro',
    icone: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <circle cx="12" cy="12" r="4" />
        <path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4" />
      </svg>
    ),
  },
  {
    valor: 'noite',
    rotulo: 'Noite',
    dica: 'Sempre escuro',
    icone: (
      <svg viewBox="0 0 24 24" aria-hidden="true">
        <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z" />
      </svg>
    ),
  },
]

// A escolha mora no <html> (data-escolha, posto pelo script de lib/tema.ts); o botão só acompanha
function assinar(avisar: () => void) {
  const obs = new MutationObserver(avisar)
  obs.observe(document.documentElement, { attributes: true, attributeFilter: ['data-escolha'] })
  return () => obs.disconnect()
}
const escolhaAtual = () => (document.documentElement.getAttribute('data-escolha') as Escolha | null) ?? 'auto'
const escolhaNoServidor = (): Escolha => 'auto'

// Grava a escolha no aparelho e repinta o app na hora
function escolher(valor: Escolha) {
  let salvo = false
  try {
    localStorage.setItem(CHAVE_TEMA, valor)
    salvo = localStorage.getItem(CHAVE_TEMA) === valor
  } catch {
    // sem armazenamento (aba anônima): troca só nesta visita
  }
  const aplicar = (window as Window & { __mgTema?: () => void }).__mgTema
  if (aplicar && salvo) {
    aplicar()
  } else {
    const raiz = document.documentElement
    const dia = valor === 'dia' || (valor === 'auto' && matchMedia('(prefers-color-scheme: light)').matches)
    raiz.setAttribute('data-tema', dia ? 'dia' : 'noite')
    raiz.setAttribute('data-escolha', valor)
  }
}

const useEscolha = () => useSyncExternalStore(assinar, escolhaAtual, escolhaNoServidor)

/** Auto | Dia | Noite: vale para o app todo, neste aparelho. */
export function TemaEscolha() {
  const escolha = useEscolha()
  return (
    <div className="tema-seg" role="group" aria-label="Aparência">
      {OPCOES.map((o) => (
        <button key={o.valor} type="button" title={o.dica} aria-pressed={escolha === o.valor} onClick={() => escolher(o.valor)}>
          {o.icone}
          {o.rotulo}
        </button>
      ))}
    </div>
  )
}

/** A mesma escolha, só com os ícones, discreta ao lado da engrenagem (todas as telas logadas). */
export function TemaRapido() {
  const escolha = useEscolha()
  return (
    <div className="tema-rapido" role="group" aria-label="Aparência">
      {OPCOES.map((o) => (
        <button
          key={o.valor}
          type="button"
          title={o.dica}
          aria-label={o.rotulo}
          aria-pressed={escolha === o.valor}
          onClick={() => escolher(o.valor)}
        >
          {o.icone}
        </button>
      ))}
    </div>
  )
}
