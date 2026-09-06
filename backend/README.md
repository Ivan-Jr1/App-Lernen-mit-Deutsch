# Deutsch App — Backend

API REST em FastAPI para estudo de alemão: flashcards com repetição espaçada
(SM-2), cenários de burocracia em roleplay e dashboard de progresso do casal.

O design completo (schema, algoritmo, regras de pontuação, superfície da API)
está em [`../docs/DESIGN.md`](../docs/DESIGN.md).

## Rodando localmente

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m app.seed            # popula usuários, ~17 cartões e 3 cenários
uvicorn app.main:app --reload
```

- API: http://localhost:8000
- Documentação interativa (Swagger): http://localhost:8000/docs
- Schema OpenAPI: http://localhost:8000/openapi.json

## Testes

```bash
cd backend
pytest -q
```

## Identificação do usuário

Não há autenticação nesta versão (são dois usuários fixos). Cada request diz
quem está agindo via `?user=ivan` ou o header `X-User: ivan`.

## Configuração

Copie `.env.example` para `.env`. Trocar o SQLite por PostgreSQL é só mudar
`DATABASE_URL` — nenhuma outra alteração no código.

## Estrutura

```
app/
  main.py        instancia o FastAPI e monta os routers
  config.py      settings via variáveis de ambiente
  database.py    engine, sessão, dependência get_db
  models.py      modelos SQLAlchemy (comentados)
  schemas.py     modelos Pydantic (contrato da API)
  deps.py        dependências: sessão e usuário atual
  srs.py         algoritmo SM-2, isolado e testável
  scoring.py     regras de pontuação
  stats.py       cálculo de streak e agregados do dashboard
  routers/       cards, reviews, scenarios, dashboard
  seed.py        popula o banco a partir de data/seed_data.py
tests/           pytest — SM-2, revisões, cenários, dashboard
```
