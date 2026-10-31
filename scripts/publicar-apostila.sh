#!/usr/bin/env bash
# Prepara as páginas de uma apostila para o site (o jeito aprovado do manual).
# Uso: scripts/publicar-apostila.sh <arquivo.pdf> <aula-id>
# Gera public/apostilas/<aula-id>/01.webp, 02.webp… (1400 px, qualidade 78) e
# copia o PDF como apostila.pdf. No fim, mostra o número de páginas.
set -euo pipefail
pdf="$1"; aula="$2"
destino="public/apostilas/$aula"
mkdir -p "$destino"
tmp="$(mktemp -d)"
pdftoppm -scale-to-x 1400 -scale-to-y -1 -jpeg -jpegopt quality=80 "$pdf" "$tmp/p"
python3 -I - "$tmp" "$destino" <<'EOF'
import sys, pathlib
from PIL import Image
tmp, destino = map(pathlib.Path, sys.argv[1:])
paginas = sorted(tmp.glob('p-*.jpg'), key=lambda p: int(p.stem.split('-')[-1]))
for i, jpg in enumerate(paginas, 1):
    Image.open(jpg).save(destino / f'{i:02d}.webp', 'WEBP', quality=78)
print(len(paginas))
EOF
rm -rf "$tmp"
cp "$pdf" "$destino/apostila.pdf"
