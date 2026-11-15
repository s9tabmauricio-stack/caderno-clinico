import type { Metadata } from 'next'
import Link from 'next/link'
import { RodapeLegal } from '@/components/RodapeLegal'
import { TemaRapido } from '@/components/TemaEscolha'

export const metadata: Metadata = { title: 'Termos de Uso' }

export default function TermosPage() {
  return (
    <main className="wrap">
      <nav className="atalhos-globais" aria-label="Navegação e aparência">
        <Link className="pill" href="/">Acessar o MedGenius</Link>
        <TemaRapido />
      </nav>
      <header className="top">
        <div>
          <h1 className="big">Termos de Uso</h1>
          <p className="lead">Propriedade intelectual e uso da plataforma</p>
        </div>
      </header>
      <article className="termos-conteudo" aria-label="Propriedade intelectual e uso da plataforma">
        <p><strong>© 2026 MedGenius. Todos os direitos reservados.</strong></p>
        <p>
          O MedGenius, incluindo o código-fonte, os algoritmos, os mecanismos de estudo,
          o layout, os textos, as questões, os materiais e os demais conteúdos, é obra
          protegida pela Lei de Direitos Autorais (Lei nº 9.610/98) e pela Lei de
          Software (Lei nº 9.609/98). A titularidade é de <strong>Mauricio Faria de Souza</strong>.
        </p>
        <p>Sem autorização prévia e por escrito do titular, é proibido:</p>
        <ul>
          <li>copiar, reproduzir, distribuir ou modificar, no todo ou em parte, qualquer conteúdo ou funcionalidade da plataforma;</li>
          <li>fazer engenharia reversa, descompilar ou tentar extrair o código-fonte ou a lógica de funcionamento;</li>
          <li>usar robôs, scrapers ou qualquer meio automatizado para coletar dados ou conteúdos;</li>
          <li>criar produtos derivados ou concorrentes com base nos mecanismos da plataforma.</li>
        </ul>
        <p>
          Quem violar estes termos pode responder civil e criminalmente, conforme a
          legislação vigente, inclusive por concorrência desleal (Lei nº 9.279/96, art. 195).
        </p>
        <p>
          O nome “MedGenius” e a identidade visual pertencem ao titular e não podem
          ser usados sem autorização.
        </p>
      </article>
      <RodapeLegal />
    </main>
  )
}
