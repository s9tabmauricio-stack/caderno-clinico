// Robô do Gmail do Med Genius: cria a conta de quem manda e-mail pedindo acesso.
// Fica no Google Apps Script da conta do Mauricio; esta é a cópia guardada no projeto.
// Passo a passo para instalar: docs/robo-gmail/README.md
//
// Como funciona: a cada 5 minutos procura e-mails com o assunto "Acesso Med Genius".
// Se quem mandou é @minha.fag.edu.br e o texto tem uma senha de 6 números, pede ao site para
// criar a conta (login = o e-mail de quem mandou), responde à pessoa e põe o e-mail na
// etiqueta "Med Genius/Contas". O e-mail com a senha vai para a lixeira.

const SITE = 'https://medgenius.vercel.app'
const ASSUNTO = 'Acesso Med Genius'
const DOMINIO = '@minha.fag.edu.br'
const ETIQUETA = 'Med Genius/Contas'

/** 1º passo: rode uma vez. Cria a chave do robô e mostra no registro (copie para a Vercel). */
function gerarChave() {
  const chave = (Utilities.getUuid() + Utilities.getUuid()).replace(/-/g, '')
  PropertiesService.getScriptProperties().setProperty('CHAVE', chave)
  Logger.log('Copie esta chave para a Vercel (ROBO_GMAIL_CHAVE): ' + chave)
}

/** 2º passo: rode uma vez. Liga o robô a cada 5 minutos. */
function ligarRobo() {
  desligarRobo()
  ScriptApp.newTrigger('verificarEmails').timeBased().everyMinutes(5).create()
  Logger.log('Robô ligado: confere o Gmail a cada 5 minutos.')
}

/** Desliga o robô (não apaga nada). */
function desligarRobo() {
  ScriptApp.getProjectTriggers()
    .filter((t) => t.getHandlerFunction() === 'verificarEmails')
    .forEach((t) => ScriptApp.deleteTrigger(t))
}

/** O que roda a cada 5 minutos. */
function verificarEmails() {
  const chave = PropertiesService.getScriptProperties().getProperty('CHAVE')
  if (!chave) throw new Error('Rode gerarChave primeiro.')
  const eu = Session.getEffectiveUser().getEmail().toLowerCase()
  const etiqueta = GmailApp.getUserLabelByName(ETIQUETA) || GmailApp.createLabel(ETIQUETA)
  const conversas = GmailApp.search('subject:"' + ASSUNTO + '" -label:' + ETIQUETA.replace(/[ /]/g, '-') + ' newer_than:14d', 0, 20)

  for (const conversa of conversas) {
    let terminou = true
    for (const msg of conversa.getMessages()) {
      if (msg.isInTrash()) continue
      const de = msg.getFrom()
      const email = ((de.match(/<([^>]+)>/) || [null, de])[1] || '').trim().toLowerCase()
      if (!email || email === eu) continue // as respostas do próprio robô
      if (!email.endsWith(DOMINIO)) continue // de fora da FAG: ignora em silêncio
      const nome = de.includes('<') ? de.split('<')[0].replace(/"/g, '').trim() : ''
      const senha = (msg.getPlainBody().match(/(?:^|\D)(\d{6})(?!\d)/) || [])[1]

      if (!senha) {
        msg.reply('Olá! Para criar sua conta no Med Genius, mande um e-mail novo com o assunto "' + ASSUNTO + '" e, no texto, só a senha que você quer: 6 números.')
        msg.moveToTrash() // assim não responde de novo na próxima rodada
        continue
      }

      const r = UrlFetchApp.fetch(SITE + '/api/contas-gmail', {
        method: 'post',
        contentType: 'application/json',
        headers: { Authorization: 'Bearer ' + chave },
        payload: JSON.stringify({ email: email, senha: senha, nome: nome }),
        muteHttpExceptions: true,
      })
      const codigo = r.getResponseCode()
      let motivo = ''
      try { motivo = JSON.parse(r.getContentText()).motivo || '' } catch (e) {}

      if (codigo === 201) {
        msg.reply('Sua conta no Med Genius está pronta!\n\nEntre em ' + SITE + ' com:\n• Login: ' + email + '\n• Senha: a de 6 números que você mandou\n\nA conta fica aberta em 1 aparelho por vez.')
      } else if (codigo === 409) {
        msg.reply('Já existe uma conta no Med Genius com o e-mail ' + email + '. Se esqueceu a senha, fale com o Mauricio.')
      } else if (codigo === 400) {
        msg.reply('Não deu para criar sua conta: ' + motivo + '\n\nMande um e-mail novo com o assunto "' + ASSUNTO + '" e, no texto, só a senha de 6 números.')
      } else {
        // Problema do site ou da chave: não responde e tenta de novo na próxima rodada.
        terminou = false
        Logger.log('Erro ' + codigo + ' com ' + email + ': ' + motivo)
        continue
      }
      msg.moveToTrash() // tira a senha da caixa de entrada
    }
    if (terminou) conversa.addLabel(etiqueta)
  }
}
