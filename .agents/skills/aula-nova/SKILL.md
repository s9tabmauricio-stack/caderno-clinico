---
name: aula-nova
description: Produção automática de uma aula do Med Genius a partir do áudio ou da transcrição. Use quando o Mauricio mandar o áudio de uma aula ("aula nova", "segue o áudio da aula de hoje"), ou a transcrição e os slides pedindo para fazer a aula: transcreve, guarda a fonte da aula, faz a apostila, publica, faz flashcards e questões, revisa e põe tudo no ar sem perguntar nada.
---

# Aula nova: do áudio ao site, sem o Mauricio encostar

Regra do Mauricio (31/10/2026): ele manda o áudio (ou a transcrição e os slides) e não aprova nada no meio. Não pergunte; decida pelo manual (`AGENTS.md`) e pelas regras abaixo, e deixe as dúvidas para o relatório final. Só pare se faltar algo impossível de contornar (sem áudio nem transcrição, áudio sem fala) e diga o porquê.

**Fonte da aula** (regra do Mauricio, 09/11/2026): a transcrição e os slides viram o arquivo fonte da aula (`apostilas-fonte/<aula-id>/fonte.md`, passo 4), e tudo o que vem depois (apostila, flashcards, questões, revisão) sai dele e é conferido contra ele.

**Economia (regra do Mauricio, 31/10/2026):** uma chamada de agente por etapa, só as desta receita. Não acrescente agentes, workflows, conferências nem correções extras, nem com o modo ultracode ligado. A conversa principal não relê a transcrição, a apostila nem os rascunhos: trabalha com o resumo que cada agente devolve. Enquanto um agente trabalha, espere o aviso de que terminou, sem ficar checando. Etapas mecânicas (fila, publicar imagens, gravar no banco, relatório) ficam na conversa principal, sem agente: não precisam do Opus (regra do Mauricio, 04/11/2026). Os agentes de escrever e revisar continuam no Opus com esforço extra-alto.

**Antigravity e Codex** seguem a mesma receita: onde ela diz "chame o agente X", leia `.claude/agents/X.md` e faça o que ele manda, na mesma ordem; onde diz Monitor, espere conferindo o `.log` de tempos em tempos (`tail -n 3 <arquivo>.log`); onde diz SendUserFile, diga o caminho do PDF. O Codex não tem o conector do Supabase: onde a receita usa o conector, ele roda o mesmo SQL com `node scripts/sql.mjs "<SQL>"` ([`docs/codex.md`](../../../docs/codex.md)); se o programa disser que o ambiente não está configurado, ele faz o que não depende do banco e para dizendo onde parou.

**Fila** (`docs/fila.md`): assim que souber o id da aula, anote a linha ("Aula nova", a aula, a matéria) como diz o topo do arquivo; no último commit da publicação, apague a linha.

Pasta de trabalho: `rascunhos/aulas/<aula-id>/` (fora do Git). Enquanto não souber o id, use `rascunhos/aulas/<AAAA-MM-DD>/` e renomeie depois.

## 1. Achar o áudio e o dia da aula

