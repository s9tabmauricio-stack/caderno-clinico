// Aparência do app: 'auto' segue o modo do aparelho; 'dia' e 'noite' são a escolha do aluno,
// salva no próprio aparelho (localStorage). O CSS lê data-tema="dia"|"noite" no <html>.
export type Escolha = 'auto' | 'dia' | 'noite'

export const CHAVE_TEMA = 'mg-tema'

// Roda no <head> antes da primeira pintura (app/layout.tsx), para a tela não piscar na cor errada,
// e de novo quando o aparelho troca de modo ou o aluno escolhe outra opção (window.__mgTema).
// Também acerta a cor da barra do navegador.
export const SCRIPT_TEMA = `(function(){try{var e=document.documentElement,m=matchMedia('(prefers-color-scheme: light)');function a(){var t='auto';try{t=localStorage.getItem('${CHAVE_TEMA}')||'auto'}catch(_){}var d=t==='dia'||(t!=='noite'&&m.matches);e.setAttribute('data-tema',d?'dia':'noite');e.setAttribute('data-escolha',t);var c=d?'#E4E7EC':'#0C0D11',q=document.querySelectorAll('meta[name="theme-color"]');for(var i=0;i<q.length;i++)q[i].setAttribute('content',c)}a();m.addEventListener('change',a);document.addEventListener('DOMContentLoaded',a);window.__mgTema=a}catch(_){}})()`
