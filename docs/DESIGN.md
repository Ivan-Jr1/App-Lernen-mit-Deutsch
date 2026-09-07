# Deutsch App — Documento de Design

> Spec escrita **antes** da implementação. Serve como referência para o backend,
> o frontend e a leitura técnica por recrutadores.

## 1. Problema

Preciso estudar alemão para uma mudança para Berlim e, ao mesmo tempo, ter um
projeto de portfólio que demonstre construção de uma **API REST real** com
frontend conectado (vaga alvo: Junior Backend / Full-Stack).

## 2. Objetivos e não-objetivos

**Objetivos**
- Flashcards com repetição espaçada (algoritmo SM-2, mesmo princípio do Anki).
- Cenários de burocracia em formato roleplay de múltipla escolha, com explicação
  ao errar.
- Dashboard de casal comparando o progresso de dois usuários fixos (`ivan`,
  `gabriela`) de forma amigável.
- Autenticação por token JWT. Cadastro fechado: só as contas do seed. Cada conta
  define a própria senha no primeiro acesso. Uma conta de visitante dá acesso
  somente leitura para recrutadores.
- Código legível, modelos comentados, testes dos endpoints principais, Swagger
  automático, README de deploy.

**Não-objetivos (fora de escopo nesta versão)**
- Cadastro aberto / recuperação de senha por e-mail.
- Áudio/TTS de pronúncia (a "dica fonética" é texto).
- App mobile nativo.

## 3. Stack

| Camada    | Tecnologia |
|-----------|------------|
| Backend   | Python 3.11+ · FastAPI · SQLAlchemy 2.x · SQLite (troca para PostgreSQL só mudando a URL) |
| Frontend  | React + Vite · Tailwind CSS · React Router |
| Testes    | pytest · httpx / TestClient |
| Deploy    | Backend no Render (free) · Frontend no Vercel (free) |

## 4. Modelo de dados

Princípio central: **um cartão compartilhado tem uma agenda SRS por usuário**.
O cartão guarda só o conteúdo; o estado de repetição espaçada (facilidade,
intervalo, data de vencimento) vive em `review_states`, uma linha por
`(usuário, cartão)`.

### 4.1 `users`
Dois registros fixos criados por seed.

| Coluna       | Tipo        | Notas |
|--------------|-------------|-------|
| id            | int PK      | |
| username      | str, unique | `ivan`, `gabriela`, `demo` |
| display_name  | str         | Nome exibido no dashboard |
| password_hash | str, nullable | Argon2. Nulo = conta ainda não reivindicada (define a senha no 1º acesso). Sempre nulo para o visitante. |
| is_guest      | bool        | `true` = conta de visitante (somente leitura), fora do dashboard do casal |
| avatar_url    | text, nullable | Foto de perfil como data URI (o cliente redimensiona para ~256px antes de enviar) |
| created_at    | datetime    | |

### 4.2 `cards`
Conteúdo do flashcard. Não guarda estado de estudo.

| Coluna         | Tipo              | Notas |
|----------------|-------------------|-------|
| id             | int PK            | |
| front_pt       | str               | Frase em português (frente) |
| back_de        | str               | Tradução em alemão (verso) |
| phonetic_hint  | str, nullable     | Aproximação de pronúncia em português — ex.: "Wie geht's" → "Ví guêts" |
| category       | str, nullable     | Agrupamento livre — ex.: `saudações`, `banco`, `moradia` |
| owner_id       | int FK users, nullable | **NULL = cartão compartilhado** (aparece para os dois). Preenchido = cartão privado daquele usuário. |
| created_at     | datetime          | |

### 4.3 `review_states`
Estado SM-2 atual de um cartão para um usuário. Criado no primeiro contato do
usuário com o cartão.

| Coluna           | Tipo     | Default | Notas |
|------------------|----------|---------|-------|
| id               | int PK   |         | |
| user_id          | int FK users   | | |
| card_id          | int FK cards   | | |
| repetitions      | int      | 0       | Nº de revisões seguidas com nota ≥ 3 (o `n` do SM-2) |
| ease_factor      | float    | 2.5     | Fator de facilidade (EF), mínimo 1.3 |
| interval_days    | int      | 0       | Intervalo atual em dias |
| due_date         | date     | hoje    | Quando o cartão volta para revisão |
| last_reviewed_at | datetime, nullable | | |
| last_grade       | int, nullable | | Última nota 0–5 |

Restrição: `UNIQUE(user_id, card_id)`.

