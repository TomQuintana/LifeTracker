from ..constants.types_expenses import EXPENSE_TYPES


def valid_type_input(type_input: str) -> bool:
    if type_input in EXPENSE_TYPES:
        return True
    return False


def valid_is_month_pass(self, month):
    if not month:
        return False
    return True
