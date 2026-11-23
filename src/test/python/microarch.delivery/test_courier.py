from uuid import uuid4

import pytest
from microarch.delivery.core.domain.model.courier.assignment import (
    Assignment,
    AssignmentStatus,
)
from microarch.delivery.core.domain.model.courier.courier import Courier
from microarch.delivery.core.domain.model.location.location import Location
from microarch.delivery.core.domain.model.order.order import Order
from microarch.delivery.core.domain.model.volume.volume import Volume


def test_courier_rejects_empty_name():
    with pytest.raises(ValueError, match="name can't be empty"):
        Courier("", Location(1, 1))


def test_courier_rejects_invalid_starting_location():
    with pytest.raises(TypeError, match="argument is not assignable to the field"):
        Courier("Courier", (1, 1))  # type: ignore[arg-type]


@pytest.mark.parametrize("volume, expected", [(19, True), (20, True), (21, False)])
def test_can_take_new_respects_capacity(volume: int, expected: bool):
    location = Location(1, 1)
    courier = Courier("Courier", location)
    order = Order(uuid4(), location, Volume(volume))

    assert courier.can_take_new(order) == expected


def test_assign_order_counts_existing_assignments_toward_capacity():
    location = Location(1, 1)
    courier = Courier("Courier", location)

    courier.assign_order(Order(uuid4(), location, Volume(12)))
    courier.assign_order(Order(uuid4(), location, Volume(8)))

    with pytest.raises(ValueError, match="can't take more orders"):
        courier.assign_order(Order(uuid4(), location, Volume(1)))


def test_move_one_step_allows_finishing_assignment():
    courier = Courier("Courier", Location(2, 2))
    assignment = Assignment(uuid4(), Volume(1), Location(4, 2))

    with pytest.raises(ValueError, match="not in adjacent cell"):
        courier.finish_assignment(assignment)
    assert assignment.status is AssignmentStatus.ASSIGNED

    courier.move(Location(3, 2))
    courier.finish_assignment(assignment)

    assert assignment.status is AssignmentStatus.COMPLETED


def test_move_to_current_location_is_allowed():
    location = Location(2, 2)
    courier = Courier("Courier", location)
    assignment = Assignment(uuid4(), Volume(1), location)

    courier.move(location)
    courier.finish_assignment(assignment)

    assert assignment.status is AssignmentStatus.COMPLETED


@pytest.mark.parametrize("destination", [Location(3, 3), Location(4, 2)])
def test_move_more_than_one_step_leaves_location_unchanged(destination: Location):
    courier = Courier("Courier", Location(2, 2))
    assignment = Assignment(uuid4(), Volume(1), Location(1, 2))

    with pytest.raises(ValueError, match="can't move more than one step"):
        courier.move(destination)

    courier.finish_assignment(assignment)
    assert assignment.status is AssignmentStatus.COMPLETED


def test_move_rejects_non_location():
    courier = Courier("Courier", Location(2, 2))

    with pytest.raises(TypeError, match="new_location must be a Location"):
        courier.move((3, 2))  # type: ignore[arg-type]


def test_finish_assignment_rejects_already_completed_assignment():
    location = Location(2, 2)
    courier = Courier("Courier", location)
    assignment = Assignment(uuid4(), Volume(1), location)
    courier.finish_assignment(assignment)

    with pytest.raises(ValueError, match="can't complete not assigned assignment"):
        courier.finish_assignment(assignment)


def test_finish_assignment_rejects_non_assignment():
    courier = Courier("Courier", Location(2, 2))

    with pytest.raises(TypeError, match="assignment must be an Assignment"):
        courier.finish_assignment(None)  # type: ignore[arg-type]
