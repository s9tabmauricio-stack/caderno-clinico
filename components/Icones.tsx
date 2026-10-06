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
  grafico: svg(<path d="M5 20v-8M12 20V5M19 20v-5" />),
  pessoa: svg(
    <>
      <circle cx="12" cy="8.5" r="3.75" />
      <path d="M4.75 20c1.3-3.7 4.1-5.6 7.25-5.6s5.95 1.9 7.25 5.6" />
    </>,
  ),
  voltar: svg(<path d="M15 5l-7 7 7 7" />),
  seta: svg(<path d="M9 5l7 7-7 7" />),
  arquivo: svg(
    <>
      <path d="M7 3.5h7l4.5 4.5V19a1.5 1.5 0 0 1-1.5 1.5H7A1.5 1.5 0 0 1 5.5 19V5A1.5 1.5 0 0 1 7 3.5z" />
      <path d="M14 3.5V8h4.5M8.5 13h7M8.5 16.5h5" />
    </>,
  ),
  pulso: svg(<path d="M3 12.5h4l2-5 3.2 10 2.6-7 1.6 2H21" />),
  certo: svg(<path d="M5 12.5l4.5 4.5L19 7.5" />),
  errado: svg(<path d="M6.5 6.5l11 11M17.5 6.5l-11 11" />),
  email: svg(
    <>
      <rect x="3.5" y="5.5" width="17" height="13" rx="2.5" />
      <path d="M4.5 7l7.5 6 7.5-6" />
    </>,
  ),
}
