-- Executar somente depois de os 14 arquivos de página e o PDF estarem no ar.
-- Conteúdo aditivo: uma aula existente com este identificador não é sobrescrita.
insert into public.aulas
  (id, materia_id, ordem, titulo, resumo, publicada, apostila_html, pdf_caminho, data_aula, professor)
select
  'pass-a5', 'pass', 5, 'Medidas de associação e efeito',
  'Da tabela de exposição e desfecho ao tamanho do benefício e do dano de uma intervenção.',
  true,
  '<div class="paginas"><div class="pdfbar"><span class="main"><span class="t">Apostila em PDF</span><span class="s">14 páginas · abre numa nova aba</span></span><a class="btn ghost sm" href="/apostilas/pass-a5/apostila.pdf" target="_blank" rel="noopener">Abrir</a></div>'
  || (select string_agg(format('<img src="/apostilas/pass-a5/%s.webp" width="1400" height="1980" alt="Página %s de 14"%s decoding="async">', lpad(i::text, 2, '0'), i, case when i = 1 then '' else ' loading="lazy"' end), '' order by i) from generate_series(1, 14) i)
  || '</div>',
  '/apostilas/pass-a5/apostila.pdf', '2026-10-19',
  'Dr. Filipe Tomasi Keppen Sequeira de Almeida'
on conflict (id) do nothing;

update public.materias
set descricao = 'Cannabis medicinal com a Dra. Gisielli Alievi; testes diagnósticos e medidas de risco com o Dr. Filipe Almeida.'
where id = 'pass'
  and descricao = 'Cannabis medicinal com a Dra. Gisielli Alievi e testes diagnósticos com o Dr. Felipe.';
