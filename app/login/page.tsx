import type { Metadata, Viewport } from 'next'
import { LoginForm } from '@/components/LoginForm'

export const metadata: Metadata = { title: { absolute: 'Med Genius · Entrar' } }

// A entrada segue o modo do aparelho (dia ou noite); a barra do navegador acompanha
export const viewport: Viewport = {
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#E4E7EC' },
    { media: '(prefers-color-scheme: dark)', color: '#0C0D11' },
  ],
  colorScheme: 'light dark',
}

// Dendritos de titânio saindo de trás do logo, com as pontas acesas em azul.
// Desenho de 390 × 844 com o centro do logo em (195, 191); as cores vêm do CSS (bloco "Tela de entrada").
const RAMOS = [
  'M150 154C120 134 95 104 80 64',
  'M130 194C100 196 70 184 40 164',
  'M126 229C90 254 40 274 26 324C16 364 20 424 30 484',
  'M178 120C172 90 160 66 146 40',
  'M-10 830C40 770 90 735 130 695',
]
const GALHOS = [
  'M109 116C90 108 64 108 36 116',
  'M85 187C70 204 58 224 46 250',
  'M21 396C40 404 60 416 74 436',
  'M165 78C150 74 134 64 122 48',
  'M64 755C72 728 72 706 64 682',
]
const PONTAS: [number, number, number][] = [
  [80, 64, 3], [40, 164, 3], [30, 484, 3], [146, 40, 3], [130, 695, 3],
  [36, 116, 2.6], [46, 250, 2.6], [74, 436, 2.6], [122, 48, 2.6], [64, 682, 2.6],
  [109, 116, 2.2], [85, 187, 2.2], [68, 267, 2.2],
]
const TRILHAS = [
  'M0 60H40L56 44V0',
  'M0 400H28L44 416V470',
  'M0 610H18L34 594V560',
  'M120 844V810L136 794H170',
]
const FIM_DAS_TRILHAS: [number, number][] = [[44, 475], [34, 555], [175, 794]]

function espelho(d: string) {
  // Reflete o lado esquerdo no direito: x → 390 − x (os números vêm em pares x y, H só tem x e V só tem y)
  let i = 0
  let comando = 'M'
  return d.replace(/[MCHLV]|-?\d+(?:\.\d+)?/g, (t) => {
    if (/[A-Z]/.test(t)) {
      comando = t
      i = 0
      return t
    }
    const ehX = comando === 'H' || (comando !== 'V' && i % 2 === 0)
    i++
    return ehX ? ` ${390 - Number(t)}` : ` ${t}`
  })
}

function Dendritos() {
  return (
    <svg className="lg-fundo" width="390" height="844" viewBox="0 0 390 844" aria-hidden="true">
      <defs>
        <linearGradient id="lg-ouro" x1="0" y1="0" x2="390" y2="844" gradientUnits="userSpaceOnUse">
          <stop className="o1" offset="0" />
          <stop className="o2" offset=".5" />
          <stop className="o3" offset="1" />
        </linearGradient>
        <radialGradient id="lg-luz-ouro">
          <stop className="lo" offset="0" />
          <stop className="lo fim" offset=".7" />
        </radialGradient>
        <radialGradient id="lg-luz-azul">
          <stop className="la" offset="0" />
          <stop className="la fim" offset=".7" />
        </radialGradient>
      </defs>
      <ellipse cx="195" cy="191" rx="240" ry="220" fill="url(#lg-luz-ouro)" />
      <ellipse cx="31" cy="560" rx="260" ry="240" fill="url(#lg-luz-azul)" />
      <ellipse cx="374" cy="640" rx="240" ry="220" fill="url(#lg-luz-ouro)" />
      <g className="trilhas">
        {TRILHAS.flatMap((d) => [d, espelho(d)]).map((d, k) => (
          <path key={k} d={d} />
        ))}
        {FIM_DAS_TRILHAS.flatMap(([x, y]) => [[x, y], [390 - x, y]]).map(([x, y], k) => (
          <circle key={k} cx={x} cy={y} r="3" />
        ))}
      </g>
      <g className="ramos">
        {RAMOS.flatMap((d) => [d, espelho(d)]).map((d, k) => (
          <path key={k} d={d} />
        ))}
      </g>
      <g className="galhos">
        {GALHOS.flatMap((d) => [d, espelho(d)]).map((d, k) => (
          <path key={k} d={d} />
        ))}
      </g>
      {PONTAS.flatMap(([x, y, r]) => [[x, y, r], [390 - x, y, r]]).map(([x, y, r], k) => (
        <g key={k}>
          <circle className="halo" cx={x} cy={y} r={r * 3} />
          <circle className="ponto" cx={x} cy={y} r={r} />
        </g>
      ))}
    </svg>
  )
}

export default function LoginPage() {
  return (
    <main className="tela-entrar">
      <div className="lg-palco">
        <Dendritos />
        <img className="lg-logo" src="/brand/med-genius.webp" width={150} height={150} alt="Logo Med Genius" />
        <div className="lg-marca">
          <h1>Med Genius</h1>
          <p className="lg-sub">Medicina · FAG</p>
        </div>
        <section className="lg-vidro" aria-label="Entrar">
          <LoginForm />
        </section>
      </div>
    </main>
  )
}
