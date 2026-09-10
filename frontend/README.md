# Deutsch App — Frontend

React + Vite + Tailwind CSS. Consome a API do `../backend`.

```bash
npm install
npm run dev      # http://localhost:5173 — repassa /api para http://localhost:8000
npm run build    # gera dist/
```

Em produção, defina `VITE_API_URL` com a URL pública do backend (ver `.env.example`).
O `vercel.json` reescreve todas as rotas para `index.html` (necessário para o React Router).

## Estrutura

```
src/
  auth/AuthContext.jsx   token JWT + sessão (localStorage), rotas protegidas
  lib/api.js             cliente fetch (injeta o Bearer, trata 401)
  lib/theme.js           hook de modo claro/escuro (classe .dark no <html>)
  components/Layout.jsx  casca: sidebar no desktop, barra inferior no celular
  components/Logo.jsx    marca com as faixas da bandeira alemã
  components/ui.jsx      Button, Card, Avatar, estados de loading/erro/vazio
  pages/                 Login · Welcome · Review · Scenarios · Dashboard · Settings
```

## Telas

- **Login** — escolhe a conta; no primeiro acesso define a senha. Botão de visitante (somente leitura).
- **Welcome** — logo após o login, confirma ou troca o idioma de estudo antes de entrar no app.
- **Review** — flashcard com flip, notas 0–5 (SM-2), barra de progresso. Ao virar
  o cartão, a resposta é falada no idioma estudado via `speechSynthesis` (com botão de mudo).
- **Scenarios** — roleplay de situações do dia a dia com feedback e explicação ao
  errar; cada fala do atendente tem um botão para ouvir.
- **Dashboard** — comparação de progresso dos dois usuários, com modo escuro.
- **Settings** — foto de perfil (redimensionada no cliente), nome, idioma de estudo,
  meta diária, velocidade da voz e troca de senha.

## PWA

`public/manifest.webmanifest` + ícones + meta tags no `index.html` tornam o app
instalável ("Adicionar à tela de início"). Sem service worker — o app precisa de
rede para a API de qualquer forma.

O README principal está em [`../README.md`](../README.md).
