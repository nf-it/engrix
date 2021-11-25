from typing import *
import datetime
import re
from wefram import ds, settings, aaa
from wefram.urls import media_res_url
from wefram.l10n import lazy_gettext
from wefram.tools import py_to_json
from wefram.models import User, SettingsCatalog


__all__ = [
    'Directory',
    'Contact',
    'Pin'
]


class Directory(ds.Model):
    id = ds.UUIDPrimaryKey()
    user_id = ds.Column(ds.UUID(), ds.ForeignKey('systemUser.id', ondelete='CASCADE'), nullable=True)
    name = ds.Column(ds.Caption(), nullable=False)


class Contact(ds.Model):
    id = ds.UUIDPrimaryKey()

    user_id = ds.Column(
        ds.UUID(),
        ds.ForeignKey(ds.ModelColumn('system.User', 'id'), ondelete='CASCADE'),
        nullable=True,
        default=None
    )
    directory_id = ds.Column(
        ds.UUID(),
        ds.ForeignKey(ds.ModelColumn('Directory', 'id'), onupdate='CASCADE'),
        nullable=True,
        default=None
    )

    avatar = ds.Column(ds.Image('contacts.avatars'))
    name = ds.Column(ds.Caption(), nullable=True, default=None)
    nickname = ds.Column(ds.String(100), nullable=False, default='')
    birthdate = ds.Column(ds.Date(), nullable=True, default=None)
    emails = ds.Column(ds.JSONB())
    phones = ds.Column(ds.JSONB())
    im = ds.Column(ds.JSONB())
    company = ds.Column(ds.String(100), nullable=False, default='')
    position = ds.Column(ds.String(200), nullable=False, default='')
    home_address = ds.Column(ds.String(500), nullable=False, default='')
    work_address = ds.Column(ds.String(500), nullable=False, default='')
    notes = ds.Column(ds.Text(), default='')

    @classmethod
    def generate_dict(
            cls,
            contact_id: Optional[str],
            user_id: Optional[str],
            name: str,
            avatar: Optional[Union[str, ds.orm.storage.StoredImage]] = None,
            nickname: Optional[str] = None,
            birthdate: Optional[datetime.date] = None,
            emails: Optional[list] = None,
            phones: Optional[list] = None,
            im: Optional[list] = None,
            company: Optional[str] = None,
            position: Optional[str] = None,
            home_address: Optional[str] = None,
            work_address: Optional[str] = None,
            notes: Optional[str] = None,
            pinned: bool = False,
            for_json: bool = False
    ) -> dict:
        result: dict = {
            'contact_id': contact_id or None,
            'user_id': user_id or None,
            'name': name,
            'avatar': avatar,
            'nickname': nickname or '',
            'birthdate': birthdate or None,
            'emails': emails or [],
            'phones': phones or [],
            'im': im or [],
            'company': company or '',
            'position': position or '',
            'home_address': home_address or '',
            'work_address': work_address or '',
            'notes': str(notes).strip() if notes else '',
            'pinned': pinned
        }
        return result if not for_json else py_to_json(result)

    # -
    # - Some useful providers for contacts, inc. special cases
    # -

    @classmethod
    async def ensure_for_user(cls, user_id: str) -> 'Contact':
        existing: Optional[Contact] = await cls.first(user_id=user_id)
        if existing is not None:
            return existing
        contact: Contact = await cls.create(
            user_id=user_id
        )
        await ds.db.flush()
        return contact

    @classmethod
    async def team(
            cls,
            *keys: Union[str, int],
            count: bool = False,
            offset: Optional[int] = None,
            limit: Optional[int] = None,
            search_term: Optional[str] = None,
            for_json: bool = False
    ) -> List[dict]:
        """ Returns a list of team (general) contacts, which includes
        contacts of all accessible users and general contacts, added
        for the general team usage. Because we cannot act with the
        Contact models themself, we return generated dicts instead.

        :return: the list of contacts
        :rtype: list of dicts
        """

        def _name(_contact: Optional[Contact], _user: Optional[User]) -> str:
            if _user is None and _contact is not None:
                return _contact.name
            elif _user is not None:
                if list_middle_name:
                    _names: list = [
                        _user.last_name, _user.first_name, _user.middle_name
                    ] if sort_by_last_name else [
                        _user.first_name, _user.middle_name, _user.last_name
                    ]
                else:
                    _names: list = [
                        _user.last_name, _user.first_name
                    ] if sort_by_last_name else [
                        _user.first_name, _user.last_name
                    ]
                return ' '.join([_s for _s in _names if _s])
            else:
                return ""

        def _avatar(_contact: Optional[Contact], _user: Optional[User]) -> Optional[Union[str, ds.orm.storage.StoredImage]]:
            _value = None
            if _user is not None and _user.avatar is not None:
                _value = _user.avatar
            elif _contact is not None and _contact.avatar is not None:
                _value = _contact.avatar
            if _value is None:
                return None
            return _value.url if for_json else _value

        logged_user_id: Optional[str] = aaa.get_current_user_id()

        if not logged_user_id:  # Return nothing for the not logged in user
            return []

        team_settings: SettingsCatalog = await settings.get('team')
        sort_by_last_name: bool = team_settings['sort_by_last_name']
        list_middle_name: bool = team_settings['list_middle_name']

        # Depending on the administrator choice - choosing sorting
        # strategy by users' last name or by users' first name.
        order_attrs = [
            Contact.name, User.last_name, User.first_name, User.middle_name
        ] if sort_by_last_name else [
            Contact.name, User.first_name, User.middle_name, User.last_name
        ]
        order = ds.func.trim(ds.func.concat_ws(' ', *order_attrs))

        # Filtering results. Necessarily fetching only objects with
        # Contact.directory_id is NULL meaning general team contacts.
        where = [
            Contact.directory_id.is_(None)
        ]

        # Ability to find contacts using their names or contact
        # data (phones, emails).
        if search_term:
            name_term = search_term.strip().lower()
            phone_term = re.sub(r'[^\d+]', '', search_term)
            email_term = re.sub(r'[^\w.@]', '', search_term)

            search_where = [
                ds.func.trim(ds.func.concat_ws(
                    ' ', Contact.name, User.first_name, User.last_name
                )).ilike(f"%{name_term}%"),

                ds.func.trim(ds.func.concat_ws(
                    ' ', Contact.name, User.last_name, User.first_name
                )).ilike(f"%{name_term}%"),
            ]
            if phone_term:
                search_where.append(
                    Contact.phones.cast(ds.String).ilike(f"%{phone_term}%")
                )
            if email_term:
                search_where.append(
                    Contact.emails.cast(ds.String).ilike(f"%{email_term}%")
                )
            where.append(ds.or_(*search_where))

        query = ds.select(Contact, User, Pin) \
            .join(User, User.id == Contact.user_id, full=True) \
            .join(Pin, ds.and_(Pin.user_id == logged_user_id, Pin.contact_id == Contact.id), isouter=True) \
            .where(ds.and_(*where) if len(where) > 1 else where[0]) \
            .order_by(Pin.contact_id.is_(None), order)

        items = await ds.execute(query)
        results: List[dict] = []

        # Parsing the results and generating the list of corresponding
        # dicts.
        contact: Optional[Contact]
        user: Optional[User]
        pin: Optional[Pin]
        for item in items:
            contact, user, pin = item
            results.append(cls.generate_dict(
                contact_id=contact.id if contact is not None else None,
                user_id=user.id if user is not None else None,
                name=_name(contact, user),
                avatar=_avatar(contact, user),
                nickname=contact.nickname if contact is not None else '',
                birthdate=contact.birthdate if contact is not None else None,
                emails=(contact.emails or []) if contact is not None else [],
                phones=(contact.phones or []) if contact is not None else [],
                im=(contact.im or []) if contact is not None else [],
                company=contact.company if contact is not None else '',
                position=contact.position if contact is not None else '',
                home_address=contact.home_address if contact is not None else '',
                work_address=contact.work_address if contact is not None else '',
                notes=contact.notes if contact is not None else '',
                pinned=pin is not None,
                for_json=for_json
            ))

        return results


class Pin(ds.Model):
    user_id = ds.Column(
        ds.UUID(),
        ds.ForeignKey(ds.ModelColumn('system.User', 'id'), ondelete='CASCADE'),
        nullable=False,
        primary_key=True
    )
    contact_id = ds.Column(
        ds.UUID(),
        ds.ForeignKey(Contact.id, ondelete='CASCADE'),
        nullable=False,
        primary_key=True
    )

    @classmethod
    async def pin(cls, contact_id: str) -> None:
        logged_user_id: Optional[str] = aaa.get_current_user_id()
        if logged_user_id is None:
            return
        pin: Optional[Pin] = await cls.first(
            user_id=logged_user_id,
            contact_id=contact_id
        )
        if pin is not None:
            return
        await Pin.create(
            user_id=logged_user_id,
            contact_id=contact_id
        )
        await ds.db.flush()

    @classmethod
    async def unpin(cls, contact_id: str) -> None:
        logged_user_id: Optional[str] = aaa.get_current_user_id()
        if logged_user_id is None:
            return
        pin: Optional[Pin] = await cls.first(
            user_id=logged_user_id,
            contact_id=contact_id
        )
        if pin is None:
            return
        await pin.delete()
        await ds.db.flush()

