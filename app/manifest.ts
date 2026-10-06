import type { MetadataRoute } from 'next'

// Permite instalar o site na tela inicial do celular, como um app
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Caderno Clínico',
    short_name: 'Caderno',
    description: 'Apostilas, questões e flashcards de cada aula, com o seu progresso salvo.',
    lang: 'pt-BR',
    start_url: '/',
    display: 'standalone',
    background_color: '#F2F2F7',
    theme_color: '#0B5BD3',
    icons: [
      { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
      { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
      { src: '/icons/maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
    ],
  }
}
