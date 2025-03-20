import enum


@enum.unique
class OrderStatus(enum.StrEnum):
    pending = enum.auto()
    paid = enum.auto()
    shipped = enum.auto()
    canceled = enum.auto()
