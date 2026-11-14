// Aviso de notas do Sagres (só do Mauricio, administrador).
//
// O que faz: entra na API do Sagres (a mesma do app Sagres Mobile) com o login do Mauricio,
// lê as notas e as faltas do semestre atual, compara com a última leitura e, se mudou algo,
// manda uma mensagem no WhatsApp dele (CallMeBot). Guarda a leitura em public.sagres_estado.
//
// Quem chama: o relógio do banco (pg_cron, job "sagres-notas"), a cada 30 minutos, de dia.
// Roda no Supabase em São Paulo (o Sagres bloqueia acesso de fora do Brasil): quem chama
// passa ?forceFunctionRegion=sa-east-1.
// Tranca: só responde a quem manda o cabeçalho x-gatilho igual a sagres_estado.gatilho.
//
// Segredos (Supabase → Edge Functions → Secrets, postos pelo Mauricio):
//   SAGRES_USUARIO, SAGRES_SENHA, WHATSAPP_NUMERO, CALLMEBOT_APIKEY
//
// Modos: sem parâmetro = confere e avisa; ?ler=1 = só mostra a leitura; ?testar=1 = confere e manda um resumo no WhatsApp
// mesmo sem novidade. Publicar: pelo conector do Supabase (deploy_edge_function) com este arquivo.
//
// Este arquivo roda no Deno (Supabase), não no Next.js: fica fora do tsconfig.

const API = "https://sagres.fag.edu.br/api/SagresApi";
const BANCO = Deno.env.get("SUPABASE_URL")!;
const CHAVE = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!;

type Link = { $link?: { href: string } };
type Avaliacao = { id: string; nome: string; peso: number; nota: number | null };
type Grupo = { id: string; nome: string; peso: number; avaliacoes: Avaliacao[] };
type Materia = {
  id: number;
  nome: string;
  limiteFaltas: number | null;
  faltas: number;
  resultado: Record<string, unknown>;
  grupos: Grupo[];
};
type Leitura = { periodo: string; materias: Materia[] };

const limpo = (s: unknown) => String(s ?? "").replace(/\s+/g, " ").trim();
const fmt = (n: number) => n.toLocaleString("pt-BR", { maximumFractionDigits: 2 });

async function banco(caminho: string, init: RequestInit = {}) {
  const r = await fetch(`${BANCO}/rest/v1/${caminho}`, {
    ...init,
    headers: { apikey: CHAVE, Authorization: `Bearer ${CHAVE}`, "Content-Type": "application/json", ...init.headers },
  });
  if (!r.ok) throw new Error(`banco ${r.status}: ${await r.text()}`);
  return r.status === 204 ? null : r.json();
}

const AUTH = "Basic " + btoa(`${Deno.env.get("SAGRES_USUARIO")}:${Deno.env.get("SAGRES_SENHA")}`);

async function sagres(caminho: string) {
  const r = await fetch(API + caminho, { headers: { Authorization: AUTH, Accept: "application/json" } });
  if (r.status === 401) throw new Error("O Sagres recusou o login (senha mudou?)");
  if (!r.ok) throw new Error(`Sagres ${r.status} em ${caminho.split("?")[0]}`);
  return r.json();
}

const href = (x: Link | undefined) => x?.$link?.href ?? "";

async function lerMateria(t: Record<string, Link & unknown>, nomes: Map<number, string>): Promise<Materia> {
  const id = t.id as unknown as number;
  const ativ = href(t.atividadeCurricular as Link);
  const [nome, faltas, resultado, grupos] = await Promise.all([
    (async () => {
      const salvo = nomes.get(id);
      if (salvo) return salvo;
      const a = await sagres(ativ);
      return limpo(a.nome);
    })(),
    sagres(href(t.faltas as Link)).then((f) => (f.itens ?? []).length as number),
    sagres(href(t.resultado as Link)).then((r) => {
      const { $link: _, ...resto } = r;
      return resto as Record<string, unknown>;
    }),
    sagres(href(t.avaliacoes as Link)).then((g) =>
      Promise.all(
        (g.itens ?? []).map(async (gr: Record<string, unknown>): Promise<Grupo> => {
          const subs = await sagres(href(gr.avaliacoes as Link));
          const avaliacoes = await Promise.all(
            (subs.itens ?? []).map(async (av: Record<string, unknown>): Promise<Avaliacao> => {
              const ln = href(av.nota as Link);
              // Nota ainda não lançada: o link vem com id -1 (".../notas/1--1-<pessoa>").
              const valor = ln && !ln.includes("--1-") ? (await sagres(ln)).valor : null;
              return { id: String(av.id), nome: limpo(av.nomeResumido || av.nome), peso: Number(av.peso), nota: valor ?? null };
            }),
          );
          avaliacoes.sort((a, b) => a.nome.localeCompare(b.nome));
          return { id: String(gr.id), nome: limpo(gr.nome), peso: Number(gr.peso), avaliacoes };
        }),
      )
    ),
  ]);
  // O total do Sagres conta aulas duplas; a lista de faltas serve quando ele não vem.
  const total = Number(resultado.totalFaltas ?? faltas);
  return { id, nome, limiteFaltas: (t.limiteFaltas as unknown as number) ?? null, faltas: total, resultado, grupos };
}

