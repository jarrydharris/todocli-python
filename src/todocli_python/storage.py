from datetime import datetime
from sqlalchemy import DateTime, Engine, create_engine, String, Boolean, func
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

MAX_DESC_CHARS = 1000


class Base(DeclarativeBase):
    pass


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(MAX_DESC_CHARS))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


def init_db() -> Engine:
    engine = create_engine("sqlite:///src/todocli_python/tasks.db")
    Base.metadata.create_all(engine)
    return engine
