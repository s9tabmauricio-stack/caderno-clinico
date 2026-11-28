// Imagens das questões (28/11/2026): converte para WebP, envia para o espaço público "questoes" do Supabase
// Storage e grava os caminhos em questoes.imagens. Usado pelo imagem-questao.mjs e pelo gravar-rascunho.mjs.
import { existsSync, readFileSync } from 'node:fs'
import { isAbsolute, join } from 'node:path'

export const ESPACO = 'questoes'

/** Pasta da questão no Storage: a aula ('neuro29-a1-q05' → 'neuro29-a1'); questão sem aula, a matéria. */
export function pastaDaQuestao(questaoId) {
  const aula = /^([a-z0-9]+-a\d+)-/.exec(questaoId)
  return aula ? aula[1] : questaoId.split('-')[0]
}

/** Caminho no Storage da n-ésima imagem (1, 2…): 'neuro29-a1/neuro29-a1-q05-1.webp'. */
export function caminhoImagem(questaoId, n) {
  return `${pastaDaQuestao(questaoId)}/${questaoId}-${n}.webp`
}

/** Acha o arquivo: como foi escrito, ou dentro de apostilas-fonte/<aula>/ (onde fica o material da aula). */
export function acharArquivo(arquivo, aulaId) {
  const candidatos = isAbsolute(arquivo) ? [arquivo] : [arquivo, ...(aulaId ? [join('apostilas-fonte', aulaId, arquivo)] : [])]
  return candidatos.find((c) => existsSync(c)) ?? null
}

/** PNG, JPG ou WebP → WebP de até 1600 px de largura (sem aumentar as pequenas). */
export async function paraWebp(arquivo) {
  const { default: sharp } = await import('sharp')
  return sharp(readFileSync(arquivo)).rotate().resize({ width: 1600, withoutEnlargement: true }).webp({ quality: 82 }).toBuffer()
}

/**
 * Envia as imagens de uma questão e grava os caminhos.
 * trocar = true: substitui as que a questão já tinha; senão, acrescenta depois delas.
 */
export async function enviarImagens(db, questaoId, arquivos, { trocar = false } = {}) {
  const { data: q, error } = await db.from('questoes').select('id, imagens').eq('id', questaoId).maybeSingle()
  if (error) throw new Error(`ler a questão ${questaoId}: ${error.message}`)
  if (!q) throw new Error(`a questão ${questaoId} não existe no banco.`)
  const antes = trocar ? [] : (q.imagens ?? [])
  const novos = []
  for (const [i, arquivo] of arquivos.entries()) {
    const caminho = caminhoImagem(questaoId, antes.length + i + 1)
    const { error: e } = await db.storage.from(ESPACO).upload(caminho, await paraWebp(arquivo), { contentType: 'image/webp', upsert: true })
    if (e) throw new Error(`enviar ${arquivo}: ${e.message}`)
    novos.push(caminho)
  }
  const imagens = [...antes, ...novos]
  const { error: e2 } = await db.from('questoes').update({ imagens }).eq('id', questaoId)
  if (e2) throw new Error(`gravar as imagens de ${questaoId}: ${e2.message}`)
  return imagens
}
