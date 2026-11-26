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

    @property
    def id(self):
        return self.__id

    @property
    def volume(self):
        return self.__volume

    @property
    def location(self):
        return self.__location

    @property
    def status(self) -> OrderStatus:
        return self.__status

    def change_order_status(self, new_status: OrderStatus) -> None:
        self.__status = self.__status.transition_to(new_status)