- O áudio vem anexado na conversa. Ache o arquivo: `find / -xdev \( -path /proc -o -path /sys -o -path '*/node_modules' -o -path /root/.cache \) -prune -o -type f \( -iname '*.m4a' -o -iname '*.mp3' -o -iname '*.wav' -o -iname '*.aac' -o -iname '*.ogg' -o -iname '*.opus' -o -iname '*.webm' -o -iname '*.mp4' -o -iname '*.amr' -o -iname '*.3gp' \) -mmin -600 -print 2>/dev/null`. No Windows, procure só na pasta do usuário (no Git Bash: `find ~ \( -path '*/node_modules' -o -path '*/AppData/Local/Temp' -o -path '*/.cache' \) -prune -o -type f \( …mesmas extensões… \) -mmin -600 -print 2>/dev/null`). Copie para a pasta de trabalho. Se vierem vários, cada um é uma aula (ou partes da mesma, se ele disser).
- **Veio a transcrição em vez do áudio** (arquivo `.txt`, `.docx`, `.pdf`, `.srt`, ou texto colado): pule o passo 2. Copie o arquivo (ou salve o texto colado) como `rascunhos/aulas/<pasta>/transcricao.txt` (`.docx` e `.pdf` ficam com a extensão deles). Ache os anexos como o áudio, com as extensões `.txt`, `.docx`, `.pdf`, `.srt`, `.vtt`, `.pptx`.
- **Slides** (`.pdf` ou `.pptx`), venham com o áudio ou com a transcrição: copie para a pasta de trabalho. Eles entram na fonte no passo 4.
- Dia e hora da gravação, nesta ordem de confiança: o que o Mauricio escreveu na mensagem; `ffprobe -v error -show_entries format_tags=creation_time:format=duration -of default=nw=1 <audio>` (o horário vem em UTC: Cascavel é UTC−3); o nome do arquivo; senão, a teórica mais recente antes de agora.

## 2. Transcrever (grátis, Whisper large-v3, nesta máquina)

Rode desligado da conversa, porque demora horas e o limite de um comando em segundo plano é 2 h:

```bash
mkdir -p rascunhos/aulas/<pasta> && nohup setsid python3 -I scripts/transcrever.py <audio> rascunhos/aulas/<pasta>/transcricao.txt --prompt "<prompt>" > rascunhos/aulas/<pasta>/transcricao.log 2>&1 &
```

No Windows (não há `setsid`), rode pelo PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/transcrever-fundo.ps1 <audio> rascunhos/aulas/<pasta> "<prompt>"
```

- `<prompt>`: "Aula de <disciplina> do curso de Medicina, em português do Brasil." mais uns 10 termos técnicos prováveis do tema (ajuda o Whisper a acertar os nomes).
- Espere com a ferramenta Monitor até o arquivo `transcricao.txt` existir (o `.log` mostra o progresso). Não pare a conversa esperando.
- Enquanto isso, faça o passo 3.

## 3. Identificar a aula pela Agenda (no lugar das quatro perguntas)

```sql
select data, inicio, fim, materia, tipo, titulo, professor, cancelado from public.agenda_eventos
where data = '<dia>' and tipo in ('teorica', 'pratica') order by inicio;
```

- Escolha a aula cujo horário contém (ou fica mais perto de) o início da gravação; teórica vence prática no mesmo horário. A duração do áudio ajuda a desempatar.
- Confirme pelo começo da transcrição (tema, nome do professor). Se a transcrição contradisser a agenda, vale a transcrição, e isso vai para o relatório.
- Matéria = `materia` da agenda (`nefro`, `pneumo`, `gastro`, `orto`, `uro`, `pass`, `angio`); disciplina = `materias.nome` (no caso de PASS e PROEX, siga a tabela da skill `apostila-padrao`). Professor = o da agenda.
- Número da aula e id: `select coalesce(max(ordem), 0) + 1 from public.aulas where materia_id = '<materia>'` → `<materia>-a<N>`. Confira que o id não existe.
- Sem agenda para o dia: deduza a matéria pelo tema da transcrição e diga no relatório.

## 4. Fonte da aula e apostila

Primeiro guarde a fonte, sem agente (mecânico):

```bash
python3 -I scripts/fonte-aula.py guardar <aula-id> --transcricao rascunhos/aulas/<aula-id>/transcricao.txt [--slides <arquivo dos slides>]
```

Ele cria `apostilas-fonte/<aula-id>/fonte.md` (vai para o Git no commit do passo 5). Se a aula já tem fonte, use `--acrescentar`. O arquivo original dos slides não vai para o Git: lembre o Mauricio no relatório de guardar na pasta da aula no Drive (ou guarde, se tiver acesso).

Depois chame o agente `apostila` no modelo Opus com esforço extra-alto (regra do Mauricio: na chamada, `model: opus` e `effort: xhigh`, que já são o padrão do agente) com: a fonte (`apostilas-fonte/<aula-id>/fonte.md`) e o caminho dos slides originais (se o Mauricio mandou, para as imagens), id da aula, disciplina, número, data, professor e a pasta de trabalho. Ele devolve título, resumo, número de páginas, professor e o que vale conferir.

## 5. Publicar a apostila (escondida)

1. `scripts/publicar-apostila.sh rascunhos/aulas/<aula-id>/apostila.pdf <aula-id>` (devolve o número de páginas).
2. Inclua a aula pelo conector com o SQL da skill `subir-apostila` (`.claude/skills/subir-apostila/SKILL.md`), mas com `publicada = false` (a turma ainda não vê). Use a altura real das páginas no `height` (`python3 -I -c "from PIL import Image; print(Image.open('public/apostilas/<aula-id>/01.webp').size)"`).
3. Se a `descricao` da matéria não citar o professor, acrescente o nome dele.
4. Guarde o HTML: copie `apostila.html`, o `mapa.md`, os `*.svg` e os programas das figuras da pasta de trabalho para `apostilas-fonte/<aula-id>/`, onde já está o `fonte.md` (sem o `apostila.css`, que fica na raiz de `apostilas-fonte/`). É o que permite corrigir a apostila depois sem remontá-la do PDF.
5. Commit (com `public/apostilas/<aula-id>/` e `apostilas-fonte/<aula-id>/`) `Apostila <Matéria> <N>: <tema> (<P> páginas)` e publique no `main` (regra do manual: `git fetch origin main && git rebase origin/main && git push origin HEAD:main`; depois empurre também o ramo da sessão).
6. Espere a Vercel: repita `curl -s -o /dev/null -w '%{http_code}' https://medgenius.vercel.app/apostilas/<aula-id>/01.webp` (com a ferramenta Monitor) até dar 200.

