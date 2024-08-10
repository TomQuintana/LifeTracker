def format_data_list(data) -> list:
    data_formated = []
    for element in data:
        data_formated.append(element)

    return data_formated


def format_data_dict(book_data) -> dict:
    book_formated = {}
    for element in book_data:
        print(element.notes)
        book_formated = {
            "uuid": element.uuid,
            "title": element.title,
            "author": element.author,
            "type": element.type,
            "notes": getattr(element, "notes", "No notes available"),
            "status": element.status,
            "physically": element.physically,
        }
        print(book_formated)

    return book_formated
