import { redirect } from 'next/navigation'
import { INICIO_MATERIAS } from '@/lib/navegacao'

// Endereço antigo: abre diretamente a tela de matérias atual.
export default function QuestoesAntiga() {
  redirect(INICIO_MATERIAS)
}
