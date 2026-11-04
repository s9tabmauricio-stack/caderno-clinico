# No computador Windows do Mauricio (desde 31/10/2026)

Lido só quando o trabalho é no PC dele (aula nova, transcrição). Na nuvem não precisa.


O PC (Windows 11, Ryzen 5 8600G, 24 GB, sem placa de vídeo NVIDIA) já tem tudo o que a receita usa: Git, ffmpeg e Poppler (`winget`), Python 3.12 com faster-whisper (modelo large-v3 já baixado), Pillow, pdfplumber e WeasyPrint, a fonte Inter (Regular, Medium, SemiBold e Bold, em `~/.fonts` e instalada no Windows) e o `gh` com login feito.
- `python3` funciona (cópia do `python.exe` em `...\Python312\python3.exe`); os comandos `python3 -I ...` do manual valem como estão.
- O WeasyPrint usa o Pango do MSYS2 (`C:\msys64\mingw64\bin`, na variável `WEASYPRINT_DLL_DIRECTORIES`). Na skill `apostila-padrao`, o bloco "Ambiente" não precisa instalar nada. Desde 03/11/2026, a skill mora no projeto (`.claude/skills/apostila-padrao/SKILL.md`), não mais na conta do Claude; mudanças no padrão vão direto nesse arquivo.
- Transcrição em segundo plano: `scripts/transcrever-fundo.ps1` (no lugar do `nohup setsid`). Velocidade medida em 31/10/2026: 6 min de áudio em 2 min (cerca de 1/3 do tempo do áudio), então uma aula de 2 h leva perto de 45 min a 1 h 15. Limitar a 6 núcleos (`cpu_threads`) quase não muda. `scripts/publicar-apostila.sh` roda no Git Bash.
- Caminhos longos: o Windows corta caminhos com mais de 260 letras. O repositório usa `core.longpaths = true`; prefira pastas de trabalho curtas.
