import { redirect } from 'next/navigation'
import { INICIO_MATERIAS } from '@/lib/navegacao'

// Mantém os endereços salvos funcionando sem exibir a antiga lista de matérias.
export default function EstudarPage() {
  redirect(INICIO_MATERIAS)
}
