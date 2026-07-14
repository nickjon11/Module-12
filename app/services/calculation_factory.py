from abc import ABC, abstractmethod

from app.schemas import CalculationType


class CalculationOperation(ABC):
    @abstractmethod
    def calculate(self, a: float, b: float) -> float:
        raise NotImplementedError


class AddOperation(CalculationOperation):
    def calculate(self, a: float, b: float) -> float:
        return a + b


class SubtractOperation(CalculationOperation):
    def calculate(self, a: float, b: float) -> float:
        return a - b


class MultiplyOperation(CalculationOperation):
    def calculate(self, a: float, b: float) -> float:
        return a * b


class DivideOperation(CalculationOperation):
    def calculate(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Cannot divide by zero")

        return a / b


class CalculationFactory:
    operation_classes = {
        CalculationType.ADD: AddOperation,
        CalculationType.SUBTRACT: SubtractOperation,
        CalculationType.MULTIPLY: MultiplyOperation,
        CalculationType.DIVIDE: DivideOperation,
    }

    @classmethod
    def create_operation(
        cls,
        calculation_type: CalculationType | str,
    ) -> CalculationOperation:
        try:
            normalized_type = CalculationType(calculation_type)
        except ValueError as error:
            raise ValueError(
                f"Invalid calculation type: {calculation_type}"
            ) from error

        operation_class = cls.operation_classes.get(normalized_type)

        if operation_class is None:
            raise ValueError(
                f"Invalid calculation type: {calculation_type}"
            )

        return operation_class()

    @classmethod
    def calculate(
        cls,
        a: float,
        b: float,
        calculation_type: CalculationType | str,
    ) -> float:
        operation = cls.create_operation(calculation_type)

        return operation.calculate(a, b)