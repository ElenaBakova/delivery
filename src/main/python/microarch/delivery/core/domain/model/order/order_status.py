from enum import Enum


class OrderStatus(Enum):
    CREATED = "created"
    ASSIGNED = "assigned"
    COMPLETED = "completed"

    def transition_to(self, new_status: "OrderStatus") -> "OrderStatus":
        if not isinstance(new_status, OrderStatus):
            raise TypeError("new_status must be an OrderStatus")

        if (self, new_status) not in (
            (OrderStatus.CREATED, OrderStatus.ASSIGNED),
            (OrderStatus.ASSIGNED, OrderStatus.COMPLETED),
        ):
            raise ValueError(
                f"can't change order status from {self.value} to {new_status.value}"
            )

        return new_status