## 6. Flashcards e questões (um agente só)

Chame o agente `conteudo` ("prepare os flashcards e as questões da `<aula-id>`"). Ele lê só a fonte da aula, uma vez, e escreve os dois rascunhos a partir dela (a apostila não entra).

## 7. Revisão

Chame o agente `revisor` para a `<aula-id>`. Ele confere contra a fonte da aula, corrige ou tira o que não bate e completa o que faltar. É ele quem aprova no lugar do Mauricio.

## 8. Gravar e pôr no ar

1. Grave sem agente: `node scripts/gravar-rascunho.mjs <aula-id>` (lê os dois rascunhos, grava e confere as contagens). Se parar com `PAROU:` por formato, corrija o rascunho e rode de novo. Sem a chave `SUPABASE_SECRET_KEY`, use o caminho `--sql` descrito no passo "Incluir" de `.claude/agents/flashcards.md` e `questoes.md`.
2. Se as contagens bateram: `update public.aulas set publicada = true where id = '<aula-id>';`
3. Não anote contagens no `AGENTS.md` (regra do manual: conte no banco). Só atualize o manual se a aula trouxer algo que ele precisa saber (matéria nova, id fora do padrão); nesse caso, commit e publique no `main` como no passo 5.
4. Apague o áudio, o `.log` e os arquivos temporários; deixe os rascunhos na pasta de trabalho. A transcrição já está guardada na fonte da aula, no Git: refazer não precisa transcrever de novo.

## 9. Relatório (curto, no chat)

- Uma linha: "<Matéria> <N> — <título> no ar: apostila de P páginas, X flashcards (Y de PROVA), Z questões."
- Como a aula foi identificada (agenda/transcrição) e qualquer divergência.
- O que vale conferir: dúvidas da apostila, itens que o revisor tirou e por quê, professor fora da tabela.
- Quanto tempo levou a transcrição e o que não foi testado.
- Se vieram slides: que o arquivo original vai para a pasta da aula no Drive (o texto já está na fonte).
- Envie o PDF da apostila com SendUserFile.

Se algo falhar no meio, a aula continua escondida (`publicada = false`): diga onde parou e o que falta. Nada fica pela metade na frente da turma.
