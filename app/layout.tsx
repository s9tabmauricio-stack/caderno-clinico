import type { Metadata, Viewport } from 'next'
import '@fontsource-variable/inter'
import './globals.css'

export const metadata: Metadata = {
  title: { default: 'Caderno Clínico', template: '%s · Caderno Clínico' },
  description: 'Apostilas, questões e flashcards de cada aula, com o seu progresso salvo.',
  applicationName: 'Caderno Clínico',
  appleWebApp: { capable: true, title: 'Caderno Clínico', statusBarStyle: 'default' },
}

export const viewport: Viewport = {
  viewportFit: 'cover',
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#F2F2F7' },
    { media: '(prefers-color-scheme: dark)', color: '#0B0C10' },
  ],
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR">
      <body>{children}</body>
    </html>
  )
}
