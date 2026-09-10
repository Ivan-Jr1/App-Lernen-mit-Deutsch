"""Idiomas que o app oferece para estudo.

Fonte única da verdade: os códigos válidos para `Card.language`,
`Scenario.language` e `User.learning_language`, com o nome de exibição.
"""

# código ISO 639-1 -> nome exibido na UI (em português, como o resto da interface)
SUPPORTED_LANGUAGES: dict[str, str] = {
    "de": "Alemão",
    "en": "Inglês",
}

# Idioma padrão de contas e conteúdo — o app nasceu para estudar alemão.
DEFAULT_LANGUAGE = "de"


def is_supported(code: str) -> bool:
    return code in SUPPORTED_LANGUAGES
