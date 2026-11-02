---
name: provas-agenda
description: Lança as provas (P2 e outras) na Agenda do Med Genius pelo conector do Supabase. Use quando o Mauricio pedir para incluir, mudar ou conferir datas de prova.
---

# Provas na Agenda

- **Provas (P2 de 10 a 25/11/2026)**: entram pelo conector em `agenda_eventos` com `tipo = 'prova'`, `fixo = true`, título "P2 de <Matéria>" (crie antes a semana em `agenda_semanas` só com a segunda-feira, se ela ainda não existir). Aparecem no dia (Início e Agenda) e no quadro "Próximas provas" no fim da Agenda. Publicar a semana não apaga; se o cronograma do WhatsApp trouxer a prova da mesma matéria no mesmo dia, no dia vale a do cronograma. Semana só de provas não aparece em "Semanas publicadas" nem vira "a próxima semana" antes de chegar.
