# Windows: roda o scripts/transcrever.py desligado da conversa (no lugar do "nohup setsid" do Linux).
# Uso: powershell -NoProfile -ExecutionPolicy Bypass -File scripts/transcrever-fundo.ps1 <audio> <pasta> "<prompt>"
# Grava <pasta>/transcricao.txt no fim e o progresso em <pasta>/transcricao.log; mostra o número do processo.
param([Parameter(Mandatory)] [string]$Audio, [Parameter(Mandatory)] [string]$Pasta, [string]$Prompt = 'Aula de Medicina em português do Brasil.')
$ErrorActionPreference = 'Stop'
New-Item -ItemType Directory -Force $Pasta | Out-Null
$script = Join-Path $PSScriptRoot 'transcrever.py'
$saida = Join-Path (Resolve-Path $Pasta) 'transcricao.txt'
$p = Start-Process -FilePath 'python3' -WindowStyle Hidden -PassThru `
    -ArgumentList @('-I', "`"$script`"", "`"$((Resolve-Path $Audio).Path)`"", "`"$saida`"", '--prompt', "`"$Prompt`"") `
    -RedirectStandardError (Join-Path $Pasta 'transcricao.log') -RedirectStandardOutput (Join-Path $Pasta 'transcricao.out')
"transcrição rodando no processo $($p.Id)"
