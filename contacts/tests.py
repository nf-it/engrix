from .models import Contact


async def team(*_) -> None:
    contacts = await Contact.team(for_json=True, search_term='@gmail.com')
    # Torres Micheal Stacey

    [
        print(c['name'], "\n  ", c['avatar'])
        for c in contacts
    ]
