from sqlalchemy import select

from app.database import SessionLocal
from app.models import Calculation
from app.schemas import CalculationCreate
from app.services.calculation_factory import CalculationFactory


def test_insert_calculation_into_database(
    reset_database,
) -> None:
    calculation_data = CalculationCreate(
        a=20,
        b=4,
        type="Divide",
    )

    result = CalculationFactory.calculate(
        calculation_data.a,
        calculation_data.b,
        calculation_data.type,
    )

    calculation = Calculation(
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value,
        result=result,
    )

    with SessionLocal() as db:
        db.add(calculation)
        db.commit()
        db.refresh(calculation)

        calculation_id = calculation.id

    with SessionLocal() as db:
        stored_calculation = db.scalar(
            select(Calculation).where(
                Calculation.id == calculation_id
            )
        )

        assert stored_calculation is not None
        assert stored_calculation.a == 20
        assert stored_calculation.b == 4
        assert stored_calculation.type == "Divide"
        assert stored_calculation.result == 5


def test_insert_add_calculation(
    reset_database,
) -> None:
    calculation_data = CalculationCreate(
        a=12,
        b=8,
        type="Add",
    )

    result = CalculationFactory.calculate(
        calculation_data.a,
        calculation_data.b,
        calculation_data.type,
    )

    calculation = Calculation(
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value,
        result=result,
    )

    with SessionLocal() as db:
        db.add(calculation)
        db.commit()
        db.refresh(calculation)

        calculation_id = calculation.id

    with SessionLocal() as db:
        stored_calculation = db.scalar(
            select(Calculation).where(
                Calculation.id == calculation_id
            )
        )

        assert stored_calculation is not None
        assert stored_calculation.type == "Add"
        assert stored_calculation.result == 20