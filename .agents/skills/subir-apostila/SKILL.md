---
name: subir-apostila
description: Põe no site a apostila em PDF de uma aula do Med Genius (páginas em imagem iguais ao PDF) e inclui a aula no banco; também troca uma apostila que já está no ar. Use quando houver um PDF de apostila para publicar ou substituir.
---

# Como subir uma apostila (o jeito aprovado: páginas iguais ao PDF)

O passo 1 e o 2 são o que faz `scripts/publicar-apostila.sh <arquivo.pdf> <aula-id>` (mostra o número de páginas no fim).

1. `pdftoppm -scale-to-x 1400 -scale-to-y -1 -jpeg -jpegopt quality=80 arquivo.pdf public/apostilas/<aula-id>/p`
2. Converter cada página para `NN.webp` (qualidade 78) e apagar os .jpg; copiar o PDF como `public/apostilas/<aula-id>/apostila.pdf`.
3. Commit + push (as imagens precisam estar no ar).
4. Incluir a aula pelo conector:

```sql
insert into public.aulas (id, materia_id, ordem, titulo, resumo, publicada, apostila_html)
select '<aula-id>', '<materia>', <N>, '<Título>', '<Resumo da capa>', true,
  '<div class="paginas"><div class="pdfbar"><span class="main"><span class="t">Apostila em PDF</span><span class="s"><P> páginas · abre numa nova aba</span></span><a class="btn ghost sm" href="/apostilas/<aula-id>/apostila.pdf" target="_blank" rel="noopener">Abrir</a></div>'
  || (select string_agg(format('<img src="/apostilas/<aula-id>/%s.webp" width="1400" height="1980" alt="Página %s de <P>"%s decoding="async">', lpad(i::text, 2, '0'), i, case when i = 1 then '' else ' loading="lazy"' end), '' order by i) from generate_series(1, <P>) i)
  || '</div>'
on conflict (id) do nothing;
```

Título, resumo e professor saem da capa (`pdftotext -f 1 -l 1`). Atualize a `descricao` da matéria com o professor. Trocar uma apostila = sobrescrever as imagens e o PDF e publicar. **Se o número de páginas mudar**, refaça também o `apostila_html` da aula (mesmo modelo acima, com o número novo), senão as páginas a mais não aparecem; pelo conector isso funciona, porque o comando é curto mesmo gerando um texto longo.

**Guarde o HTML da apostila em [`apostilas-fonte/<aula-id>/`](apostilas-fonte/README.md)** (o arquivo de onde o PDF é gerado, com as figuras e os programas que as desenham). Sem ele, mudar o visual obriga a remontar a apostila inteira a partir do PDF. As apostilas anteriores a 31/10/2026 ainda não têm esse arquivo; as de Pneumologia 1 a 4 já têm.
