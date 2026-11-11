# Embolia pulmonar nas Provas da FAG (apostila pessoal do Mauricio)

Apostila de véspera, feita em 10/11/2026 a pedido do Mauricio: só o que é preciso para acertar as 15 questões
das Provas da FAG da aula `pneumo-a1` (no banco: `prova` igual a `p2`, `p2-t23`, `p2-t26`, `p2-t28` ou `exame`).
Sai da fonte da aula (`../fonte.md`); o que não foi dito em aula e alguma questão cobra está em caixa roxa.

- **Não vai para o site**: não tem pasta em `public/apostilas/` nem linha no banco. O PDF fica com o Mauricio (Drive, pasta MEDGENIUS).
- Organização: 10 ideias (cada uma com as etiquetas das questões que resolve e as armadilhas que já apareceram),
  o mapa das 15 questões com a página onde reler e um treino de 24 afirmações de verdadeiro ou falso.
- As figuras são as da apostila da aula (`../fig-algoritmo.svg` e `../fig-escada.svg`).

Gerar de novo:

```bash
apostilas-fonte/ferramentas/preparar.sh /tmp/gerar
cp apostilas-fonte/pneumo-a1/*.svg apostilas-fonte/pneumo-a1/provas-fag/apostila.html /tmp/gerar/
cd /tmp/gerar && python3 render.py apostila.html "Pneumologia - Aula 1 - Dr. Guerra - Embolia pulmonar nas Provas da FAG.pdf"
```

Mudou alguma questão das Provas da FAG da aula? Confira o mapa (capítulo 11) e as etiquetas dos capítulos.
