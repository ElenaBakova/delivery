from enum import Enum


class OrderStatus(Enum):
    CREATED = "created"
    ASSIGNED = "assigned"
    COMPLETED = "completed"
