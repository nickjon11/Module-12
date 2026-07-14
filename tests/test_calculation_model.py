from app.models import Calculation


def test_create_calculation_model() -> None:
    calculation = Calculation(
        a=10,
        b=5,
        type="Add",
        result=15,
    )

    assert calculation.a == 10
    assert calculation.b == 5
    assert calculation.type == "Add"
    assert calculation.result == 15


def test_calculation_model_allows_user_id() -> None:
    calculation = Calculation(
        a=20,
        b=4,
        type="Divide",
        result=5,
        user_id=1,
    )

    assert calculation.user_id == 1


def test_calculation_model_user_id_is_optional() -> None:
    calculation = Calculation(
        a=7,
        b=3,
        type="Sub",
        result=4,
    )

    assert calculation.user_id is None