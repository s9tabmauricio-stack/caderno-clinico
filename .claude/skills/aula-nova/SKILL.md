---
name: aula-nova
description: Produção automática de uma aula do Med Genius a partir do áudio. Use quando o Mauricio mandar o áudio de uma aula ("aula nova", "segue o áudio da aula de hoje"): transcreve, faz a apostila, publica, faz flashcards e questões, revisa e põe tudo no ar sem perguntar nada.
---

# Aula nova: do áudio ao site, sem o Mauricio encostar

Regra do Mauricio (31/10/2026): ele manda o áudio e não aprova nada no meio. Não pergunte; decida pelo manual (`AGENTS.md`) e pelas regras abaixo, e deixe as dúvidas para o relatório final. Só pare se faltar algo impossível de contornar (sem áudio, áudio sem fala) e diga o porquê.

Pasta de trabalho: `rascunhos/aulas/<aula-id>/` (fora do Git). Enquanto não souber o id, use `rascunhos/aulas/<AAAA-MM-DD>/` e renomeie depois.

## 1. Achar o áudio e o dia da aula

- O áudio vem anexado na conversa. Ache o arquivo: `find / -xdev \( -path /proc -o -path /sys -o -path '*/node_modules' -o -path /root/.cache \) -prune -o -type f \( -iname '*.m4a' -o -iname '*.mp3' -o -iname '*.wav' -o -iname '*.aac' -o -iname '*.ogg' -o -iname '*.opus' -o -iname '*.webm' -o -iname '*.mp4' -o -iname '*.amr' -o -iname '*.3gp' \) -mmin -600 -print 2>/dev/null`. No Windows, procure só na pasta do usuário (no Git Bash: `find ~ \( -path '*/node_modules' -o -path '*/AppData/Local/Temp' -o -path '*/.cache' \) -prune -o -type f \( …mesmas extensões… \) -mmin -600 -print 2>/dev/null`). Copie para a pasta de trabalho. Se vierem vários, cada um é uma aula (ou partes da mesma, se ele disser).
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

## 4. Apostila

Chame o agente `apostila` no modelo Opus com esforço extra-alto (regra do Mauricio: na chamada, `model: opus` e `effort: xhigh`, que já são o padrão do agente) com: caminho da transcrição, id da aula, disciplina, número, data, professor e a pasta de trabalho. Ele devolve título, resumo, número de páginas, professor e o que vale conferir.

## 5. Publicar a apostila (escondida)

1. `scripts/publicar-apostila.sh rascunhos/aulas/<aula-id>/apostila.pdf <aula-id>` (devolve o número de páginas).
2. Inclua a aula pelo conector com o SQL de "Como subir uma apostila" do `AGENTS.md`, mas com `publicada = false` (a turma ainda não vê). Use a altura real das páginas no `height` (`python3 -I -c "from PIL import Image; print(Image.open('public/apostilas/<aula-id>/01.webp').size)"`).
3. Se a `descricao` da matéria não citar o professor, acrescente o nome dele.
4. Commit `Apostila <Matéria> <N>: <tema> (<P> páginas)` e publique no `main` (regra do manual: `git fetch origin main && git rebase origin/main && git push origin HEAD:main`; depois empurre também o ramo da sessão).
5. Espere a Vercel: repita `curl -s -o /dev/null -w '%{http_code}' https://medgenius.vercel.app/apostilas/<aula-id>/01.webp` (com a ferramenta Monitor) até dar 200.

## 6. Flashcards e questões (ao mesmo tempo)

Chame, em paralelo, o agente `flashcards` ("prepare os flashcards da `<aula-id>`") e o agente `questoes` ("prepare as questões da `<aula-id>`").

## 7. Revisão

Chame o agente `revisor` para a `<aula-id>`. Ele corrige ou tira o que não bate com a apostila e completa o que faltar. É ele quem aprova no lugar do Mauricio.

## 8. Gravar e pôr no ar

1. Em paralelo: agente `flashcards` ("inclua o rascunho aprovado da `<aula-id>`") e agente `questoes` ("inclua o rascunho revisado da `<aula-id>`").
2. Confira as contagens e então: `update public.aulas set publicada = true where id = '<aula-id>';`
3. Atualize no `AGENTS.md` a lista de "Pendências e ideias" (cards e questões da aula nova), commit e publique no `main` como no passo 5.
4. Apague o áudio, o `.log` e os arquivos temporários; deixe a transcrição e os rascunhos na pasta de trabalho (servem para refazer sem transcrever de novo, enquanto a sessão durar).

## 9. Relatório (curto, no chat)

- Uma linha: "<Matéria> <N> — <título> no ar: apostila de P páginas, X flashcards (Y de PROVA), Z questões."
- Como a aula foi identificada (agenda/transcrição) e qualquer divergência.
- O que vale conferir: dúvidas da apostila, itens que o revisor tirou e por quê, professor fora da tabela.
- Quanto tempo levou a transcrição e o que não foi testado.
- Envie o PDF da apostila com SendUserFile.

Se algo falhar no meio, a aula continua escondida (`publicada = false`): diga onde parou e o que falta. Nada fica pela metade na frente da turma.
