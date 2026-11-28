import test from 'node:test'
import assert from 'node:assert/strict'
import { lerQuestoes } from '../scripts/rascunho.mjs'
import { caminhoImagem, pastaDaQuestao } from '../scripts/imagens-questoes.mjs'

const RASCUNHO = `## 01 · Neuro

### 1 · tema: AVC
Veja a tomografia.
- A) Isquêmico
- B*) Hemorrágico
- C) Tumor
- D) Abscesso
- E) Normal

**Comentário:** Hiperdensidade.
**Por que as erradas:**
A, C, D e E: não.
**Imagem:** tc-q01.png
**Imagem:** \`tc-q01-corte2.jpg\`

### 2 · tema: Cefaleia
Sem imagem.
- A*) Enxaqueca
- B) Tensional
- C) Salvas
- D) HSA
- E) Sinusite

**Comentário:** Pulsátil.
**Por que as erradas:**
B, C, D e E: não.
`

test('linha **Imagem:** vira a lista de imagens, na ordem; questão sem a linha fica sem', () => {
  const [q1, q2] = lerQuestoes(RASCUNHO)
  assert.deepEqual(q1.imagens, ['tc-q01.png', 'tc-q01-corte2.jpg'])
  assert.equal(q1.por_que_erradas, 'A, C, D e E: não.')
  assert.equal(q2.imagens, undefined)
})

test('caminho no Storage: pasta da aula e número da imagem', () => {
  assert.equal(pastaDaQuestao('neuro29-a1-q05'), 'neuro29-a1')
  assert.equal(pastaDaQuestao('neuro29-a1-q05-v2'), 'neuro29-a1')
  assert.equal(caminhoImagem('neuro29-a1-q05', 2), 'neuro29-a1/neuro29-a1-q05-2.webp')
  assert.equal(pastaDaQuestao('nf-t19-q03'), 'nf')
})