async function ler(anterior: Leitura | null): Promise<Leitura> {
  const eu = await sagres("/eu");
  const per = await sagres(`/diario/periodos-letivos?idPessoa=${eu.id}&perfil=1`);
  const hoje = Date.now();
  const itens = (per.itens ?? []) as Record<string, unknown>[];
  const atual =
    itens.find((p) => Date.parse(String(p.inicio)) <= hoje && hoje <= Date.parse(String(p.fim))) ?? itens[0];
  const turmas = await sagres(href(atual.turmas as Link));
  const nomes = new Map((anterior?.materias ?? []).map((m) => [m.id, m.nome] as [number, string]));
  const materias = await Promise.all((turmas.itens ?? []).map((t: Record<string, Link>) => lerMateria(t, nomes)));
  materias.sort((a, b) => a.nome.localeCompare(b.nome));
  return { periodo: limpo(atual.codigo), materias };
}

// O que mudou entre duas leituras, em frases para o WhatsApp.
function novidades(antes: Leitura, agora: Leitura): string[] {
  const out: string[] = [];
  const notasAntes = new Map<string, number | null>();
  const faltasAntes = new Map<number, number>();
  for (const m of antes.materias) {
    faltasAntes.set(m.id, m.faltas);
    for (const g of m.grupos) for (const a of g.avaliacoes) notasAntes.set(`${m.id}|${a.id}`, a.nota);
  }
  for (const m of agora.materias) {
    for (const g of m.grupos)
      for (const a of g.avaliacoes) {
        const velha = notasAntes.get(`${m.id}|${a.id}`) ?? null;
        if (a.nota === null || a.nota === velha) continue;
        out.push(
          velha === null
            ? `📚 *${m.nome}*: ${g.nome} ${a.nome} = *${fmt(a.nota)}*`
            : `✏️ *${m.nome}*: ${g.nome} ${a.nome} mudou de ${fmt(velha)} para *${fmt(a.nota)}*`,
        );
      }
    const fa = faltasAntes.get(m.id);
    if (fa !== undefined && m.faltas > fa)
      out.push(`🕒 *${m.nome}*: ${m.faltas} falta(s)${m.limiteFaltas ? ` de ${m.limiteFaltas} permitidas` : ""}`);
  }
  return out;
}

function resumo(l: Leitura): string {
  const linhas = l.materias.map((m) => {
    const ns = m.grupos.flatMap((g) => g.avaliacoes.filter((a) => a.nota !== null).map((a) => `${g.nome} ${a.nome} ${fmt(a.nota!)}`));
    return `• ${m.nome}: ${ns.length ? ns.join(", ") : "sem nota"}${m.faltas ? ` (${m.faltas} falta(s))` : ""}`;
  });
  return `Semestre ${l.periodo}\n${linhas.join("\n")}`;
}

async function whatsapp(texto: string) {
  const u = new URL("https://api.callmebot.com/whatsapp.php");
  u.searchParams.set("phone", Deno.env.get("WHATSAPP_NUMERO")!);
  u.searchParams.set("text", texto);
  u.searchParams.set("apikey", Deno.env.get("CALLMEBOT_APIKEY")!);
  const r = await fetch(u);
  // Erro do CallMeBot vem com status 203 e o motivo no fim do texto (ex.: "APIKey is invalid").
  // O começo do texto repete o número e a mensagem, então o erro guarda só o fim.
  const txt = (await r.text()).replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
  if (r.status !== 200 || /invalid|error/i.test(txt)) throw new Error(`WhatsApp (CallMeBot): ${txt.slice(-160)}`);
}

Deno.serve(async (req) => {
  const [estado] = await banco("sagres_estado?id=eq.1&select=gatilho,ultimo,erro");
  if (!estado?.gatilho || req.headers.get("x-gatilho") !== estado.gatilho) return new Response("nao", { status: 403 });
  const params = new URL(req.url).searchParams;
  const testar = params.has("testar");
  const anterior = estado.ultimo as Leitura | null;
  // ?ler=1: só mostra a leitura, sem guardar nem mandar mensagem (para conferir).
  if (params.has("ler")) return Response.json(await ler(anterior));
  const agoraIso = new Date().toISOString();

  try {
    const agora = await ler(anterior);
    const mudou = anterior ? novidades(anterior, agora) : [];
    if (mudou.length) await whatsapp(`Sagres: novidade!\n\n${mudou.join("\n")}`);
    else if (!anterior || testar)
      await whatsapp(`${anterior ? "Teste do aviso de notas" : "Aviso de notas ligado ✅"}\n\n${resumo(agora)}`);
    else if (estado.erro) await whatsapp("Aviso de notas: voltou a funcionar ✅");
    await banco("sagres_estado?id=eq.1", {
      method: "PATCH",
      headers: { Prefer: "return=minimal" },
      body: JSON.stringify({ ultimo: agora, lido_em: agoraIso, erro: null, ...(mudou.length ? { mudou_em: agoraIso } : {}) }),
    });
    return Response.json({ ok: true, novidades: mudou.length, materias: agora.materias.length });
  } catch (e) {
    const msg = String((e as Error).message ?? e).slice(0, 500);
    // Avisa só quando o erro aparece (não a cada 30 minutos).
    if (!estado.erro) await whatsapp(`Aviso de notas parou: ${msg}`).catch(() => {});
    await banco("sagres_estado?id=eq.1", {
      method: "PATCH",
      headers: { Prefer: "return=minimal" },
      body: JSON.stringify({ erro: msg, lido_em: agoraIso }),
    }).catch(() => {});
    return Response.json({ ok: false, erro: msg }, { status: 500 });
  }
});
