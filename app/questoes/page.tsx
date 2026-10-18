import { redirect } from 'next/navigation'

// A aba Questões virou parte da aba Estudar; este endereço continua valendo para quem o tinha salvo
export default function QuestoesAntiga() {
  redirect('/estudar')
}
