-- Aplicar após o PDF e as 20 imagens estarem disponíveis em produção.
-- Não altera estrutura, questões, flashcards ou progresso dos alunos.
insert into public.aulas (id, materia_id, ordem, titulo, resumo, publicada, data_aula, professor, pdf_caminho, apostila_html)
select 'nefro-a6', 'nefro', 6, 'Da bexiga ao rim — infecção urinária',
  'Como reconhecer, investigar e tratar a infecção urinária na mulher adulta e na gestação.',
  true, date '2026-10-21', 'Dra. Andressa', null,
  '<div class="paginas"><div class="pdfbar"><span class="main"><span class="t">Apostila em PDF</span><span class="s">20 páginas · abre numa nova aba</span></span><a class="btn ghost sm" href="/apostilas/nefro-a6/apostila.pdf" target="_blank" rel="noopener">Abrir</a></div>'
  || (select string_agg(format('<img src="/apostilas/nefro-a6/%s.webp" width="1400" height="1980" alt="Página %s de 20"%s decoding="async">', lpad(i::text, 2, '0'), i, case when i = 1 then '' else ' loading="lazy"' end), '' order by i) from generate_series(1, 20) i)
  || '</div>'
on conflict (id) do nothing;

update public.materias
set descricao = concat_ws(' ', nullif(descricao, ''), 'Infecção urinária com a Dra. Andressa.')
where id = 'nefro' and position('Dra. Andressa' in coalesce(descricao, '')) = 0;
