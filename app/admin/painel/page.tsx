import { redirect } from 'next/navigation'

// O painel foi juntado à tela Conteúdo; este endereço continua valendo para quem o tinha salvo
export default function PainelAntigo() {
  redirect('/admin/conteudo')
}
