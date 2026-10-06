// Endereço do projeto e chave pública (publishable key) do Supabase.
// Os dois são feitos para ficar visíveis no navegador: quem protege os dados
// são as regras de segurança do banco (cada aluno só acessa o próprio progresso).
// Para usar outro projeto, defina NEXT_PUBLIC_SUPABASE_URL e
// NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY nas variáveis de ambiente.

export const SUPABASE_URL =
  process.env.NEXT_PUBLIC_SUPABASE_URL ?? 'https://xtlpmtylifbalzxnfkib.supabase.co'

export const SUPABASE_KEY =
  process.env.NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY ?? 'sb_publishable_WYK9fPYCBkNK7VtFsNm-5A_efcMDwPK'
