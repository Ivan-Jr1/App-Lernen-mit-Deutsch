"""Testes do dashboard do casal."""


def _complete_scenario(client, user: str) -> None:
    scenario = client.get("/api/scenarios/anmeldung").json()
    attempt_id = client.post(
        "/api/scenarios/anmeldung/attempts", params={"user": user}
    ).json()["id"]
    for step in scenario["steps"]:
        correct = sorted(step["options"], key=lambda o: o["option_order"])[0]["id"]
        client.post(
            f"/api/attempts/{attempt_id}/answers",
            params={"user": user},
            json={"step_id": step["id"], "option_id": correct},
        )


def test_dashboard_agrega_pontos_streak_e_totais(client, seeded):
    card_ids = [c["id"] for c in client.get("/api/reviews/due", params={"user": "ivan"}).json()]
    for card_id in card_ids:
        client.post("/api/reviews", params={"user": "ivan"}, json={"card_id": card_id, "grade": 5})
    _complete_scenario(client, "ivan")

    dashboard = client.get("/api/dashboard").json()
    ivan = next(u for u in dashboard["users"] if u["username"] == "ivan")
    esposa = next(u for u in dashboard["users"] if u["username"] == "esposa")

    # 2 revisões x 10 + cenário 2/2 (15 + 5 bônus) = 40
    assert ivan["total_points"] == 40
    assert ivan["total_cards_reviewed"] == 2
    assert ivan["scenarios_completed"] == 1
    assert ivan["current_streak"] == 1
    assert ivan["longest_streak"] == 1
    assert ivan["cards_due_today"] == 0

    # esposa não estudou: tudo zerado, mas os cartões compartilhados seguem vencidos
    assert esposa["total_points"] == 0
    assert esposa["current_streak"] == 0
    assert esposa["cards_due_today"] == 2
