"""Regras de pontuação do modo casal. Centralizadas para poderem evoluir sem
caçar constantes pelos endpoints."""

from app.srs import PASSING_GRADE

POINTS_REVIEW_PASS = 10  # revisão de cartão com nota >= 3
POINTS_REVIEW_FAIL = 3  # revisão com nota < 3 — ainda recompensa por aparecer
POINTS_SCENARIO_COMPLETE = 15
POINTS_SCENARIO_FLAWLESS_BONUS = 5  # bônus por concluir sem nenhum erro


def points_for_review(grade: int) -> int:
    return POINTS_REVIEW_PASS if grade >= PASSING_GRADE else POINTS_REVIEW_FAIL


def points_for_scenario(correct_count: int, total_steps: int) -> int:
    points = POINTS_SCENARIO_COMPLETE
    if correct_count == total_steps:
        points += POINTS_SCENARIO_FLAWLESS_BONUS
    return points
