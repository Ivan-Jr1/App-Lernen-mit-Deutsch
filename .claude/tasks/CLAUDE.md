# CLAUDE.md

Contexto permanente do projeto **Deutsch App**, lido automaticamente pelo
Claude Code em toda sessão dentro desta pasta.

## O que é este projeto

App full-stack com dois objetivos: (1) ajudar Ivan e a esposa a estudar
alemão para uma mudança para Berlim (WHV, março/2027), e (2) servir como
projeto de portfólio para vagas de Junior Backend/Full-Stack Developer.

Público-alvo do código: recrutadores técnicos vão ler este repositório.
Priorize clareza e comentários sobre "esperteza".

## Stack

- **Backend**: Python 3.12 + FastAPI + SQLAlchemy + SQLite (local) /
  PostgreSQL (produção, se necessário)
- **Frontend**: React (Vite) + Tailwind CSS
- **Deploy**: backend no Render (free tier), frontend no Vercel ou Netlify

## Estrutura de pastas

```
deutsch-app/
  backend/
    main.py          # rotas da API (FastAPI)
    models.py         # modelos SQLAlchemy
    schemas.py         # schemas Pydantic (validação de entrada/saída)
    database.py        # engine e sessão do banco
    srs.py              # algoritmo SM-2 (repetição espaçada)
    seed_data.py         # dados de exemplo (cartões + cenários)
    requirements.txt
  frontend/
    src/
      api.js            # funções de chamada à API
      App.jsx
      pages/
        Flashcards.jsx
        Scenarios.jsx
        Couple.jsx
    package.json
  README.md
```

## Funcionalidades principais

1. **Flashcards com SM-2**: cartões com frente (PT), verso (DE) e dica
   fonética (aproximação de pronúncia em português). Revisão calcula o
   próximo intervalo com o algoritmo SM-2.
2. **Cenários de burocracia**: roleplay de situações reais (Anmeldung,
   banco, aluguel) com múltipla escolha e explicação da resposta certa.
3. **Modo casal**: dashboard comparando pontos, streak e progresso entre
   dois usuários fixos: `"ivan"` e `"esposa"`.

## Convenções de código

- Nomes de variáveis e comentários em português quando forem sobre domínio
  (ex: `phonetic_hint`, `next_review`) — o código deve ser legível pro
  próprio Ivan revisar depois
- Endpoints REST seguem padrão `/recurso/{id}/acao` (ex: `/cards/{id}/review`)
- Toda alteração no backend precisa manter o Swagger (`/docs`) funcional
  como documentação viva da API
- Testes ficam em `backend/tests/`, usando `pytest` + `TestClient` do FastAPI
- Commits pequenos e descritivos — este repo pode ser revisado por
  recrutadores, então o histórico do Git também é parte do portfólio

## Como rodar localmente

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (em outro terminal)
cd frontend
npm install
npm run dev
```

## O que NÃO fazer

- Não adicionar autenticação/login complexo — são só dois usuários fixos,
  não é um SaaS multiusuário
- Não trocar SQLite por Postgres antes do deploy real — complexidade
  desnecessária em desenvolvimento local
- Não remover as dicas fonéticas dos cartões — é o método de estudo
  próprio do Ivan, é a parte mais pessoal e diferenciada do projeto
