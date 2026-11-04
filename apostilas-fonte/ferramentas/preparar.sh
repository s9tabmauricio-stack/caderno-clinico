#!/usr/bin/env bash
# Prepara uma pasta de trabalho para gerar uma apostila (vale para Claude, Antigravity e Codex).
# Uso: apostilas-fonte/ferramentas/preparar.sh <pasta-de-trabalho>
#
# 1. instala o WeasyPrint e o pdfplumber, se faltarem;
# 2. instala a fonte Inter (Regular, Medium, SemiBold, Bold) que está aqui em fonts/,
#    se ela ainda não estiver no computador (sem internet);
# 3. copia para a pasta o apostila.css oficial (apostilas-fonte/apostila.css),
#    o render.py e o checar.py.
# Nunca redigite nem edite esses três arquivos na pasta: o original é o daqui.
set -euo pipefail
destino="${1:?diga a pasta de trabalho. Ex.: apostilas-fonte/ferramentas/preparar.sh rascunhos/aulas/gastro-a4}"
aqui="$(cd "$(dirname "$0")" && pwd)"
py="$(command -v python3 || command -v python)"

if ! "$py" -c "import weasyprint, pdfplumber, PIL, fontTools" 2>/dev/null; then
  "$py" -m pip install -q -r "$aqui/requirements.txt" 2>/dev/null \
    || "$py" -m pip install -q --break-system-packages -r "$aqui/requirements.txt"
fi

if command -v fc-list >/dev/null && ! fc-list : family | grep -q "Inter SemiBold"; then
  mkdir -p "$HOME/.fonts"
  cp "$aqui"/fonts/Inter-*.ttf "$HOME/.fonts/"
  fc-cache -f >/dev/null
  echo "fonte Inter instalada em ~/.fonts"
fi

mkdir -p "$destino"
cp "$aqui/../apostila.css" "$aqui/render.py" "$aqui/checar.py" "$destino/"
cp -r "$aqui/fonts" "$destino/"
echo "pronto em $destino: apostila.css, render.py, checar.py e fonts/"
echo "fonte para medir texto nos SVGs (PIL): $aqui/fonts/Inter-Regular.ttf (e -Medium, -SemiBold, -Bold)"
