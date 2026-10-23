-- Angiologia como matéria (já aparecia na agenda com o id `angio`). Rubi, como as outras em tons de pedra preciosa.
insert into public.materias (id, nome, descricao, ordem, cor_inicio, cor_fim)
values ('angio', 'Angiologia', 'Angiologia com o Dr. Jeferson F. Toregeani, o Dr. Walter Karakhanian e o Dr. Américo.', 7, '#B91C1C', '#7F1D1D')
on conflict (id) do nothing;
