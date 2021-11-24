from typing import *
from wefram.l10n import lazy_gettext
from wefram import aaa, ds, settings


aaa.permissions.register('access', lazy_gettext("Able to see contacts", 'contacts'))
aaa.permissions.register('personal', lazy_gettext("Able to create own contact directories", 'contacts'))
aaa.permissions.register('workspace', lazy_gettext("Administrate general workspace contact directories", 'contacts'))
aaa.permissions.register('admin', lazy_gettext("Administrate contacts settings", 'contacts'))

# ds.storages.register('default', requires=['some_permission'])
ds.storages.register('avatars')


settings.register(
    name='general',
    requires='admin',
    properties=[
        ('personal', settings.BooleanProp(lazy_gettext("Allow personal contact books", 'contacts'))),
    ],
    defaults={
        'personal': False,
    },
    order=10
)

settings.register(
    name='team',
    requires='admin',
    properties=[
        ('sort_by_last_name', settings.BooleanProp(lazy_gettext("Sort users' contacts by last name", 'contacts'))),
        ('list_middle_name', settings.BooleanProp(lazy_gettext("Display users' middle names in lists", 'contacts')))
    ],
    defaults={
        'sort_by_last_name': True,
        'list_middle_name': True
    },
    order=20
)

settings.register(
    name='chat',
    requires='admin',
    properties=[
        ('chat', settings.BooleanProp(lazy_gettext("Enable chats", 'contacts')))
    ],
    defaults={
        'chat': True
    },
    order=30
)

