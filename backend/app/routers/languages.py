"""Idiomas disponíveis para estudo. Usado pela tela de Configurações."""

from fastapi import APIRouter

from app.deps import Reader
from app.languages import SUPPORTED_LANGUAGES
from app.schemas import LanguageOut

router = APIRouter(prefix="/api/languages", tags=["languages"])


@router.get("", response_model=list[LanguageOut])
def list_languages(current_user: Reader):
    return [LanguageOut(code=code, name=name) for code, name in SUPPORTED_LANGUAGES.items()]
