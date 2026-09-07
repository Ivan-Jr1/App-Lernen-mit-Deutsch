"""Testes do reset de placar."""


def _study_a_bit(client, headers):
    for card in client.get("/api/reviews/due", headers=headers).json()[:2]:
        client.post("/api/reviews", headers=headers, json={"card_id": card["id"], "grade": 5})
    scenario = client.get("/api/scenarios/anmeldung", headers=headers).json()
    attempt_id = client.post(
        "/api/scenarios/anmeldung/attempts", headers=headers
    ).json()["id"]
    for step in scenario["steps"]:
        correct = sorted(step["options"], key=lambda o: o["option_order"])[0]["id"]
        client.post(
            f"/api/attempts/{attempt_id}/answers",
            headers=headers,
            json={"step_id": step["id"], "option_id": correct},
        )


def test_reset_zera_o_placar_mas_mantem_a_agenda(client, auth):
    ivan, gabriela = auth("ivan"), auth("gabriela")
    _study_a_bit(client, ivan)
    _study_a_bit(client, gabriela)

    before = client.get("/api/dashboard", headers=ivan).json()
    assert next(u for u in before["users"] if u["username"] == "ivan")["total_points"] > 0

    assert client.post("/api/progress/reset", headers=ivan).status_code == 204

    after = client.get("/api/dashboard", headers=ivan).json()
    ivan_row = next(u for u in after["users"] if u["username"] == "ivan")
    assert ivan_row["total_points"] == 0
    assert ivan_row["current_streak"] == 0
    assert ivan_row["total_cards_reviewed"] == 0
    assert ivan_row["scenarios_completed"] == 0
    # agenda mantida: os 2 cartões revisados não voltam para a fila de hoje
    assert ivan_row["cards_due_today"] == 0

    # a conta da gabriela não é afetada
    gabriela_row = next(u for u in after["users"] if u["username"] == "gabriela")
    assert gabriela_row["total_points"] > 0


def test_visitante_nao_reseta(client, guest_headers):
    assert client.post("/api/progress/reset", headers=guest_headers).status_code == 403
