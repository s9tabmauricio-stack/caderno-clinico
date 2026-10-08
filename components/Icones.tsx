// Ícones de traço simples, desenhados para o Med Genius

const svg = (d: React.ReactNode) => (
  <svg viewBox="0 0 24 24" aria-hidden="true">
    {d}
  </svg>
)

export const Icone = {
  inicio: svg(<path d="M4 10.5 12 4l8 6.5V19a1.5 1.5 0 0 1-1.5 1.5H15v-6H9v6H5.5A1.5 1.5 0 0 1 4 19z" />),
  cards: svg(
    <>
      <rect x="3.5" y="7" width="13" height="13.5" rx="2.5" />
      <path d="M8 3.5h9.5a3 3 0 0 1 3 3V16" />
    </>,
  ),
  grafico: svg(
    <>
      <path d="M5 20v-4M10 20v-6M15 20v-8M20 20H3.5" />
      <path d="M4 11.5 9 7l3 2.5L19 4" />
      <path d="M15 4h4v4" />
    </>,
  ),
  pessoa: svg(
    <>
      <circle cx="12" cy="8.5" r="3.75" />
      <path d="M4.75 20c1.3-3.7 4.1-5.6 7.25-5.6s5.95 1.9 7.25 5.6" />
    </>,
  ),
  voltar: svg(<path d="M15 5l-7 7 7 7" />),
  seta: svg(<path d="M9 5l7 7-7 7" />),
  engrenagem: svg(
    <>
      <circle cx="12" cy="12" r="3" />
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z" />
    </>,
  ),
  agenda: svg(
    <>
      <rect x="3.5" y="5" width="17" height="15.5" rx="3" />
      <path d="M3.5 10h17M8 3v4M16 3v4" />
    </>,
  ),
  arquivo: svg(
    <>
      <path d="M7 3.5h7l4.5 4.5V19a1.5 1.5 0 0 1-1.5 1.5H7A1.5 1.5 0 0 1 5.5 19V5A1.5 1.5 0 0 1 7 3.5z" />
      <path d="M14 3.5V8h4.5M8.5 13h7M8.5 16.5h5" />
    </>,
  ),
  pulso: svg(<path d="M3 12.5h4l2-5 3.2 10 2.6-7 1.6 2H21" />),
  certo: svg(<path d="M5 12.5l4.5 4.5L19 7.5" />),
  errado: svg(<path d="M6.5 6.5l11 11M17.5 6.5l-11 11" />),
  cadeado: svg(
    <>
      <rect x="5" y="10.5" width="14" height="10" rx="2.5" />
      <path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5" />
    </>,
  ),
  email: svg(
    <>
      <rect x="3.5" y="5.5" width="17" height="13" rx="2.5" />
      <path d="M4.5 7l7.5 6 7.5-6" />
    </>,
  ),
}
