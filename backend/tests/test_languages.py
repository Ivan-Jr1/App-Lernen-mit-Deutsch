"""Testes do idioma de estudo: endpoint de idiomas, troca no perfil e o filtro
de idioma na fila de revisão e na lista de cenários."""

import pytest

from app.models import Card, Scenario, ScenarioOption, ScenarioStep


@pytest.fixture
def with_english_content(db_session, seeded):
    """Acrescenta ao cenário base (alemão) um cartão e um cenário em inglês."""
    db_session.add(
        Card(front_pt="Obrigado", back_target="Thank you", category="básico", language="en")
    )
    scenario = Scenario(
        slug="airport-check-in",
        title="Check-in no aeroporto",
        description="No balcão de check-in.",
        category="viagem",
        language="en",
    )
    db_session.add(scenario)
    db_session.flush()
    step = ScenarioStep(
        scenario_id=scenario.id, step_order=1, speaker_text_target="May I see your passport?"
    )
    db_session.add(step)
    db_session.flush()
    db_session.add_all(
        [
            ScenarioOption(
                step_id=step.id, option_text_target="Here you are.", is_correct=True,
                explanation="Forma natural.", option_order=1,
            ),
            ScenarioOption(
                step_id=step.id, option_text_target="Why?", is_correct=False,
                explanation="Questionar atrasa.", option_order=2,
            ),
        ]
    )
    db_session.commit()


def test_lista_de_idiomas(client, auth):
    response = client.get("/api/languages", headers=auth("ivan"))
    assert response.status_code == 200
    codes = {row["code"] for row in response.json()}
    assert {"de", "en"} <= codes


def test_conta_comeca_em_alemao(client, auth):
    me = client.get("/api/auth/me", headers=auth("ivan")).json()
    assert me["learning_language"] == "de"


def test_trocar_idioma_no_perfil(client, auth):
    response = client.patch(
        "/api/auth/me", headers=auth("ivan"), json={"learning_language": "en"}
    )
    assert response.status_code == 200
    assert response.json()["learning_language"] == "en"


def test_idioma_invalido_e_recusado(client, auth):
    response = client.patch(
        "/api/auth/me", headers=auth("ivan"), json={"learning_language": "fr"}
    )
    assert response.status_code == 422


def test_fila_de_revisao_segue_o_idioma_ativo(client, auth, with_english_content):
    headers = auth("ivan")

    de_cards = client.get("/api/reviews/due", headers=headers).json()["cards"]
    assert de_cards and all(c["language"] == "de" for c in de_cards)

    client.patch("/api/auth/me", headers=headers, json={"learning_language": "en"})
    en_cards = client.get("/api/reviews/due", headers=headers).json()["cards"]
    assert en_cards and all(c["language"] == "en" for c in en_cards)


def test_lista_de_cenarios_segue_o_idioma_ativo(client, auth, with_english_content):
    headers = auth("ivan")

    assert {s["slug"] for s in client.get("/api/scenarios", headers=headers).json()} == {
        "anmeldung"
    }

    client.patch("/api/auth/me", headers=headers, json={"learning_language": "en"})
    assert {s["slug"] for s in client.get("/api/scenarios", headers=headers).json()} == {
        "airport-check-in"
    }


def test_visitante_ve_alemao_por_padrao(client, guest_headers, with_english_content):
    scenarios = client.get("/api/scenarios", headers=guest_headers).json()
    assert {s["slug"] for s in scenarios} == {"anmeldung"}
