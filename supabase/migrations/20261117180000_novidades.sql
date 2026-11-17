-- Novidades do app (17/11/2026): avisos do sininho ao lado da engrenagem.
-- O administrador escreve e apaga em Administração → Novidades (com a chave secreta); a turma só lê.
-- id em texto: as três primeiras mantêm o id que já tinham no código, para quem já viu não ver de novo.
create table public.novidades (
  id text default (gen_random_uuid())::text not null,
  titulo text not null,
  texto text not null,
  criado_em timestamp with time zone default now() not null,
  constraint novidades_pkey PRIMARY KEY (id),
  constraint novidades_titulo_check CHECK (((char_length(btrim(titulo)) >= 1) AND (char_length(btrim(titulo)) <= 120))),
  constraint novidades_texto_check CHECK (((char_length(btrim(texto)) >= 1) AND (char_length(btrim(texto)) <= 1000)))
);
CREATE INDEX novidades_criado_idx ON public.novidades USING btree (criado_em DESC);
alter table public.novidades enable row level security;
create policy "Turma lê as novidades" on public.novidades as permissive for select to authenticated using (true);
revoke all on public.novidades from anon, authenticated;
grant select on public.novidades to authenticated;

insert into public.novidades (id, titulo, texto, criado_em) values
  ('2026-11-17-fastcards', 'FastCardsGenius', 'Os antigos Flashcards Dia D agora se chamam FastCardsGenius: um baralho rápido de véspera para resolver as questões das Provas da FAG.', '2026-11-17 12:00:00-03'),
  ('2026-11-17-modo-crazy', 'Estudo diário e Modo CRAZY', 'No cartão de cada aula, na matéria: Apostila, Questões e Flashcards ficam no Estudo diário; Provas da FAG e FastCardsGenius ficam no Modo CRAZY, para a véspera da prova.', '2026-11-17 12:01:00-03'),
  ('2026-11-17-novidades', 'Novidades por aqui', 'Este sininho avisa quando o app ganha algo novo. A bolinha some depois que você abre.', '2026-11-17 12:02:00-03');
