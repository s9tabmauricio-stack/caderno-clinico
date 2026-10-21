import type { Metadata, Viewport } from 'next'
import '@fontsource-variable/cinzel'
import '@fontsource-variable/inter'
import './globals.css'
import { SCRIPT_TEMA } from '@/lib/tema'

export const metadata: Metadata = {
  title: { default: 'Med Genius', template: 'Med Genius · %s' },
  description: 'Apostilas, questões e flashcards de cada aula, com o seu progresso salvo.',
  applicationName: 'Med Genius',
  appleWebApp: { capable: true, title: 'Med Genius', statusBarStyle: 'default' },
}

export const viewport: Viewport = {
  viewportFit: 'cover',
  // O app segue o modo do aparelho (dia ou noite) ou a escolha do aluno; a barra do navegador acompanha (lib/tema.ts)
  themeColor: [
    { media: '(prefers-color-scheme: light)', color: '#E4E7EC' },
    { media: '(prefers-color-scheme: dark)', color: '#0C0D11' },
  ],
  colorScheme: 'light dark',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // data-tema (dia/noite) é posto pelo script antes da primeira pintura; o servidor não sabe a escolha
    <html lang="pt-BR" data-tema="noite" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: SCRIPT_TEMA }} />
      </head>
      <body>{children}</body>
    </html>
  )
}
