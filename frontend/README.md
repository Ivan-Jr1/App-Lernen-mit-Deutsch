# Deutsch App — Frontend

React + Vite + Tailwind CSS. Consome a API do `../backend`.

```bash
npm install
npm run dev      # http://localhost:5173 — repassa /api para http://localhost:8000
npm run build    # gera dist/
```

Em produção, defina `VITE_API_URL` com a URL pública do backend (ver `.env.example`).
O `vercel.json` reescreve todas as rotas para `index.html` (necessário para o React Router).

## Telas

- `src/pages/Review.jsx` — revisão de flashcards com notas 0–5 (SM-2)
- `src/pages/Scenarios.jsx` — cenários de burocracia em roleplay
- `src/pages/Dashboard.jsx` — comparação de progresso dos dois usuários

O usuário ativo (ivan / esposa) é escolhido no cabeçalho e guardado no `localStorage`
(`src/user.jsx`). Não há autenticação nesta versão.

O README principal do projeto está em [`../README.md`](../README.md).
