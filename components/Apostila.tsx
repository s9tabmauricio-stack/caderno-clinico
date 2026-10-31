'use client'

import { useEffect, useLayoutEffect, useRef, useState } from 'react'
import { Icone } from './Icones'

const ZOOMS = [1, 1.5, 2, 3]

// Apostila da aula. Quando ela é publicada como as páginas do PDF (imagens dentro de .paginas), ganha:
// - um contador flutuante "Página 4 de 19" com setas para ir à página anterior ou à próxima;
// - tela cheia ao tocar numa página, com zoom (botões + e −, ou dois toques) e setas entre as páginas.
// Apostilas em texto (sem .paginas) aparecem como antes.
export function Apostila({ html }: { html: string }) {
  const artigo = useRef<HTMLElement>(null)
  const visor = useRef<HTMLDialogElement>(null)
  const area = useRef<HTMLDivElement>(null)
  const [paginas, setPaginas] = useState<HTMLImageElement[]>([])
  const [atual, setAtual] = useState(0)
  const [naTela, setNaTela] = useState(false)
  const [aberta, setAberta] = useState<number | null>(null)
  const [zoom, setZoom] = useState(0)
  // Centro da área antes de mudar o zoom, para ampliar sem perder o ponto que o aluno estava lendo
  const centro = useRef<{ x: number; y: number } | null>(null)

  // Acha as páginas, deixa cada uma "tocável" (também pelo teclado) e acompanha qual está no meio da tela
  useEffect(() => {
    const imgs = [...(artigo.current?.querySelectorAll<HTMLImageElement>('.paginas img') ?? [])]
    setPaginas(imgs)
    if (!imgs.length) return
    imgs.forEach((img, i) => {
      img.tabIndex = 0
      img.setAttribute('role', 'button')
      img.setAttribute('aria-label', `Abrir a página ${i + 1} de ${imgs.length} em tela cheia`)
    })
    const visiveis = new Set<Element>()
    const noMeio = new IntersectionObserver(
      (itens) => {
        for (const it of itens) if (it.isIntersecting) setAtual(imgs.indexOf(it.target as HTMLImageElement))
      },
      { rootMargin: '-45% 0px -45% 0px' },
    )
    const algumaNaTela = new IntersectionObserver((itens) => {
      for (const it of itens) {
        if (it.isIntersecting) visiveis.add(it.target)
        else visiveis.delete(it.target)
      }
      setNaTela(visiveis.size > 0)
    })
    imgs.forEach((img) => {
      noMeio.observe(img)
      algumaNaTela.observe(img)
    })
    return () => {
      noMeio.disconnect()
      algumaNaTela.disconnect()
    }
  }, [html])

  function abrir(i: number) {
    setZoom(0)
    setAberta(i)
    visor.current?.showModal()
    document.documentElement.style.overflow = 'hidden'
  }

  function fechar() {
    visor.current?.close()
  }

  function irPara(i: number) {
    const img = paginas[i]
    if (!img) return
    const suave = !window.matchMedia('(prefers-reduced-motion: reduce)').matches
    img.scrollIntoView({ block: 'start', behavior: suave ? 'smooth' : 'auto' })
  }

  function trocarNoVisor(i: number) {
    if (i < 0 || i >= paginas.length) return
    setAberta(i)
    area.current?.scrollTo(0, 0)
  }

  function mudarZoom(novo: number) {
    const el = area.current
    if (el) centro.current = { x: (el.scrollLeft + el.clientWidth / 2) / el.scrollWidth, y: (el.scrollTop + el.clientHeight / 2) / el.scrollHeight }
    setZoom(Math.max(0, Math.min(ZOOMS.length - 1, novo)))
  }

  // Depois de mudar o zoom, mantém no meio da tela o mesmo ponto da página
  useLayoutEffect(() => {
    const el = area.current
    const c = centro.current
    if (!el || !c) return
    el.scrollLeft = c.x * el.scrollWidth - el.clientWidth / 2
    el.scrollTop = c.y * el.scrollHeight - el.clientHeight / 2
    centro.current = null
  }, [zoom])

  // Setas do teclado e + / − dentro da tela cheia (Esc fecha sozinho, pelo próprio <dialog>)
  useEffect(() => {
    if (aberta === null) return
    function tecla(e: KeyboardEvent) {
      if (e.key === 'ArrowRight') trocarNoVisor((aberta ?? 0) + 1)
      else if (e.key === 'ArrowLeft') trocarNoVisor((aberta ?? 0) - 1)
      else if (e.key === '+' || e.key === '=') mudarZoom(zoom + 1)
      else if (e.key === '-') mudarZoom(zoom - 1)
      else return
      e.preventDefault()
    }
    window.addEventListener('keydown', tecla)
    return () => window.removeEventListener('keydown', tecla)
  })

  function tocarNoArtigo(e: React.MouseEvent | React.KeyboardEvent) {
    if ('key' in e && e.key !== 'Enter' && e.key !== ' ') return
    const img = (e.target as HTMLElement).closest('.paginas img')
    const i = img ? paginas.indexOf(img as HTMLImageElement) : -1
    if (i < 0) return
    e.preventDefault()
    abrir(i)
  }

  const total = paginas.length
  const pagina = aberta !== null ? paginas[aberta] : null

  return (
    <>
      <article ref={artigo} className="ap" onClick={tocarNoArtigo} onKeyDown={tocarNoArtigo} dangerouslySetInnerHTML={{ __html: html }} />

      {total > 1 && (
        <div className="ap-contador" hidden={!naTela} role="navigation" aria-label="Páginas da apostila">
          <button type="button" onClick={() => irPara(atual - 1)} disabled={atual === 0} aria-label="Página anterior">
            {Icone.voltar}
          </button>
          <span aria-live="polite">
            Página {atual + 1} de {total}
          </span>
          <button type="button" onClick={() => irPara(atual + 1)} disabled={atual >= total - 1} aria-label="Próxima página">
            {Icone.seta}
          </button>
          <button type="button" onClick={() => abrir(atual)} aria-label={`Abrir a página ${atual + 1} em tela cheia`}>
            {Icone.ampliar}
          </button>
        </div>
      )}

      <dialog
        ref={visor}
        className="ap-visor"
        aria-label="Página da apostila em tela cheia"
        onClose={() => {
          // Volta à apostila na página que o aluno estava vendo na tela cheia
          if (aberta !== null) paginas[aberta]?.scrollIntoView({ block: 'start' })
          setAberta(null)
          document.documentElement.style.overflow = ''
        }}
      >
        {pagina && aberta !== null && (
          <>
            <div className="ap-visor-topo">
              <span className="ap-visor-t">
                Página {aberta + 1} de {total}
              </span>
              <button type="button" className="ap-visor-b" onClick={() => mudarZoom(zoom - 1)} disabled={zoom === 0} aria-label="Diminuir o zoom">
                {Icone.menos}
              </button>
              <span className="ap-visor-z">{Math.round(ZOOMS[zoom] * 100)}%</span>
              <button
                type="button"
                className="ap-visor-b"
                onClick={() => mudarZoom(zoom + 1)}
                disabled={zoom === ZOOMS.length - 1}
                aria-label="Aumentar o zoom"
              >
                {Icone.mais}
              </button>
              <button type="button" className="btn sm ap-visor-fechar" onClick={fechar}>
                Fechar
              </button>
            </div>
            <div className="ap-visor-area" ref={area}>
              {/* eslint-disable-next-line @next/next/no-img-element -- a mesma imagem da página, já baixada */}
              <img
                src={pagina.currentSrc || pagina.src}
                alt={pagina.alt}
                style={{ width: `${ZOOMS[zoom] * 100}%` }}
                onDoubleClick={() => mudarZoom(zoom === 0 ? 2 : 0)}
              />
            </div>
            <div className="ap-visor-pe">
              <button type="button" className="btn ghost sm" onClick={() => trocarNoVisor(aberta - 1)} disabled={aberta === 0}>
                {Icone.voltar}
                <span>Anterior</span>
              </button>
              <button type="button" className="btn ghost sm" onClick={() => trocarNoVisor(aberta + 1)} disabled={aberta >= total - 1}>
                <span>Próxima</span>
                {Icone.seta}
              </button>
            </div>
          </>
        )}
      </dialog>
    </>
  )
}
