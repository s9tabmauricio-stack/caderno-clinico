import type { Metadata, Viewport } from 'next'
import '@fontsource-variable/cinzel'
import '@fontsource-variable/inter'
import './globals.css'

export const metadata: Metadata = {
  title: { default: 'Med Genius', template: 'Med Genius · %s' },
  description: 'Apostilas, questões e flashcards de cada aula, com o seu progresso salvo.',
  applicationName: 'Med Genius',
  appleWebApp: { capable: true, title: 'Med Genius', statusBarStyle: 'default' },
}

export const viewport: Viewport = {
  viewportFit: 'cover',
  // O app segue o modo do aparelho (dia ou noite); a barra do navegador acompanha
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#E4E7EC' },
    { media: '(prefers-color-scheme: dark)', color: '#0C0D11' },
  ],
  colorScheme: 'light dark',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}
