-- Mensagens para o administrador (19/11/2026): botão de balão no topo de todas as telas.
-- O aluno escreve e vê as próprias; o administrador lê, marca como lida e apaga em
-- Administração → Mensagens (com a chave secreta). Primeiro passo do chat dentro do app.
create table public.mensagens (
  id uuid default gen_random_uuid() not null,
  user_id uuid default auth.uid() not null,
  autor text default 'Aluno'::text not null,
  texto text not null,
  status text default 'nova'::text not null,
  criado_em timestamp with time zone default now() not null,
  constraint mensagens_pkey PRIMARY KEY (id),
  constraint mensagens_status_check CHECK ((status = ANY (ARRAY['nova'::text, 'lida'::text]))),
  constraint mensagens_texto_check CHECK (((char_length(btrim(texto)) >= 1) AND (char_length(btrim(texto)) <= 2000))),
  constraint mensagens_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth.users(id) ON DELETE CASCADE
);
CREATE INDEX mensagens_user_idx ON public.mensagens USING btree (user_id, criado_em DESC);
CREATE INDEX mensagens_novas_idx ON public.mensagens USING btree (criado_em) WHERE (status = 'nova'::text);

-- Mensagem nova: autor (nome completo; sem nome, o login), dono, status e data saem daqui, não do aluno.
CREATE OR REPLACE FUNCTION public.mensagens_preencher()
 RETURNS trigger
 LANGUAGE plpgsql
 SECURITY DEFINER
 SET search_path TO ''
AS $function$
begin
  if auth.uid() is not null then
    new.user_id := auth.uid();
    new.status := 'nova';
    new.criado_em := now();
    new.autor := coalesce(
      nullif(btrim((select p.nome from public.perfis p where p.id = auth.uid())), ''),
      nullif(split_part((select u.email from auth.users u where u.id = auth.uid()), '@', 1), ''),
      'Aluno'
    );
  end if;
  new.texto := btrim(new.texto);
  return new;
end;
$function$
;
revoke execute on function public.mensagens_preencher() from public, anon, authenticated;
CREATE TRIGGER mensagens_preencher BEFORE INSERT ON public.mensagens FOR EACH ROW EXECUTE FUNCTION mensagens_preencher();

alter table public.mensagens enable row level security;
create policy "Aluno escreve a própria mensagem" on public.mensagens as permissive for insert to authenticated with check ((( SELECT auth.uid() AS uid) = user_id));
create policy "Aluno vê as próprias mensagens" on public.mensagens as permissive for select to authenticated using ((( SELECT auth.uid() AS uid) = user_id));
revoke all on public.mensagens from anon, authenticated;
grant insert, select on public.mensagens to authenticated;
