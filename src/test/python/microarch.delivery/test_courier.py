from uuid import uuid4

import pytest
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


def test_move_one_step_allows_completing_assignment():
    courier = Courier("Courier", Location(2, 2))
    order = Order(uuid4(), Location(4, 2), Volume(1))
    courier.assign_order(order)

    with pytest.raises(ValueError, match="not in adjacent cell"):
        courier.complete_assignment(order)

    courier.move(Location(3, 2))
    courier.complete_assignment(order)


def test_move_to_current_location_is_allowed():
    location = Location(2, 2)
    courier = Courier("Courier", location)
    order = Order(uuid4(), location, Volume(1))
    courier.assign_order(order)

    courier.move(location)
    courier.complete_assignment(order)


@pytest.mark.parametrize("destination", [Location(3, 3), Location(4, 2)])
def test_move_more_than_one_step_leaves_location_unchanged(destination: Location):
    courier = Courier("Courier", Location(2, 2))
    order = Order(uuid4(), Location(1, 2), Volume(1))
    courier.assign_order(order)

    with pytest.raises(ValueError, match="can't move more than one step"):
        courier.move(destination)

    courier.complete_assignment(order)


def test_move_rejects_non_location():
    courier = Courier("Courier", Location(2, 2))

    with pytest.raises(TypeError, match="new_location must be a Location"):
        courier.move((3, 2))  # type: ignore[arg-type]


@pytest.mark.parametrize(
    "courier_location, can_complete",
    [
        pytest.param(Location(2, 2), True),
        pytest.param(Location(3, 2), True),
        pytest.param(Location(4, 2), False),
    ],
)
def test_complete_assignment_depends_on_courier_location(
    courier_location: Location, can_complete: bool
):
    order_location = Location(2, 2)
    courier = Courier("Courier", courier_location)
    order = Order(uuid4(), order_location, Volume(20))
    next_order = Order(uuid4(), order_location, Volume(1))
    courier.assign_order(order)

    if can_complete:
        courier.complete_assignment(order)
    else:
        with pytest.raises(ValueError, match="not in adjacent cell"):
            courier.complete_assignment(order)

    assert courier.can_take_new(next_order) is can_complete


def test_complete_assignment_rejects_unassigned_order():
    location = Location(2, 2)
    courier = Courier("Courier", location)
    courier.assign_order(Order(uuid4(), location, Volume(1)))
    unassigned_order = Order(uuid4(), location, Volume(1))

    with pytest.raises(ValueError, match="order is not assigned to that courier"):
        courier.complete_assignment(unassigned_order)


def test_complete_assignment_rejects_already_completed_order():
    location = Location(2, 2)
    courier = Courier("Courier", location)
    order = Order(uuid4(), location, Volume(1))
    courier.assign_order(order)
    courier.complete_assignment(order)

    with pytest.raises(ValueError, match="order is not assigned to that courier"):
        courier.complete_assignment(order)


def test_complete_assignment_rejects_non_order():
    courier = Courier("Courier", Location(2, 2))

    with pytest.raises(TypeError, match="order must be an Order"):
        courier.complete_assignment(None)  # type: ignore[arg-type]


def test_complete_assignment_frees_only_the_completed_orders_capacity():
    location = Location(2, 2)
    courier = Courier("Courier", location)
    courier.assign_order(Order(uuid4(), location, Volume(8)))
    order = Order(uuid4(), location, Volume(12))
    courier.assign_order(order)
    next_order = Order(uuid4(), location, Volume(12))

    assert not courier.can_take_new(next_order)

    courier.complete_assignment(order)

    assert courier.can_take_new(next_order)
    assert not courier.can_take_new(Order(uuid4(), location, Volume(13)))
