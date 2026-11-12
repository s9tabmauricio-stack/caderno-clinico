# Robô do Gmail: contas criadas sozinhas

Quem quer entrar no Med Genius manda um e-mail para o Mauricio:

- **de:** o e-mail da faculdade (`@minha.fag.edu.br`; de outro endereço, o robô ignora);
- **assunto:** `Acesso Med Genius`;
- **texto:** só a senha que a pessoa quer, com **6 números**.

A cada 5 minutos, o robô (um Google Apps Script na conta do Mauricio) acha esses e-mails e pede ao site para criar a conta. O **login é o próprio e-mail da pessoa** e a senha são os 6 números. A conta nasce igual às criadas em Configurações → Alunos (confirmada, 1 aparelho). O robô responde à pessoa ("conta pronta", "já existe conta" ou "faltou a senha"), põe a conversa na etiqueta **Med Genius/Contas** e manda o e-mail com a senha para a lixeira.

- Código do robô: [`Codigo.gs`](Codigo.gs) (esta é a cópia guardada no projeto; mudou lá, copie para cá).
- No site: `app/api/contas-gmail/route.ts`, que só atende quem manda a chave `ROBO_GMAIL_CHAVE`. As regras (só `@minha.fag.edu.br`, senha de 6 números) estão em `lib/contas-gmail.ts`.
- O robô nunca troca a senha de uma conta que já existe.

## Instalar (uma vez, uns 10 minutos)

1. No computador, entre em https://script.google.com com a conta **s9tabmauricio@gmail.com** (a que recebe os e-mails) e clique em **Novo projeto**.
2. Dê o nome **Robô Med Genius** (clicando em "Projeto sem título", no alto).
3. Apague o que estiver escrito e cole todo o conteúdo de `Codigo.gs`. Clique no disquete (**Salvar**).
4. No alto, escolha a função **gerarChave** e clique em **Executar**. O Google pede autorização: **Revisar permissões** → escolha a conta → **Avançado** → **Acessar Robô Med Genius (não seguro)** → **Permitir**. (O aviso aparece porque o robô é seu e não foi publicado; ele lê o Gmail e acessa o site.)
5. Embaixo, no **Registro de execução**, aparece "Copie esta chave…" seguida de letras e números. Copie só a chave.
6. Na Vercel: projeto do Med Genius → **Settings** → **Environment Variables** → **Add**. Nome `ROBO_GMAIL_CHAVE`, valor a chave copiada, ambiente **Production**. Salve.
7. Ainda na Vercel: **Deployments** → no primeiro da lista, os três pontinhos → **Redeploy** (a chave só vale depois disso).
8. Volte ao script, escolha a função **ligarRobo** e clique em **Executar**. Pronto: está ligado.

## Testar

Peça a alguém da turma (ou use o seu e-mail da FAG) para mandar o e-mail com assunto `Acesso Med Genius` e 6 números no texto. Em até 5 minutos chega a resposta "Sua conta no Med Genius está pronta!" e a conta aparece em Configurações → Alunos.

## Se der problema

- **Ninguém recebe resposta:** no script, menu da esquerda → **Execuções**, veja o erro. "Erro 401" = a chave da Vercel não é a mesma do robô (refaça os passos 4 a 7). "Erro 503" = faltou a chave na Vercel ou o Redeploy.
- **Desligar o robô:** no script, escolha **desligarRobo** e clique em **Executar**.
- **Trocar a chave** (se vazou): rode **gerarChave** de novo e refaça os passos 6 e 7.
- O Google manda um e-mail ao Mauricio quando o robô falha várias vezes seguidas.
