// Mensagens dos alunos para o administrador (botão de balão no topo, components/Mensagem.tsx).
// Ficam na tabela `mensagens`: o aluno escreve e vê só as próprias; o administrador lê, marca como lida
// e apaga em Administração → Mensagens (/admin/mensagens, com a chave secreta).

export type Mensagem = { id: string; user_id: string; autor: string; texto: string; status: string; criado_em: string }

export const LIMITE_MENSAGEM = 2000
