import logging

logger = logging.getLogger(__name__)

def add(a: float, b: float) -> float:
    logger.info(f"Adding {a} + {b}")
    return a + b

def subtract(a: float, b: float) -> float:
    logger.info(f"Subtracting {a} - {b}")
    return a - b

def multiply(a: float, b: float) -> float:
    logger.info(f"Multiplying {a} * {b}")
    return a * b

def divide(a: float, b: float) -> float:
    logger.info(f"Dividing {a} / {b}")
    if b == 0:
        logger.error("Division by zero attempted")
        raise ValueError("Cannot divide by zero")
    return a / b