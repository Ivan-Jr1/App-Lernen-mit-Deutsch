"""Testes dos endpoints de revisão de flashcards."""

from datetime import timedelta

from app.stats import today_in_study_tz


def test_cartoes_novos_aparecem_como_vencidos(client, seeded):
    response = client.get("/api/reviews/due", params={"user": "ivan"})
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert all(card["is_new"] for card in body)


def test_submeter_revisao_com_acerto_pontua_e_reagenda(client, seeded):
    card_id = client.get("/api/reviews/due", params={"user": "ivan"}).json()[0]["id"]

    response = client.post(
        "/api/reviews", params={"user": "ivan"}, json={"card_id": card_id, "grade": 5}
    )
    assert response.status_code == 201
    body = response.json()
    assert body["new_interval"] == 1
    assert body["points_earned"] == 10
    assert body["next_due_date"] == (today_in_study_tz() + timedelta(days=1)).isoformat()

    # o cartão revisado sai da lista de vencidos de hoje
    remaining = client.get("/api/reviews/due", params={"user": "ivan"}).json()
    assert card_id not in [card["id"] for card in remaining]


def test_revisao_com_erro_pontua_menos(client, seeded):
    card_id = client.get("/api/reviews/due", params={"user": "ivan"}).json()[0]["id"]
    response = client.post(
        "/api/reviews", params={"user": "ivan"}, json={"card_id": card_id, "grade": 1}
    )
    assert response.json()["points_earned"] == 3


def test_progresso_e_independente_por_usuario(client, seeded):
    card_id = client.get("/api/reviews/due", params={"user": "ivan"}).json()[0]["id"]
    client.post("/api/reviews", params={"user": "ivan"}, json={"card_id": card_id, "grade": 5})

    # esposa ainda vê o mesmo cartão como novo
    esposa_due = client.get("/api/reviews/due", params={"user": "esposa"}).json()
    assert card_id in [card["id"] for card in esposa_due]


def test_usuario_ausente_retorna_400(client, seeded):
    assert client.get("/api/reviews/due").status_code == 400


def test_cartao_inexistente_retorna_404(client, seeded):
    response = client.post(
        "/api/reviews", params={"user": "ivan"}, json={"card_id": 9999, "grade": 5}
    )
    assert response.status_code == 404
