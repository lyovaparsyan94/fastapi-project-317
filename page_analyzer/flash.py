from fastapi import Request

FLASH_KEY = "flash"


def flash(request: Request, message: str, category: str = "success") -> None:
    messages = request.session.get(FLASH_KEY, [])
    messages.append({"message": message, "category": category})
    # Starlette считает сессию изменённой только при присваивании ключа,
    # мутации вложенного списка в cookie не попадают.
    request.session[FLASH_KEY] = messages


def get_flashed_messages(request: Request) -> list[dict[str, str]]:
    return request.session.pop(FLASH_KEY, [])
