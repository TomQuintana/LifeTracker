def valid_type_input(type_input: str) -> bool:
    if type_input in ["food", "goOut", "others", "fixed", "clothes", "books", "fubol"]:
        return True
    return False
