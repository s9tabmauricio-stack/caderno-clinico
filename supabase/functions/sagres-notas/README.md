# Aviso de notas do Sagres (só do Mauricio)

A cada 30 minutos, das 7h às 23h30 (horário de Brasília), um robô lê as notas e as faltas do Mauricio no Sagres. Se aparecer nota nova, nota mudada ou falta nova, ele manda uma mensagem no WhatsApp do Mauricio. Está no ar desde 14/11/2026.

## Como funciona

1. O relógio do banco (pg_cron, job `sagres-notas`) chama a função `sagres-notas` do Supabase.
2. A função roda em **São Paulo** (`?forceFunctionRegion=sa-east-1`), porque o Sagres bloqueia acesso de fora do Brasil.
3. Ela entra na **API do Sagres**, `https://sagres.fag.edu.br/api/SagresApi`, que é a mesma do app Sagres Mobile. O login vai em "Basic" (usuário e senha), sem captcha. O site do Portal Sagres tem reCAPTCHA e não é usado.
   Caminho até a nota: `/eu`, depois `/diario/periodos-letivos`, depois as turmas do semestre atual. Em cada turma: `avaliacoes` (grupos Teórica/Prática), as avaliações de cada grupo (AV1, AV2…) e `/diario/notas/<id>` (`valor`). As faltas vêm de `resultado.totalFaltas`, ou da lista `faltas`.
4. Ela compara com a última leitura (`public.sagres_estado.ultimo`), manda o WhatsApp pelo **CallMeBot** e guarda a leitura nova.
5. Se algo quebrar (senha mudou, CallMeBot fora do ar), manda **um** aviso e grava o motivo em `sagres_estado.erro`. Quando volta a funcionar, avisa de novo.

## Segredos

Ficam em Supabase → Edge Functions → Secrets e quem põe é o Mauricio: `SAGRES_USUARIO`, `SAGRES_SENHA`, `WHATSAPP_NUMERO` (55 + DDD + número, só números) e `CALLMEBOT_APIKEY`.
Mudou a senha do Sagres? Troque `SAGRES_SENHA` lá. O próximo ciclo já usa a nova.

## Tranca

A função só responde a quem manda o cabeçalho `x-gatilho` igual a `sagres_estado.gatilho`. O relógio lê esse valor do banco, e ninguém mais o vê. A tabela não é lida pelo app, só pela chave secreta.

## Mexer

- Código: `index.ts` nesta pasta, publicado pelo conector do Supabase (`deploy_edge_function`, `verify_jwt: true`). Ele roda no Deno e por isso fica fora do `tsconfig.json`.
- Conferir sem mandar mensagem: chame a função com `?ler=1`. Forçar um resumo no WhatsApp: `?testar=1`.
- Ver se está rodando: `select lido_em, mudou_em, erro from public.sagres_estado;` e `select * from net._http_response order by id desc limit 5;`.
- Pausar: `select cron.alter_job((select jobid from cron.job where jobname = 'sagres-notas'), active := false);` (`true` volta).
