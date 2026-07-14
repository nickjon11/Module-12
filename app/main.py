from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, models, operations, schemas
from app.database import Base, engine, get_db


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Module 10 Secure Calculator API",
    version="1.0.0",
)


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "FastAPI Calculator is running"}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.get("/add")
def add_numbers(a: float, b: float) -> dict[str, float]:
    return {"result": operations.add(a, b)}


@app.get("/subtract")
def subtract_numbers(a: float, b: float) -> dict[str, float]:
    return {"result": operations.subtract(a, b)}


@app.get("/multiply")
def multiply_numbers(a: float, b: float) -> dict[str, float]:
    return {"result": operations.multiply(a, b)}


@app.get("/divide")
def divide_numbers(a: float, b: float) -> dict[str, float]:
    try:
        result = operations.divide(a, b)
        return {"result": result}
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


@app.post(
    "/users",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    existing_username = crud.get_user_by_username(
        db,
        user_data.username,
    )

    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists.",
        )

    existing_email = crud.get_user_by_email(
        db,
        str(user_data.email),
    )

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists.",
        )

    try:
        return crud.create_user(db, user_data)

    except IntegrityError as exc:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username or email already exists.",
        ) from exc
