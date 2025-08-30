from sqlalchemy.orm import Mapped, mapped_column
from database.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, )
    title: Mapped[str] = mapped_column(max_length=100)
    description: Mapped[str | None] = mapped_column(nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)
