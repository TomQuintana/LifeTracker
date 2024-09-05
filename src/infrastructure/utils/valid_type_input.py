from ..constants.types_expenses import EXPENSE_TYPES


def valid_type_input(type_input: str) -> bool:
    if type_input in EXPENSE_TYPES:
        return True
    return False
