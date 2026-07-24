from datetime import datetime
from sqlalchemy import (
    UUID,
    text,
    String,
    DateTime,
    CheckConstraint,
    Boolean,
    ForeignKey,
    func,
    UniqueConstraint
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship
)
import uuid

class Base(DeclarativeBase):
    pass


class ApiKeys(Base):
    __tablename__ = 'api_keys'
    
    __table_args__ = (
        CheckConstraint(
            "key_type IN ('User', 'Application')",
            name="check_key_type"
        ),
        UniqueConstraint(
            'client', 'owner_email',
            name="uq_client_owner_email"
        )
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=lambda: uuid.uuid4()
    )

    api_key_hash: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    client: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    key_type: Mapped[str] = mapped_column(
        String(10),
        nullable=False
    )

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    require_jwt: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    require_external_id: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("true")
    )

    owner_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    hmac_secret_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    created_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=text("current_user")
    )


class Users(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=lambda: uuid.uuid4()
    )

    person_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("persons.id"),
        nullable=False
    )

    api_key_id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        ForeignKey("api_keys.id"),
        nullable=False
    )

    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    created_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=text("current_user")
    )

    # Relationships
    person: Mapped["Persons"] = relationship(back_populates="memberships")


class Persons(Base):
    __tablename__ = "persons"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID,
        primary_key=True,
        default=lambda: uuid.uuid4()
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    last_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    created_by: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        server_default=text("current_user")
    )

    # Relationships
    memberships: Mapped[list["Users"]] = relationship(back_populates="person")