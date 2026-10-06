# Caderno Clínico

Site de estudos com apostila, banco de questões e flashcards de cada aula. Cada aluno entra com um link enviado por e-mail e o progresso fica salvo no Supabase.

## Como está montado

| Parte | Onde fica |
|---|---|
| Telas | `app/` (Next.js 16, App Router) e `components/` |
| Login e sessão | `lib/supabase/` e `proxy.ts` (renova a sessão e protege as páginas) |
| Leitura dos dados | `lib/dados.ts` |
| Repetição espaçada dos flashcards | `lib/srs.ts` |
| Banco de dados | `supabase/migrations/` (tudo o que já foi aplicado no projeto `caderno-clinico`) |

### Tabelas

- **Conteúdo:** `materias`, `aulas` (com `apostila_html` e `pdf_caminho`), `questoes` (banco de questões da matéria, com aula opcional), `flashcards`
- **Progresso de cada aluno:** `respostas` (última resposta de cada questão) e `revisoes` (estado de cada flashcard)
- **Alunos:** `perfis`, criado sozinho no primeiro login
- **Visões prontas para as telas:** `progresso_aulas`, `progresso_materias`, `progresso_temas`, `questoes_do_aluno`, `flashcards_do_aluno`

As regras de segurança (RLS) garantem que cada aluno só vê e altera o próprio progresso, e que ninguém altera o conteúdo pelo site.

## Rodar no computador

Precisa do Node.js 20.9 ou mais novo.

```bash
npm install
npm run dev
```

Abra http://localhost:3000. O endereço e a chave pública do Supabase já estão em `lib/supabase/config.ts`; para usar outro projeto, copie `.env.example` para `.env.local` e preencha.

## Publicar na Vercel

1. Suba esta pasta para um repositório no GitHub.
2. Na Vercel, clique em **Add New → Project**, escolha o repositório e clique em **Deploy**. Não precisa configurar nada.
3. No Supabase, em **Authentication → URL Configuration**:
   - **Site URL:** o endereço que a Vercel deu (por exemplo `https://caderno-clinico.vercel.app`)
   - **Redirect URLs:** adicione `https://SEU-ENDERECO/auth/callback` e `http://localhost:3000/auth/callback`

## Antes de abrir para os alunos

O envio de e-mails que vem com o Supabase só entrega para os e-mails da equipe do projeto e tem limite baixo por hora. Para os alunos receberem o link:

1. Crie uma conta num serviço de e-mail (por exemplo Resend, que tem plano gratuito).
2. No Supabase, em **Authentication → Emails → SMTP Settings**, preencha os dados desse serviço.

Opcional: para o link funcionar mesmo quando o aluno abre o e-mail em outro aparelho, troque o modelo **Magic Link** (Authentication → Emails) para apontar para:

```
{{ .SiteURL }}/auth/confirm?token_hash={{ .TokenHash }}&type=email
```

### Login com Google (opcional)

Depois de ativar o Google em **Authentication → Sign In / Providers** no Supabase, defina a variável `NEXT_PUBLIC_LOGIN_GOOGLE=1` na Vercel. O botão "Continuar com Google" aparece na tela de entrada.

## Adicionar conteúdo

Por enquanto, pelo **Table Editor** do Supabase:

1. `materias`: uma linha por matéria (`id` curto, como `cardio`).
2. `aulas`: `materia_id`, `ordem`, `titulo`, `resumo` e `apostila_html`.
3. `questoes`: toda questão pertence a uma matéria (`materia_id`) e entra no banco de questões dela. Se o assunto for de uma aula, preencha também `aula_id` para ela aparecer na aba Questões da aula. `alternativas` é uma lista, como `["A", "B", "C", "D"]`, e `correta` é a posição da certa (0 = A). Opcionais: `tema` e `prova` (viram filtros), `fonte` (ex.: "P2 T19 · nº 1"), `comentario` e `por_que_erradas`.
4. `flashcards`: `frente` e `verso`.

Para o PDF da apostila, envie o arquivo em **Storage → apostilas** e coloque o caminho (por exemplo `nefro/lesao-renal-aguda.pdf`) no campo `pdf_caminho` da aula.
