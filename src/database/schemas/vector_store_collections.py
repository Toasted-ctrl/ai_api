from sqlalchemy import String, UUID, Integer, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from typing import List
import uuid

from database.schemas.base import Base


class VectorStoreCollectionT(Base):
    __tablename__ = "vector_store_collection"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=lambda: uuid.uuid4()
    )

    name: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    vector_store_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        unique=True,
        nullable=False
    )

    e_provider: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    e_dimensions: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    e_model: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    access_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    required_filters: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list
    )