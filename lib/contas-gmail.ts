// Robô do Gmail (docs/robo-gmail/): regras de quem pode ganhar conta sozinho.
// Sem importações, para os testes rodarem direto no Node.

/** Só e-mails da faculdade ganham conta pelo robô (regra do Mauricio, 12/11/2026). */
export const DOMINIO_TURMA = 'minha.fag.edu.br'

export type PedidoConta = { email: string; senha: string; nome: string }

/** Confere o pedido que o robô mandou; devolve o pedido limpo ou o motivo da recusa. */
export function lerPedidoConta(corpo: unknown): PedidoConta | { erro: string } {
  const dados = (corpo && typeof corpo === 'object' ? corpo : {}) as Record<string, unknown>
  const email = typeof dados.email === 'string' ? dados.email.trim().toLowerCase() : ''
  const senha = typeof dados.senha === 'string' ? dados.senha.trim() : ''
  const nome = typeof dados.nome === 'string' ? dados.nome.trim().slice(0, 120) : ''
  const [usuario, dominio, ...resto] = email.split('@')
  if (!usuario || resto.length || !/^[^\s@]+$/.test(usuario)) return { erro: 'E-mail inválido.' }
  if (dominio !== DOMINIO_TURMA) return { erro: `Só e-mails @${DOMINIO_TURMA} ganham conta.` }
  if (!/^\d{6}$/.test(senha)) return { erro: 'A senha precisa ter exatamente 6 números.' }
  return { email, senha, nome }
}

/** Compara a chave do robô sem vazar, pelo tempo de resposta, quantas letras bateram. */
export function chaveConfere(recebida: string, certa: string): boolean {
  if (!certa || recebida.length !== certa.length) return false
  let diferenca = 0
  for (let i = 0; i < certa.length; i++) diferenca |= recebida.charCodeAt(i) ^ certa.charCodeAt(i)
  return diferenca === 0
}