### 4.4 `review_logs`
Histórico imutável de cada revisão. Base para "total de cartões revisados",
pontos e gráficos.

| Coluna              | Tipo     | Notas |
|---------------------|----------|-------|
| id                  | int PK   | |
| user_id             | int FK users | |
| card_id             | int FK cards | |
| grade               | int      | Nota informada, 0–5 |
| previous_interval   | int      | Intervalo antes desta revisão |
| new_interval        | int      | Intervalo calculado |
| ease_factor_after   | float    | EF após esta revisão |
| points_earned       | int      | Pontos concedidos (ver §6) |
| reviewed_at         | datetime | |

### 4.5 `scenarios`
Um cenário de burocracia.

| Coluna      | Tipo        | Notas |
|-------------|-------------|-------|
| id          | int PK      | |
| slug        | str, unique | ex.: `anmeldung`, `abrir-conta`, `alugar-apartamento` |
| title       | str         | |
| description | str         | Contexto exibido antes de começar |
| category    | str         | ex.: `registro`, `banco`, `moradia` |
| created_at  | datetime    | |

### 4.6 `scenario_steps`
Cada fala do "atendente" dentro de um cenário, em ordem.

| Coluna          | Tipo   | Notas |
|-----------------|--------|-------|
| id              | int PK | |
| scenario_id     | int FK scenarios | |
| step_order      | int    | 1, 2, 3… |
| speaker_text_de | str    | Fala do atendente em alemão |
| speaker_text_pt | str, nullable | Tradução de apoio |

Restrição: `UNIQUE(scenario_id, step_order)`.

### 4.7 `scenario_options`
As 2–3 respostas de múltipla escolha de um passo.

| Coluna         | Tipo   | Notas |
|----------------|--------|-------|
| id             | int PK | |
| step_id        | int FK scenario_steps | |
| option_text_de | str    | Texto da opção em alemão |
| is_correct     | bool   | Exatamente uma `true` por passo |
| explanation    | str    | Por que a resposta correta é mais natural — mostrado ao errar |
| option_order   | int    | Ordem de exibição |

### 4.8 `scenario_attempts`
Uma jogada de um cenário por um usuário.

| Coluna          | Tipo     | Notas |
|-----------------|----------|-------|
| id              | int PK   | |
| user_id         | int FK users | |
| scenario_id     | int FK scenarios | |
| total_steps     | int      | Nº de passos no cenário no momento da jogada |
| correct_count   | int      | Acertos na primeira tentativa |
| is_completed    | bool     | `true` quando todos os passos foram respondidos |
| points_earned   | int      | Pontos concedidos (ver §6) |
| started_at      | datetime | |
| completed_at    | datetime, nullable | |

### 4.9 `scenario_attempt_answers`
Resposta escolhida em cada passo de uma jogada. Permite revisar os erros depois.

| Coluna       | Tipo   | Notas |
|--------------|--------|-------|
| id           | int PK | |
| attempt_id   | int FK scenario_attempts | |
| step_id      | int FK scenario_steps | |
| option_id    | int FK scenario_options | Opção escolhida |
| is_correct   | bool   | Cópia do acerto no momento da resposta |
| answered_at  | datetime | |

### 4.10 Diagrama de relacionamentos

```
users ──1:N──> cards (owner_id, opcional)
users ──1:N──> review_states <──N:1── cards        UNIQUE(user_id, card_id)
users ──1:N──> review_logs   <──N:1── cards
users ──1:N──> scenario_attempts <──N:1── scenarios
scenarios ──1:N──> scenario_steps ──1:N──> scenario_options
scenario_attempts ──1:N──> scenario_attempt_answers ──N:1──> scenario_steps / scenario_options
```

## 5. Algoritmo SM-2

Entrada: nota `q` de 0 a 5 informada pelo usuário ao revisar.

```
EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
se EF' < 1.3: EF' = 1.3           # EF é sempre atualizado

se q >= 3:                        # acerto
    se repetitions == 0: interval = 1
    senão se repetitions == 1: interval = 6
    senão: interval = round(interval * EF)   # usa o EF anterior
    repetitions += 1
senão:                            # erro — volta para o início
    repetitions = 0
    interval = 1

due_date = hoje + interval dias
```

Um cartão está "vencido" para um usuário quando `due_date <= hoje` — ou quando
ainda não existe `review_state` para aquele `(usuário, cartão)` (cartão novo).

## 6. Pontos e streak (dashboard do casal)

