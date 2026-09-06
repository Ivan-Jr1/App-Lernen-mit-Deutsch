"""Algoritmo de repetição espaçada SM-2 (o mesmo princípio usado pelo Anki).

Isolado de FastAPI e do banco para ser testável de forma pura. Referência:
https://super-memory.com/english/ol/sm2.htm
"""

from dataclasses import dataclass

MIN_EASE_FACTOR = 2.5 - 1.2  # 1.3 — piso do fator de facilidade definido pelo SM-2
PASSING_GRADE = 3  # nota mínima para o cartão "avançar" no intervalo


@dataclass(frozen=True)
class Sm2State:
    """Estado de agendamento de um cartão para um usuário."""

    repetitions: int
    ease_factor: float
    interval_days: int


def initial_state() -> Sm2State:
    """Estado de um cartão nunca revisado."""
    return Sm2State(repetitions=0, ease_factor=2.5, interval_days=0)


def review(state: Sm2State, grade: int) -> Sm2State:
    """Aplica uma revisão com nota `grade` (0 a 5) e devolve o novo estado.

    O fator de facilidade é sempre recalculado. Nota abaixo de 3 zera as
    repetições e reagenda o cartão para o dia seguinte.
    """
    if not 0 <= grade <= 5:
        raise ValueError("grade deve estar entre 0 e 5")

    new_ease = state.ease_factor + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
    new_ease = max(new_ease, MIN_EASE_FACTOR)

    if grade < PASSING_GRADE:
        return Sm2State(repetitions=0, ease_factor=new_ease, interval_days=1)

    if state.repetitions == 0:
        new_interval = 1
    elif state.repetitions == 1:
        new_interval = 6
    else:
        new_interval = round(state.interval_days * state.ease_factor)

    return Sm2State(
        repetitions=state.repetitions + 1,
        ease_factor=new_ease,
        interval_days=new_interval,
    )
