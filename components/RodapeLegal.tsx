import Link from 'next/link'

export function RodapeLegal() {
  return (
    <footer className="rodape-legal">
      <p>© 2026 MedGenius – Mauricio Faria de Souza. Todos os direitos reservados.</p>
      <Link href="/termos">Termos de Uso</Link>
    </footer>
  )
}
