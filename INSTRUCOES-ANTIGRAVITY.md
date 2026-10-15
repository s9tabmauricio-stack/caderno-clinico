# Instruções para o assistente (Antigravity) — Med Genius

Você vai trabalhar comigo no Med Genius, o app de estudos da minha turma de Medicina (FAG).
Eu não sou programador: explique tudo em português do Brasil, em linguagem simples, e diga em uma ou duas frases o que mudou.

## 1) Leia primeiro

- Abra e leia por inteiro o `CLAUDE.md` e o `AGENTS.md` na raiz do projeto. Eles são o manual: onde fica cada coisa, banco de dados, como subir apostilas, como cadastrar questões, regras da agenda e do visual.
- Antes de começar qualquer tarefa, me resuma em poucas linhas as regras que você entendeu.
- O Next.js deste projeto é uma versão nova, com mudanças em relação ao que você conhece. Antes de escrever código, leia o guia certo em `node_modules/next/dist/docs/`.

## 2) O que você pode fazer (o mesmo que o outro assistente faz)

- Mudar telas e funcionalidades do app.
- Subir apostilas novas (PDF → imagens `.webp` em `public/apostilas/<aula-id>/`, PDF copiado, commit e push, e só depois incluir a aula no banco), exatamente como está no `CLAUDE.md`.
- Incluir questões e flashcards no banco, seguindo o formato do `CLAUDE.md` (alternativas, gabarito como índice 0–4, `comentario`, `por_que_erradas`, `origem`).
- Corrigir questões criando uma versão nova (`<id>-v2`, mesma ordem), marcando a antiga com `substituida_por` e levando os recados junto. Nunca apague nem reescreva texto longo direto; eu limpo depois em Conteúdo → Limpeza.
- Quando a prova não tiver gabarito: resolva com base na apostila da aula, marque como não oficial e discuta as duvidosas comigo, uma por uma, mostrando o texto completo da questão antes de pedir decisão.

## 3) Regras que nunca se quebram

- Nunca mude o domínio de login (`DOMINIO_LOGIN` em `lib/cpf.ts`). As contas dependem dele.
- Nunca peça nem digite senhas ou chaves. Eu mesmo crio contas e configuro chaves.
- Não mexa no banco além do que a tarefa pede. Nada de apagar tabelas, dados de alunos ou migrações sem eu autorizar.
- O que for substituído deve poder ser limpo depois (sem deixar lixo).
- Eu sou sensível a custo: prefira o caminho barato (converter arquivos em vez de reescrever conteúdo; não reenviar textos grandes à toa).
- Mostre o conteúdo (a questão, a tela) antes de me pedir uma decisão. Um assunto por vez.

## 4) Como conviver com o outro assistente (Claude)

- Podemos estar trabalhando ao mesmo tempo. Trabalhe sempre em um ramo (branch) seu, com nome começando por `antigravity/`. Nunca mande direto para o ramo `main` sem eu pedir.
- Só o `main` publica o site (a Vercel publica sozinha em 1–2 minutos). Quando uma mudança estiver pronta, me diga e eu autorizo juntar ao `main`.
- Antes de começar, atualize seu ramo com o que há de mais novo no `main` para não atropelar o trabalho do outro.
- Se for mexer em algo que o outro pode estar mexendo (a mesma tela, o mesmo arquivo), me avise antes.
- Ao terminar, diga claramente o que foi testado e o que NÃO foi testado.
