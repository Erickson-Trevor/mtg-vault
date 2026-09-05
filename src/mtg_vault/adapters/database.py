from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mtg_vault.domain.models import Base, VaultCard

# Establish the SQLite connection
ENGINE = create_engine("sqlite:///mtg_vault.db", echo=False)

# Create a factory for generating new database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)

def init_db():
    """Generates the physical database tables based on domain models."""
    Base.metadata.create_all(bind=ENGINE)

class CardRepository:
    """Handles all database transactions for VaultCard objects."""

    def __init__(self, session):
        self.session = session

    def save(self, card: VaultCard) -> VaultCard:
        """Saves a new card to the database and commits the transaction."""
        self.session.add(card)
        self.session.commit()
        self.session.refresh(card)
        return card