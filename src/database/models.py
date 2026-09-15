from sqlalchemy.orm import Session

from database.schemas.models import ModelsT


def get_models_by_expertise(
    session: Session,
    expertise: str
) -> list[str]:

    models = (
        session.query(ModelsT)
        .filter(ModelsT.expertise == expertise)
        .all()
    )

    return [m.name for m in models]