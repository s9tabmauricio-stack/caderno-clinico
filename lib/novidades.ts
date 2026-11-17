// Novidades do app, mostradas no botão do sininho ao lado da engrenagem (components/Novidades.tsx).
// Para avisar a turma de algo novo: ponha um item NO TOPO da lista, com um `id` que nunca foi usado
// (data + palavra). Quem ainda não viu esse `id` vê a bolinha piscando até abrir o painel.
// Escreva para o aluno, em uma ou duas frases simples. Mantenha só as ~10 mais recentes.

export type Novidade = { id: string; data: string; titulo: string; texto: string }

export const NOVIDADES: Novidade[] = [
  {
    id: '2026-11-17-novidades',
    data: '17/11/2026',
    titulo: 'Novidades por aqui',
    texto: 'Este sininho avisa quando o app ganha algo novo. A bolinha some depois que você abre.',
  },
  {
    id: '2026-11-17-modo-crazy',
    data: '17/11/2026',
    titulo: 'Estudo diário e Modo CRAZY',
    texto:
      'No cartão de cada aula, na matéria: Apostila, Questões e Flashcards ficam no Estudo diário; Provas da FAG e FastCardsGenius ficam no Modo CRAZY, para a véspera da prova.',
  },
  {
    id: '2026-11-17-fastcards',
    data: '17/11/2026',
    titulo: 'FastCardsGenius',
    texto:
      'Os antigos Flashcards Dia D agora se chamam FastCardsGenius: um baralho rápido de véspera para resolver as questões das Provas da FAG.',
  },
]

export const CHAVE_NOVIDADES = 'mg-novidades-vistas'
