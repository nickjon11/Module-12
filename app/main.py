from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import crud, operations, schemas
from app.database import Base, engine, get_db
from app.security import verify_password


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Module 12 User and Calculation API",
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
    include_in_schema=False,
)
def create_user_legacy(
    user_data: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(user_data, db)


@app.post(
    "/users/register",
    response_model=schemas.UserRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
)
def register_user(
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


@app.post(
    "/users/login",
    response_model=schemas.LoginResponse,
    tags=["Users"],
)
def login_user(
    login_data: schemas.UserLogin,
    db: Session = Depends(get_db),
):
    user = crud.get_user_by_email(
        db,
        str(login_data.email),
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(
        login_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return {
        "message": "Login successful",
        "user_id": user.id,
        "username": user.username,
    }


@app.get(
    "/calculations",
    response_model=list[schemas.CalculationRead],
    tags=["Calculations"],
)
def browse_calculations(
    db: Session = Depends(get_db),
):
    return crud.get_calculations(db)


@app.get(
    "/calculations/{calculation_id}",
    response_model=schemas.CalculationRead,
    tags=["Calculations"],
)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
):
    calculation = crud.get_calculation(
        db,
        calculation_id,
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found.",
        )

    return calculation


@app.post(
    "/calculations",
    response_model=schemas.CalculationRead,
    status_code=status.HTTP_201_CREATED,
    tags=["Calculations"],
)
def add_calculation(
    calculation_data: schemas.CalculationCreate,
    db: Session = Depends(get_db),
):
    if calculation_data.user_id is not None:
        user = crud.get_user_by_id(
            db,
            calculation_data.user_id,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

    return crud.create_calculation(
        db,
        calculation_data,
    )


@app.put(
    "/calculations/{calculation_id}",
    response_model=schemas.CalculationRead,
    tags=["Calculations"],
)
def edit_calculation(
    calculation_id: int,
    calculation_data: schemas.CalculationUpdate,
    db: Session = Depends(get_db),
):
    calculation = crud.get_calculation(
        db,
        calculation_id,
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found.",
        )

    if calculation_data.user_id is not None:
        user = crud.get_user_by_id(
            db,
            calculation_data.user_id,
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found.",
            )

    return crud.update_calculation(
        db,
        calculation,
        calculation_data,
    )


@app.delete(
    "/calculations/{calculation_id}",
    response_model=schemas.DeleteResponse,
    tags=["Calculations"],
)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
):
    calculation = crud.get_calculation(
        db,
        calculation_id,
    )

    if calculation is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Calculation not found.",
        )

    crud.delete_calculation(
        db,
        calculation,
    )

    return {
        "message": "Calculation deleted successfully"
    }