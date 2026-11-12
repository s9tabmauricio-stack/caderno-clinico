import { createServerClient } from '@supabase/ssr'
import { NextResponse, type NextRequest } from 'next/server'
import { COOKIE_APARELHO, SAIU_OUTRO_APARELHO, precisaConferir, valorCookieAparelho } from '@/lib/aparelhos'
import { destinoAposLogin, rotaPublica } from '@/lib/auth'
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
      setAll(cookiesToSet, headers) {
        cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value))
        response = NextResponse.next({ request })
        Object.entries(headers).forEach(([key, value]) => response.headers.set(key, value))
        cookiesToSet.forEach(({ name, value, options }) => response.cookies.set(name, value, options))
      },
    },
  })

  // Não coloque código entre a criação do cliente e esta linha.
  const { data, error } = await supabase.auth.getClaims()
  const logado = !error && Boolean(data?.claims?.sub)
  response.headers.set('Cache-Control', 'private, no-store')

  const { pathname, searchParams } = request.nextUrl
  const publica = rotaPublica(pathname)

  // Link de e-mail que voltou para a raiz do site (endereço de retorno não liberado)
  if (pathname === '/' && searchParams.has('code')) {
    const url = request.nextUrl.clone()
    url.pathname = '/auth/callback'
    return redirecionar(url, response)
  }

  // Limite de aparelhos: a conta entrou em outro aparelho e este foi derrubado? Sai daqui na hora, com aviso.
  // Pergunta ao banco no máximo a cada 2 minutos (cookie mg_aparelho); sem isso, sairia só quando o acesso vencesse (até 1 h).
  if (logado && !publica) {
    const sessaoId = typeof data?.claims?.session_id === 'string' ? data.claims.session_id : ''
    const agora = Date.now() / 1000
    if (sessaoId && precisaConferir(request.cookies.get(COOKIE_APARELHO)?.value, sessaoId, agora)) {
      const { data: ativa, error: erroConferir } = await supabase.rpc('sessao_ativa')
      if (!erroConferir && ativa === false) {
        await supabase.auth.signOut({ scope: 'local' })
        response.cookies.delete(COOKIE_APARELHO)
        const url = request.nextUrl.clone()
        url.pathname = '/login'
        url.search = ''
        url.searchParams.set('saiu', SAIU_OUTRO_APARELHO)
        url.searchParams.set('next', destinoAposLogin(`${pathname}${request.nextUrl.search}`))
        return redirecionar(url, response)
      }
      if (!erroConferir) {
        response.cookies.set(COOKIE_APARELHO, valorCookieAparelho(sessaoId, agora), {
          httpOnly: true,
          sameSite: 'lax',
          secure: request.nextUrl.protocol === 'https:',
          path: '/',
          maxAge: 60 * 60 * 24 * 30,
        })
      }
    }
  }

  if (!logado && !publica) {
    const url = request.nextUrl.clone()
    url.pathname = '/login'
    url.search = ''
    url.searchParams.set('next', destinoAposLogin(`${pathname}${request.nextUrl.search}`))
    return redirecionar(url, response)
  }

  if (logado && pathname === '/login') {
    const url = request.nextUrl.clone()
    const destino = new URL(destinoAposLogin(searchParams.get('next')), request.url)
    url.pathname = destino.pathname
    url.search = destino.search
    url.hash = destino.hash
    return redirecionar(url, response)
  }

  return response
}

// Redireciona mantendo os cookies de sessão que acabaram de ser renovados
function redirecionar(url: URL, comCookiesDe: NextResponse) {
  const r = NextResponse.redirect(url)
  comCookiesDe.cookies.getAll().forEach((c) => r.cookies.set(c))
  for (const name of ['Cache-Control', 'Expires', 'Pragma']) {
    const value = comCookiesDe.headers.get(name)
    if (value) r.headers.set(name, value)
  }
  return r
}
