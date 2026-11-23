from uuid import UUID

from microarch.delivery.core.domain.model.location.location import Location
from microarch.delivery.core.domain.model.order.order_status import OrderStatus
from microarch.delivery.core.domain.model.volume.volume import Volume


class Order:
    def __init__(self, order_id: UUID, location: Location, volume: Volume) -> None:
        if (
            not isinstance(order_id, UUID)
            or not isinstance(volume, Volume)
            or not isinstance(location, Location)
        ):
            raise TypeError("argument is not assignable to the field")

        self.__id = order_id
        self.__volume = volume
        self.__location = location
        self.__status: OrderStatus = OrderStatus.CREATED

    def change_order_status(self, new_status):
        if new_status == OrderStatus.ASSIGNED and self.__status != OrderStatus.CREATED:
            raise ValueError(
                "can't set status assigned for order with status != created"
            )

        if (
            new_status == OrderStatus.COMPLETED
            and self.__status != OrderStatus.ASSIGNED
        ):
            raise ValueError(
                "can't set status completed for order with status != assigned"
            )

        self.__status = new_status
