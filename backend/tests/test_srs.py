"""Testes unitários do algoritmo SM-2 (sem banco, sem HTTP)."""

import pytest

from app.srs import MIN_EASE_FACTOR, initial_state, review


def test_primeiro_acerto_agenda_para_um_dia():
    result = review(initial_state(), grade=5)
    assert result.repetitions == 1
    assert result.interval_days == 1


def test_segundo_acerto_agenda_para_seis_dias():
    state = review(initial_state(), grade=5)
    result = review(state, grade=5)
    assert result.repetitions == 2
    assert result.interval_days == 6


def test_terceiro_acerto_multiplica_pelo_ease_factor():
    state = review(review(initial_state(), grade=5), grade=5)  # reps 2, interval 6, EF já subiu
    result = review(state, grade=4)
    assert result.repetitions == 3
    assert result.interval_days == round(6 * state.ease_factor)  # usa o EF anterior à revisão


def test_erro_reinicia_repeticoes_e_intervalo():
    state = review(review(initial_state(), grade=5), grade=5)
    result = review(state, grade=2)
    assert result.repetitions == 0
    assert result.interval_days == 1


def test_ease_factor_nunca_fica_abaixo_do_piso():
    state = initial_state()
    for _ in range(10):
        state = review(state, grade=0)
    assert state.ease_factor == pytest.approx(MIN_EASE_FACTOR)


@pytest.mark.parametrize("grade", [-1, 6, 99])
def test_nota_fora_do_intervalo_levanta_erro(grade):
    with pytest.raises(ValueError):
        review(initial_state(), grade=grade)
