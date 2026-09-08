"""Testes de autenticação: contas, claim de senha, login e visitante."""

from tests.conftest import TEST_PASSWORD


def test_contas_comecam_sem_senha(client, seeded):
    accounts = client.get("/api/auth/accounts").json()
    assert {a["username"] for a in accounts} == {"ivan", "gabriela"}  # visitante fica de fora
    assert all(a["claimed"] is False for a in accounts)


def test_primeiro_acesso_define_a_senha_e_retorna_token(client, seeded):
    response = client.post(
        "/api/auth/claim", json={"username": "ivan", "password": TEST_PASSWORD}
    )
    assert response.status_code == 201
    assert response.json()["user"]["readonly"] is False
    assert response.json()["access_token"]

    accounts = client.get("/api/auth/accounts").json()
    assert next(a for a in accounts if a["username"] == "ivan")["claimed"] is True


def test_claim_duas_vezes_falha(client, seeded):
    client.post("/api/auth/claim", json={"username": "ivan", "password": TEST_PASSWORD})
    again = client.post(
        "/api/auth/claim", json={"username": "ivan", "password": "outra-senha"}
    )
    assert again.status_code == 409


def test_login_com_senha_certa_e_errada(client, seeded):
    client.post("/api/auth/claim", json={"username": "ivan", "password": TEST_PASSWORD})

    ok = client.post("/api/auth/login", json={"username": "ivan", "password": TEST_PASSWORD})
    assert ok.status_code == 200

    bad = client.post("/api/auth/login", json={"username": "ivan", "password": "errada"})
    assert bad.status_code == 401


def test_login_antes_de_definir_senha_falha(client, seeded):
    response = client.post(
        "/api/auth/login", json={"username": "gabriela", "password": TEST_PASSWORD}
    )
    assert response.status_code == 401


def test_visitante_le_mas_nao_escreve(client, guest_headers):
    assert client.get("/api/scenarios", headers=guest_headers).status_code == 200

    card_id = client.get("/api/reviews/due", headers=guest_headers).json()["cards"][0]["id"]
    blocked = client.post(
        "/api/reviews", headers=guest_headers, json={"card_id": card_id, "grade": 5}
    )
    assert blocked.status_code == 403


def test_token_invalido_retorna_401(client, seeded):
    response = client.get(
        "/api/reviews/due", headers={"Authorization": "Bearer nao-e-um-token"}
    )
    assert response.status_code == 401


def test_atualizar_perfil_nome_e_foto(client, auth):
    headers = auth("ivan")
    response = client.patch(
        "/api/auth/me",
        headers=headers,
        json={"display_name": "Ivan B.", "avatar_url": "data:image/png;base64,AAAA"},
    )
    assert response.status_code == 200
    assert response.json()["display_name"] == "Ivan B."

    me = client.get("/api/auth/me", headers=headers).json()
    assert me["avatar_url"] == "data:image/png;base64,AAAA"


def test_atualizar_meta_diaria(client, auth):
    headers = auth("ivan")
    assert client.get("/api/auth/me", headers=headers).json()["daily_goal"] == 20

    updated = client.patch("/api/auth/me", headers=headers, json={"daily_goal": 30})
    assert updated.status_code == 200
    assert updated.json()["daily_goal"] == 30

    fora_do_limite = client.patch("/api/auth/me", headers=headers, json={"daily_goal": 0})
    assert fora_do_limite.status_code == 422


def test_visitante_nao_edita_perfil(client, guest_headers):
    response = client.patch(
        "/api/auth/me", headers=guest_headers, json={"display_name": "Hacker"}
    )
    assert response.status_code == 403


def test_trocar_senha(client, auth):
    headers = auth("ivan")  # claim define TEST_PASSWORD

    wrong = client.post(
        "/api/auth/change-password",
        headers=headers,
        json={"current_password": "errada", "new_password": "novasenha123"},
    )
    assert wrong.status_code == 403

    ok = client.post(
        "/api/auth/change-password",
        headers=headers,
        json={"current_password": "senha-de-teste", "new_password": "novasenha123"},
    )
    assert ok.status_code == 204

    assert (
        client.post(
            "/api/auth/login", json={"username": "ivan", "password": "novasenha123"}
        ).status_code
        == 200
    )
