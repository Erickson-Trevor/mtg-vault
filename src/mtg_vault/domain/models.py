from datetime import datetime, timezone
from sqlalchemy import String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class Deck(Base):
    __tablename__ = "decks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    commander: Mapped[str] = mapped_column(String(100))

    cards = relationship("VaultCard", back_populates="deck")

class VaultCard(Base):
    __tablename__ = "vault_ cards"

    id: Mapped[int] = mapped_column(primary_key=True)

    deck_id: Mapped[int] = mapped_column(ForeignKey("decks.id"), nullable=True)

    name: Mapped[str] = mapped_column(String(100))
    set_code: Mapped[str] = mapped_column(String(10, nullable=True))
    scryfall_id: Mapped[str] = mapped_column(String(50, nullable=True))
    mana_cost: Mapped[str] = mapped_column(String(50, nullable=True))
    type_line: Mapped[str] = mapped_column(String(100, nullable=True))

    physical_location: Mapped[str] = mapped_column(String(100))
    is_proxy: Mapped[bool] = mapped_column(Boolean, default=False)
    usd_price: Mapped[float] = mapped_column(Float, nullable=True)

    last_price_update: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=True
    )

    deck = relationship("Deck", back_populates="cards")