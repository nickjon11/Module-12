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


def get_user_by_id(
    db: Session,
    user_id: int,
) -> models.User | None:
    return db.get(models.User, user_id)


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


def calculate_result(
    a: float,
    b: float,
    calculation_type: schemas.CalculationType,
) -> float:
    if calculation_type == schemas.CalculationType.ADD:
        return a + b

    if calculation_type == schemas.CalculationType.SUBTRACT:
        return a - b

    if calculation_type == schemas.CalculationType.MULTIPLY:
        return a * b

    if calculation_type == schemas.CalculationType.DIVIDE:
        if b == 0:
            raise ValueError("Cannot divide by zero")

        return a / b

    raise ValueError("Unsupported calculation type")


def get_calculations(
    db: Session,
) -> list[models.Calculation]:
    statement = select(models.Calculation).order_by(
        models.Calculation.id
    )

    return list(db.scalars(statement).all())


def get_calculation(
    db: Session,
    calculation_id: int,
) -> models.Calculation | None:
    return db.get(models.Calculation, calculation_id)


def create_calculation(
    db: Session,
    calculation_data: schemas.CalculationCreate,
) -> models.Calculation:
    result = calculate_result(
        calculation_data.a,
        calculation_data.b,
        calculation_data.type,
    )

    calculation = models.Calculation(
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value,
        result=result,
        user_id=calculation_data.user_id,
    )

    db.add(calculation)
    db.commit()
    db.refresh(calculation)

    return calculation


def update_calculation(
    db: Session,
    calculation: models.Calculation,
    calculation_data: schemas.CalculationUpdate,
) -> models.Calculation:
    calculation.a = calculation_data.a
    calculation.b = calculation_data.b
    calculation.type = calculation_data.type.value
    calculation.result = calculate_result(
        calculation_data.a,
        calculation_data.b,
        calculation_data.type,
    )
    calculation.user_id = calculation_data.user_id

    db.commit()
    db.refresh(calculation)

    return calculation


def delete_calculation(
    db: Session,
    calculation: models.Calculation,
) -> None:
    db.delete(calculation)
    db.commit()