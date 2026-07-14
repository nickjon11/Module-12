from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.security import hash_password


def get_user_by_username(
    db: Session,
    username: str,
) -> models.User | None:
    statement = select(models.User).where(
        models.User.username == username
    )

    return db.scalar(statement)


def get_user_by_email(
    db: Session,
    email: str,
) -> models.User | None:
    statement = select(models.User).where(
        models.User.email == email
    )

    return db.scalar(statement)


def create_user(
    db: Session,
    user_data: schemas.UserCreate,
) -> models.User:
    user = models.User(
        username=user_data.username,
        email=str(user_data.email),
        password_hash=hash_password(user_data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
