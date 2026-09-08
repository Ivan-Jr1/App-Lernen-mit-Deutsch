"""Testes do dashboard do casal."""


def _complete_scenario(client, headers) -> None:
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


def test_dashboard_agrega_pontos_streak_e_totais(client, auth):
    ivan = auth("ivan")
    card_ids = [c["id"] for c in client.get("/api/reviews/due", headers=ivan).json()["cards"]]
    for card_id in card_ids:
        client.post("/api/reviews", headers=ivan, json={"card_id": card_id, "grade": 5})
    _complete_scenario(client, ivan)

    dashboard = client.get("/api/dashboard", headers=ivan).json()
    ivan_row = next(u for u in dashboard["users"] if u["username"] == "ivan")
    gabriela_row = next(u for u in dashboard["users"] if u["username"] == "gabriela")

    # 2 revisões x 10 + cenário 2/2 (15 + 5 bônus) = 40
    assert ivan_row["total_points"] == 40
    assert ivan_row["total_cards_reviewed"] == 2
    assert ivan_row["scenarios_completed"] == 1
    assert ivan_row["current_streak"] == 1
    assert ivan_row["longest_streak"] == 1
    assert ivan_row["cards_due_today"] == 0
    assert ivan_row["reviewed_today"] == 2
    assert ivan_row["daily_goal"] == 20

    assert gabriela_row["total_points"] == 0
    assert gabriela_row["current_streak"] == 0
    assert gabriela_row["cards_due_today"] == 2
    assert gabriela_row["reviewed_today"] == 0


def test_dashboard_nao_lista_o_visitante(client, guest_headers):
    dashboard = client.get("/api/dashboard", headers=guest_headers).json()
    assert {u["username"] for u in dashboard["users"]} == {"ivan", "gabriela"}
