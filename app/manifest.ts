import type { MetadataRoute } from 'next'

// Permite instalar o site na tela inicial do celular ou do tablet, como um app
export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'Med Genius',
    short_name: 'Med Genius',
    description: 'Apostilas, questões e flashcards de cada aula, com o seu progresso salvo.',
    lang: 'pt-BR',
    start_url: '/',
    display: 'standalone',
    background_color: '#0E1124',
    theme_color: '#0E1124',
    icons: [
      { src: '/icons/icon-192.png', sizes: '192x192', type: 'image/png' },
      { src: '/icons/icon-512.png', sizes: '512x512', type: 'image/png' },
      { src: '/icons/maskable-512.png', sizes: '512x512', type: 'image/png', purpose: 'maskable' },
    ],
  }
}
