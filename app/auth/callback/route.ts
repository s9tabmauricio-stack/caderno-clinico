import { NextResponse, type NextRequest } from 'next/server'
import { createClient } from '@/lib/supabase/server'

// Volta do link de e-mail (ou do Google): troca o código pela sessão do aluno
export async function GET(request: NextRequest) {
  const { searchParams, origin } = new URL(request.url)
  const code = searchParams.get('code')
  const destino = caminhoSeguro(searchParams.get('next'))

  if (code) {
    const supabase = await createClient()
    const { error } = await supabase.auth.exchangeCodeForSession(code)
    if (!error) return NextResponse.redirect(`${origin}${destino}`)
  }

  const motivo = searchParams.get('error_description')
  return NextResponse.redirect(`${origin}/auth/erro${motivo ? `?motivo=${encodeURIComponent(motivo)}` : ''}`)
}

function caminhoSeguro(next: string | null) {
  return next && next.startsWith('/') && !next.startsWith('//') ? next : '/'
}
