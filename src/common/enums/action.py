import enum


@enum.unique
class ActionType(enum.StrEnum):
    new_order = enum.auto()
