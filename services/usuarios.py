from sqlalchemy.orm import Session

from models import Usuario


def get_user_by_email(email: str, db: Session) -> Usuario | None:
    return db.query(Usuario).filter(Usuario.email == email.lower()).first()
