import pytest

from app.schemas import CalculationType
from app.services.calculation_factory import CalculationFactory


def test_add_operation() -> None:
    result = CalculationFactory.calculate(
        10,
        5,
        CalculationType.ADD,
    )

    assert result == 15


def test_subtract_operation() -> None:
    result = CalculationFactory.calculate(
        10,
        5,
        CalculationType.SUBTRACT,
    )

    assert result == 5


def test_multiply_operation() -> None:
    result = CalculationFactory.calculate(
        10,
        5,
        CalculationType.MULTIPLY,
    )

    assert result == 50


def test_divide_operation() -> None:
    result = CalculationFactory.calculate(
        10,
        5,
        CalculationType.DIVIDE,
    )

    assert result == 2


def test_factory_accepts_string_type() -> None:
    result = CalculationFactory.calculate(
        8,
        2,
        "Divide",
    )

    assert result == 4


def test_division_by_zero() -> None:
    with pytest.raises(
        ValueError,
        match="Cannot divide by zero",
    ):
        CalculationFactory.calculate(
            10,
            0,
            CalculationType.DIVIDE,
        )


def test_invalid_calculation_type() -> None:
    with pytest.raises(
        ValueError,
        match="Invalid calculation type",
    ):
        CalculationFactory.calculate(
            10,
            5,
            "Power",
        )