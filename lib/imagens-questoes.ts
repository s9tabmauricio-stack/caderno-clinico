// Imagens das questões (28/11/2026): ficam no espaço público "questoes" do Supabase Storage;
// questoes.imagens guarda os caminhos lá dentro, na ordem. A maioria das questões não tem nenhuma.
import { SUPABASE_URL } from '@/lib/supabase/config'

/** 'neuro29-a1/neuro29-a1-q05-1.webp' → endereço público da imagem (um endereço completo passa direto). */
export function urlImagemQuestao(caminho: string) {
  if (/^https?:\/\//.test(caminho)) return caminho
  return `${SUPABASE_URL}/storage/v1/object/public/questoes/${caminho.split('/').map(encodeURIComponent).join('/')}`
}
