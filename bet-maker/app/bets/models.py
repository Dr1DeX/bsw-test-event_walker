from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class Bets(Base):
    __tablename__ = 'Bets'

    event_id: Mapped[str] = mapped_column(primary_key=True, index=True, nullable=False)
    sum_bet: Mapped[DECIMAL] = mapped_column(DECIMAL(precision=10, scale=2), nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
