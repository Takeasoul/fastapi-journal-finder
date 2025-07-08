from typing import Type, Optional
import enum

from sqlalchemy import TypeDecorator, String


def enum_key_to_value(enum_class: Type[enum.Enum], key: str) -> Optional[str]:
    try:
        return enum_class[key].value
    except KeyError:
        return None

def enum_value_to_key(enum_class: Type[enum.Enum], value: str) -> Optional[str]:
    for member in enum_class:
        if member.value == value:
            return member.name
    return None

def enum_value_to_member(enum_class: Type[enum.Enum], value: str) -> Optional[enum.Enum]:
    for member in enum_class:
        if member.value == value:
            return member
    return None

def enum_key_to_member(enum_class: Type[enum.Enum], key: str) -> Optional[enum.Enum]:
    try:
        return enum_class[key]
    except KeyError:
        return None

class EnumValueType(TypeDecorator):
    impl = String
    def __init__(self, enum_class, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.enum_class = enum_class
    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if isinstance(value, self.enum_class):
            return value.value
        if isinstance(value, str):
            return enum_key_to_value(self.enum_class, value)
        raise ValueError(f"Unexpected enum value: {value}")
    def process_result_value(self, value, dialect):
        if value is None:
            return None
        return enum_value_to_member(self.enum_class, value)