Derivados de `review_logs` e `scenario_attempts` — não há tabela de placar
separada, os números são calculados por agregação SQL.

**Pontos**
- Revisão de cartão com nota ≥ 3: **+10**
- Revisão de cartão com nota < 3: **+3** (recompensa por aparecer)
- Cenário concluído: **+15**, com **+5** de bônus se zero erros

**Dia de estudo**: qualquer dia (fuso `Europe/Berlin`) com ao menos uma revisão
ou um cenário concluído.

- **Streak atual**: dias de estudo consecutivos terminando hoje (ou ontem, se
  ainda não houve estudo hoje).
- **Streak recorde**: maior sequência de dias de estudo consecutivos no
  histórico.

**Números do dashboard, por usuário**: pontos totais, streak atual, streak
recorde, total de cartões revisados (`count(review_logs)`), cenários concluídos
(`count(scenario_attempts where is_completed)`).

## 7. Superfície da API

Autenticação por `Authorization: Bearer <token>` em tudo, exceto `/api/health` e
`/api/auth/*`. Endpoints de escrita recusam o token de visitante (403).

```
GET  /api/health

GET  /api/auth/accounts                    contas fixas e se já têm senha
POST /api/auth/claim                       body: {username, password} — define a senha no 1º acesso, devolve token
POST /api/auth/login                       body: {username, password} — devolve token
POST /api/auth/guest                       devolve token somente leitura (visitante)
GET  /api/auth/me                          confirma a sessão atual
PATCH /api/auth/me                         body: {display_name?, avatar_url?} — atualiza o perfil  [escrita]
POST /api/auth/change-password             body: {current_password, new_password}                  [escrita]

GET  /api/cards?category=                  lista cartões visíveis ao usuário
POST /api/cards                            cria cartão (compartilhado ou privado)     [escrita]
GET  /api/cards/{id}
PUT  /api/cards/{id}                                                                  [escrita]
DELETE /api/cards/{id}                                                                [escrita]

GET  /api/reviews/due?limit=               cartões vencidos para revisão
POST /api/reviews                          body: {card_id, grade} — aplica SM-2, grava log  [escrita]

GET  /api/scenarios                        lista cenários
GET  /api/scenarios/{slug}                 cenário com passos e opções
POST /api/scenarios/{slug}/attempts        inicia uma jogada                          [escrita]
POST /api/attempts/{id}/answers            body: {step_id, option_id} — acerto + explicação  [escrita]
GET  /api/attempts/{id}                    estado da jogada

GET  /api/dashboard                        números dos dois usuários lado a lado

POST /api/progress/reset                    zera o placar da conta (apaga review_logs e
                                            scenario_attempts; mantém review_states)     [escrita]
```

O usuário que age vem sempre do token — não há mais `?user=` nem header `X-User`.

## 8. Estrutura de pastas

```
backend/
  app/
    main.py            # instancia o FastAPI, monta os routers, seed opcional no boot
    config.py          # settings via variáveis de ambiente
    database.py        # engine, SessionLocal, Base, get_db
    auth.py            # hash de senha (argon2) e tokens JWT
    deps.py            # dependências: sessão, usuário do token, exigência de escrita
    models.py          # modelos SQLAlchemy (comentados)
    schemas.py         # modelos Pydantic (request/response)
    srs.py             # algoritmo SM-2 isolado e testável
    scoring.py         # regras de pontuação
    stats.py           # cálculo de streak e agregados do dashboard
    routers/
      auth.py  cards.py  reviews.py  scenarios.py  dashboard.py
    data/
      seed_data.py     # conteúdo: contas, ~75 cartões (15 temas), 7 cenários
    seed.py            # insere seed_data.py no banco (idempotente; --reset)
  tests/
    conftest.py        # banco :memory: isolado + TestClient + helpers de auth
    test_srs.py  test_auth.py  test_reviews.py  test_scenarios.py  test_dashboard.py
  requirements.txt
  .python-version      # 3.12.8 (deploy)
frontend/
  src/
    auth/AuthContext.jsx   # token JWT + sessão, rotas protegidas
    lib/  api.js  theme.js
    components/  Layout.jsx  Logo.jsx  ui.jsx  icons.jsx
    pages/  Login.jsx  Review.jsx  Scenarios.jsx  Dashboard.jsx  Settings.jsx
  public/  manifest.webmanifest  icon-192.png  icon-512.png
  vercel.json          # rewrite SPA -> index.html
docs/
  DESIGN.md
  screenshots/
render.yaml            # blueprint do backend
README.md
```
