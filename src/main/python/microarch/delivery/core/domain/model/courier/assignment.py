import uuid
from enum import Enum
from uuid import UUID

from microarch.delivery.core.domain.model.location.location import Location
from microarch.delivery.core.domain.model.volume.volume import Volume


class AssignmentStatus(Enum):
    ASSIGNED = "assigned"
    COMPLETED = "completed"


class Assignment:
    def __init__(
        self,
        order_id: UUID,
        volume: Volume,
        location: Location,
        status: AssignmentStatus = AssignmentStatus.ASSIGNED,
    ):
        if (
            not isinstance(order_id, UUID)
            or not isinstance(volume, Volume)
            or not isinstance(location, Location)
            or not isinstance(status, AssignmentStatus)
        ):
            raise TypeError("argument is not assignable to the field")

        if status is AssignmentStatus.COMPLETED:
            raise ValueError("can't create assignment with status = completed")

        self.__id = uuid.uuid4()
        self.__order_id = order_id
        self.__volume = volume
        self.__location = location
        self.__status: AssignmentStatus = status

    @property
    def order_id(self):
        return self.__order_id

    @property
    def status(self):
        return self.__status

    @property
    def volume(self):
        return self.__volume

    def complete(self, courier_location: Location):
        if not (
            courier_location.is_adjacent(self.__location)
            or courier_location == self.__location
        ):
            raise ValueError(
                "can't complete order when courier is not in adjacent cell"
            )

        if self.__status != AssignmentStatus.ASSIGNED:
            raise ValueError("can't complete not assigned assignment")

        self.__status = AssignmentStatus.COMPLETED
