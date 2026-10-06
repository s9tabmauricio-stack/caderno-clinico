import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'
import type { Database } from '@/lib/database.types'
import { SUPABASE_KEY, SUPABASE_URL } from './config'

// Roda antes de cada página: renova a sessão do aluno e decide para onde ele vai.
export async function updateSession(request: NextRequest) {
  let response = NextResponse.next({ request })

  const supabase = createServerClient<Database>(SUPABASE_URL, SUPABASE_KEY, {
    cookies: {
      getAll() {
        return request.cookies.getAll()
      },
      setAll(cookiesToSet) {
        cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value))
        response = NextResponse.next({ request })
        cookiesToSet.forEach(({ name, value, options }) => response.cookies.set(name, value, options))
      },
    },
  })

  // Não coloque código entre a criação do cliente e esta linha.
  const { data } = await supabase.auth.getClaims()
  const logado = Boolean(data?.claims)

  const { pathname, searchParams } = request.nextUrl
  const publica = pathname.startsWith('/login') || pathname.startsWith('/auth')

  // Link de e-mail que voltou para a raiz do site (endereço de retorno não liberado)
  if (pathname === '/' && searchParams.has('code')) {
    const url = request.nextUrl.clone()
    url.pathname = '/auth/callback'
    return redirecionar(url, response)
  }

  if (!logado && !publica) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    url.search = ''
    return redirecionar(url, response)
  }

  if (logado && pathname.startsWith('/login')) {
    const url = request.nextUrl.clone()
    url.pathname = '/'
    url.search = ''
    return redirecionar(url, response)
  }

  return response
}

// Redireciona mantendo os cookies de sessão que acabaram de ser renovados
function redirecionar(url: URL, comCookiesDe: NextResponse) {
  const r = NextResponse.redirect(url)
  comCookiesDe.cookies.getAll().forEach((c) => r.cookies.set(c))
  return r
}
