"""Testes dos endpoints de revisão de flashcards."""

from datetime import timedelta

from app.stats import today_in_study_tz


def test_cartoes_novos_aparecem_como_vencidos(client, auth):
    response = client.get("/api/reviews/due", headers=auth("ivan"))
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(card["is_new"] for card in body)


def test_submeter_revisao_com_acerto_pontua_e_reagenda(client, auth):
    headers = auth("ivan")
    card_id = client.get("/api/reviews/due", headers=headers).json()[0]["id"]

    response = client.post(
        "/api/reviews", headers=headers, json={"card_id": card_id, "grade": 5}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["new_interval"] == 1
    assert body["points_earned"] == 10
    assert body["next_due_date"] == (today_in_study_tz() + timedelta(days=1)).isoformat()

    remaining = client.get("/api/reviews/due", headers=headers).json()
    assert card_id not in [card["id"] for card in remaining]


def test_revisao_com_erro_pontua_menos(client, auth):
    headers = auth("ivan")
    card_id = client.get("/api/reviews/due", headers=headers).json()[0]["id"]
    response = client.post(
        "/api/reviews", headers=headers, json={"card_id": card_id, "grade": 1}
    )
    assert response.json()["points_earned"] == 3


def test_progresso_e_independente_por_usuario(client, auth):
    ivan = auth("ivan")
    card_id = client.get("/api/reviews/due", headers=ivan).json()[0]["id"]
    client.post("/api/reviews", headers=ivan, json={"card_id": card_id, "grade": 5})

    gabriela_due = client.get("/api/reviews/due", headers=auth("gabriela")).json()
    assert card_id in [card["id"] for card in gabriela_due]


def test_sem_token_retorna_401(client, seeded):
    assert client.get("/api/reviews/due").status_code == 401


def test_cartao_inexistente_retorna_404(client, auth):
    response = client.post(
        "/api/reviews", headers=auth("ivan"), json={"card_id": 9999, "grade": 5}
    )
    assert response.status_code == 404
