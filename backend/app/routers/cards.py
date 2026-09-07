"""CRUD de flashcards. Um cartão é visível ao usuário quando é compartilhado
(`owner_id` nulo) ou pertence a ele."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import or_, select

from app.deps import DbSession, Reader, Writer
from app.models import Card, User
from app.schemas import CardCreate, CardOut, CardUpdate

router = APIRouter(prefix="/api/cards", tags=["cards"])


def _visible_to(user: User):
    return or_(Card.owner_id.is_(None), Card.owner_id == user.id)


def _load_visible_card(db: DbSession, card_id: int, user: User) -> Card:
    card = db.get(Card, card_id)
    if card is None or (card.owner_id is not None and card.owner_id != user.id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Cartão não encontrado.")
    return card


@router.get("", response_model=list[CardOut])
def list_cards(db: DbSession, current_user: Reader, category: str | None = None):
    query = select(Card).where(_visible_to(current_user)).order_by(Card.id)
    if category:
        query = query.where(Card.category == category)
    return list(db.scalars(query))


@router.post("", response_model=CardOut, status_code=status.HTTP_201_CREATED)
def create_card(payload: CardCreate, db: DbSession, current_user: Writer):
    owner_id: int | None = None
    if payload.owner_username:
        owner = db.scalar(select(User).where(User.username == payload.owner_username))
        if owner is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Dono informado não existe.")
        owner_id = owner.id

    card = Card(
        front_pt=payload.front_pt,
        back_de=payload.back_de,
        phonetic_hint=payload.phonetic_hint,
        category=payload.category,
        owner_id=owner_id,
    )
    db.add(card)
    db.commit()
    db.refresh(card)
    return card


@router.get("/{card_id}", response_model=CardOut)
def get_card(card_id: int, db: DbSession, current_user: Reader):
    return _load_visible_card(db, card_id, current_user)


@router.put("/{card_id}", response_model=CardOut)
def update_card(card_id: int, payload: CardUpdate, db: DbSession, current_user: Writer):
    card = _load_visible_card(db, card_id, current_user)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(card, field, value)
    db.commit()
    db.refresh(card)
    return card


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: DbSession, current_user: Writer):
    card = _load_visible_card(db, card_id, current_user)
    db.delete(card)
    db.commit()
