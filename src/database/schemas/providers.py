from sqlalchemy import (
    String,
    Boolean
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from database.schemas.base import Base


class ProvidersT(Base):
    __tablename__ = "providers"

    id: Mapped[str] = mapped_column(
        String(50),
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True
    )

    base_url: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True
    )

    langchain_con: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=False
    )

    host: Mapped[str] = mapped_column(
        String(30),
        nullable=True,
        unique=False
    )

    mac_address: Mapped[str] = mapped_column(
        String(30),
        nullable=True,
        unique=True
    )

    internal: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    requires_api_key: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )