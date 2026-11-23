import uuid

from microarch.delivery.core.domain.model.courier.assignment import Assignment
from microarch.delivery.core.domain.model.location.location import Location
from microarch.delivery.core.domain.model.order.order import Order
from microarch.delivery.core.domain.model.volume.volume import Volume


class Courier:
    def __init__(self, name: str, location: Location) -> None:
        if not isinstance(location, Location):
            raise TypeError("argument is not assignable to the field")

        if name == "":
            raise ValueError("name can't be empty")

        self.__id = uuid.uuid4()
        self.__name = name
        self.__location = location
        self.__max_volume = Volume(20)
        self.__assignments: list[Assignment] = []

    def can_take_new(self, order: Order):
        total_volume = sum(
            (assignment.volume for assignment in self.__assignments), order.volume
        )

        return total_volume <= self.__max_volume

    def assign_order(self, order: Order):
        if not self.can_take_new(order):
            raise ValueError("can't take more orders")

        new_assignment = Assignment(order.id, order.volume, order.location)
        self.__assignments.append(new_assignment)

    def finish_assignment(self, assignment: Assignment) -> None:
        if not isinstance(assignment, Assignment):
            raise TypeError("assignment must be an Assignment")

        assignment.complete(self.__location)

    def move(self, new_location: Location) -> None:
        if not isinstance(new_location, Location):
            raise TypeError("new_location must be a Location")

        if self.__location != new_location and (
            not self.__location.is_adjacent(new_location)
        ):
            raise ValueError("courier can't move more than one step")

        self.__location = new_location
