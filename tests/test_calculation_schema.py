import pytest
from pydantic import ValidationError

from app.schemas import CalculationCreate, CalculationType


def test_valid_add_schema() -> None:
    calculation = CalculationCreate(
        a=10,
        b=5,
        type="Add",
    )

    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == CalculationType.ADD


def test_valid_subtract_schema() -> None:
    calculation = CalculationCreate(
        a=10,
        b=5,
        type="Sub",
    )

    assert calculation.type == CalculationType.SUBTRACT


def test_valid_multiply_schema() -> None:
    calculation = CalculationCreate(
        a=10,
        b=5,
        type="Multiply",
    )

    assert calculation.type == CalculationType.MULTIPLY


def test_valid_divide_schema() -> None:
    calculation = CalculationCreate(
        a=10,
        b=5,
        type="Divide",
    )

    assert calculation.type == CalculationType.DIVIDE


def test_invalid_type_schema() -> None:
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b=5,
            type="Power",
        )


def test_division_by_zero_schema() -> None:
    with pytest.raises(
        ValidationError,
        match="Cannot divide by zero",
    ):
        CalculationCreate(
            a=10,
            b=0,
            type="Divide",
        )


def test_invalid_first_operand() -> None:
    with pytest.raises(ValidationError):
        CalculationCreate(
            a="not-a-number",
            b=5,
            type="Add",
        )


def test_invalid_second_operand() -> None:
    with pytest.raises(ValidationError):
        CalculationCreate(
            a=10,
            b="not-a-number",
            type="Add",
        )


def test_numeric_strings_are_converted() -> None:
    calculation = CalculationCreate(
        a="10",
        b="5",
        type="Add",
    )

    assert calculation.a == 10.0
    assert calculation.b == 5.0