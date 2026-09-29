from enum import Enum

from mongoengine import (
    BooleanField,
    Document,
    EmailField,
    EnumField,
    ListField,
    ReferenceField,
    StringField,
)

from db import *  # noqa: F401,F403


class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

    meta = {"collection": "authors"}


class Quote(Document):
    tags = ListField(StringField(), default=list)
    author = ReferenceField(Author, required=True)
    quote = StringField(required=True)

    meta = {"collection": "quotes"}


class PreferredChannel(Enum):
    EMAIL = "email"
    SMS = "sms"


class Contact(Document):
    fullname = StringField(required=True)
    email = EmailField(required=True)
    phone = StringField()
    preferred_channel = EnumField(
        PreferredChannel,
        default=PreferredChannel.EMAIL,
    )
    sent = BooleanField(default=False)

    meta = {"collection": "contacts"}
