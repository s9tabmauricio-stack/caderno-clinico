#!/usr/bin/env node
// Põe imagem numa questão que já está no banco (ECG, raio X, foto…). A maioria das questões não tem.
//
// Uso:
//   node scripts/imagem-questao.mjs <questao-id> <arquivo> [<arquivo>…]   acrescenta (na ordem)
//   node scripts/imagem-questao.mjs <questao-id> <arquivo> --trocar        substitui as que ela tinha
//   node scripts/imagem-questao.mjs <questao-id> --tirar                   tira as imagens da questão
//
// O arquivo pode estar em qualquer lugar ou dentro de apostilas-fonte/<aula>/. Vira WebP e vai para o
// espaço público "questoes" do Supabase Storage. Precisa de SUPABASE_SECRET_KEY (ambiente ou .env.local).
// Questão corrigida (-v2): ponha a imagem na versão nova (o gravar-rascunho e a correção não copiam sozinhos).
import { acharArquivo, enviarImagens, pastaDaQuestao } from './imagens-questoes.mjs'

const URL_PADRAO = 'https://xtlpmtylifbalzxnfkib.supabase.co' // igual a lib/supabase/config.ts
const args = process.argv.slice(2)
const parar = (msg) => { console.error('PAROU: ' + msg); process.exit(1) }
const [questaoId, ...resto] = args.filter((a) => !a.startsWith('--'))
if (!questaoId) parar('diga o id da questão. Ex.: node scripts/imagem-questao.mjs neuro29-a1-q05 ecg.png')
const tirar = args.includes('--tirar')
if (!tirar && !resto.length) parar('diga o arquivo da imagem (ou --tirar).')

const aula = /^[a-z0-9]+-a\d+$/.test(pastaDaQuestao(questaoId)) ? pastaDaQuestao(questaoId) : null
const arquivos = resto.map((a) => acharArquivo(a, aula) ?? parar(`não achei o arquivo ${a}.`))

try { process.loadEnvFile('.env.local') } catch { /* sem .env.local: usa o ambiente */ }
const chave = process.env.SUPABASE_SECRET_KEY
if (!chave) parar('falta a chave SUPABASE_SECRET_KEY no ambiente (ou em .env.local).')
const { createClient } = await import('@supabase/supabase-js')
const db = createClient(process.env.NEXT_PUBLIC_SUPABASE_URL ?? URL_PADRAO, chave, { auth: { persistSession: false, autoRefreshToken: false } })

try {
  if (tirar) {
    const { error } = await db.from('questoes').update({ imagens: [] }).eq('id', questaoId)
    if (error) parar(error.message)
    console.log(`${questaoId}: imagens tiradas (os arquivos continuam no Storage).`)
  } else {
    const imagens = await enviarImagens(db, questaoId, arquivos, { trocar: args.includes('--trocar') })
    console.log(`${questaoId}: ${imagens.length} ${imagens.length === 1 ? 'imagem' : 'imagens'} (${imagens.join(', ')}).`)
  }
} catch (e) {
  parar(e.message)
}
