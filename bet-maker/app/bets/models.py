from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


class Bets(Base):
    __tablename__ = 'Bets'

    event_id: Mapped[int] = mapped_column(primary_key=True, index=True, nullable=False)
    ratio: Mapped[float] = mapped_column(nullable=False)
    deadline: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
