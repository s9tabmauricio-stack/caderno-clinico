import { createServerClient } from '@supabase/ssr'
import { cookies } from 'next/headers'
import type { Database } from '@/lib/database.types'
import { SUPABASE_KEY, SUPABASE_URL } from './config'

// Cliente usado no servidor (páginas e rotas). Crie um novo a cada uso.
export async function createClient() {
  const cookieStore = await cookies()

  return createServerClient<Database>(SUPABASE_URL, SUPABASE_KEY, {
    cookies: {
      getAll() {
        return cookieStore.getAll()
      },
      setAll(cookiesToSet) {
        try {
          cookiesToSet.forEach(({ name, value, options }) => cookieStore.set(name, value, options))
        } catch {
          // Chamado de um Server Component: o proxy já renova a sessão.
        }
      },
    },
  })
}

export type SupabaseServidor = Awaited<ReturnType<typeof createClient>>
