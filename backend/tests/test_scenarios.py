"""Testes dos endpoints de cenários de burocracia."""


def _correct_and_wrong_option(step: dict) -> tuple[int, int]:
    # o endpoint não expõe is_correct; nas fixtures a opção 1 é sempre a certa
    ordered = sorted(step["options"], key=lambda o: o["option_order"])
    return ordered[0]["id"], ordered[1]["id"]


def test_listar_cenarios(client, seeded):
    response = client.get("/api/scenarios")
    assert response.status_code == 200
    assert response.json()[0]["slug"] == "anmeldung"


def test_detalhe_do_cenario_nao_expoe_resposta_correta(client, seeded):
    step = client.get("/api/scenarios/anmeldung").json()["steps"][0]
    assert "is_correct" not in step["options"][0]
    assert "explanation" not in step["options"][0]


def test_fluxo_completo_de_uma_jogada(client, seeded):
    scenario = client.get("/api/scenarios/anmeldung").json()
    attempt_id = client.post(
        "/api/scenarios/anmeldung/attempts", params={"user": "ivan"}
    ).json()["id"]

    # passo 1: erra de propósito
    correct_1, wrong_1 = _correct_and_wrong_option(scenario["steps"][0])
    first = client.post(
        f"/api/attempts/{attempt_id}/answers",
        params={"user": "ivan"},
        json={"step_id": scenario["steps"][0]["id"], "option_id": wrong_1},
    ).json()
    assert first["is_correct"] is False
    assert first["correct_option_id"] == correct_1
    assert first["explanation"]
    assert first["attempt_completed"] is False

    # passo 2: acerta e conclui a jogada
    correct_2, _ = _correct_and_wrong_option(scenario["steps"][1])
    last = client.post(
        f"/api/attempts/{attempt_id}/answers",
        params={"user": "ivan"},
        json={"step_id": scenario["steps"][1]["id"], "option_id": correct_2},
    ).json()
    assert last["attempt_completed"] is True
    assert last["points_earned"] == 15  # concluiu com 1 erro -> sem bônus

    attempt = client.get(f"/api/attempts/{attempt_id}", params={"user": "ivan"}).json()
    assert attempt["is_completed"] is True
    assert attempt["correct_count"] == 1


def test_responder_o_mesmo_passo_duas_vezes_falha(client, seeded):
    scenario = client.get("/api/scenarios/anmeldung").json()
    attempt_id = client.post(
        "/api/scenarios/anmeldung/attempts", params={"user": "ivan"}
    ).json()["id"]
    step_id = scenario["steps"][0]["id"]
    option_id = scenario["steps"][0]["options"][0]["id"]

    payload = {"step_id": step_id, "option_id": option_id}
    client.post(f"/api/attempts/{attempt_id}/answers", params={"user": "ivan"}, json=payload)
    second = client.post(
        f"/api/attempts/{attempt_id}/answers", params={"user": "ivan"}, json=payload
    )
    assert second.status_code == 409


def test_jogada_de_outro_usuario_retorna_404(client, seeded):
    attempt_id = client.post(
        "/api/scenarios/anmeldung/attempts", params={"user": "ivan"}
    ).json()["id"]
    response = client.get(f"/api/attempts/{attempt_id}", params={"user": "esposa"})
    assert response.status_code == 404
