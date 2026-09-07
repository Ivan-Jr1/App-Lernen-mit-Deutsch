"""Testes dos endpoints de cenários de burocracia."""


def _correct_and_wrong_option(step: dict) -> tuple[int, int]:
    # o endpoint não expõe is_correct; nas fixtures a opção 1 é sempre a certa
    ordered = sorted(step["options"], key=lambda o: o["option_order"])
    return ordered[0]["id"], ordered[1]["id"]


def test_listar_cenarios(client, auth):
    response = client.get("/api/scenarios", headers=auth("ivan"))
    assert response.status_code == 200
    assert response.json()[0]["slug"] == "anmeldung"


def test_detalhe_do_cenario_nao_expoe_resposta_correta(client, auth):
    step = client.get("/api/scenarios/anmeldung", headers=auth("ivan")).json()["steps"][0]
    assert "is_correct" not in step["options"][0]
    assert "explanation" not in step["options"][0]


def test_fluxo_completo_de_uma_jogada(client, auth):
    headers = auth("ivan")
    scenario = client.get("/api/scenarios/anmeldung", headers=headers).json()
    attempt_id = client.post(
        "/api/scenarios/anmeldung/attempts", headers=headers
    ).json()["id"]

    correct_1, wrong_1 = _correct_and_wrong_option(scenario["steps"][0])
    first = client.post(
        f"/api/attempts/{attempt_id}/answers",
        headers=headers,
        json={"step_id": scenario["steps"][0]["id"], "option_id": wrong_1},
    ).json()
    assert first["is_correct"] is False
    assert first["correct_option_id"] == correct_1
    assert first["explanation"]
    assert first["attempt_completed"] is False

    correct_2, _ = _correct_and_wrong_option(scenario["steps"][1])
    last = client.post(
        f"/api/attempts/{attempt_id}/answers",
        headers=headers,
        json={"step_id": scenario["steps"][1]["id"], "option_id": correct_2},
    ).json()
    assert last["attempt_completed"] is True
    assert last["points_earned"] == 15  # concluiu com 1 erro -> sem bônus

    attempt = client.get(f"/api/attempts/{attempt_id}", headers=headers).json()
    assert attempt["is_completed"] is True
    assert attempt["correct_count"] == 1


def test_responder_o_mesmo_passo_duas_vezes_falha(client, auth):
    headers = auth("ivan")
    scenario = client.get("/api/scenarios/anmeldung", headers=headers).json()
    attempt_id = client.post(
        "/api/scenarios/anmeldung/attempts", headers=headers
    ).json()["id"]
    step_id = scenario["steps"][0]["id"]
    option_id = scenario["steps"][0]["options"][0]["id"]

    payload = {"step_id": step_id, "option_id": option_id}
    client.post(f"/api/attempts/{attempt_id}/answers", headers=headers, json=payload)
    second = client.post(
        f"/api/attempts/{attempt_id}/answers", headers=headers, json=payload
    )
    assert second.status_code == 409


def test_jogada_de_outro_usuario_retorna_404(client, auth):
    attempt_id = client.post(
        "/api/scenarios/anmeldung/attempts", headers=auth("ivan")
    ).json()["id"]
    response = client.get(f"/api/attempts/{attempt_id}", headers=auth("esposa"))
    assert response.status_code == 404
