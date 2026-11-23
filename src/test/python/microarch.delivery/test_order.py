from uuid import UUID, uuid4

import pytest
from microarch.delivery.core.domain.model.location.location import Location
from microarch.delivery.core.domain.model.order.order import Order
from microarch.delivery.core.domain.model.order.order_status import OrderStatus
from microarch.delivery.core.domain.model.volume.volume import Volume


def test_order_init():
    order_id = uuid4()
    location = Location(2, 3)
    volume = Volume(4)

    order = Order(order_id, location, volume)

    assert order.id == order_id
    assert order.location == location
    assert order.volume == volume


@pytest.mark.parametrize(
    "order_id, location, volume",
    [
        ("UUID", Location(1, 1), Volume(2)),
        (uuid4(), (1, 1), Volume(2)),
        (uuid4(), Location(1, 1), 2),
    ],
)
def test_order_rejects_invalid_creation_arguments(
    order_id: UUID, location: Location, volume: Volume
):
    with pytest.raises(TypeError, match="argument is not assignable to the field"):
        Order(order_id, location, volume)


def test_order_moves_from_created_to_assigned_to_completed():
    order = Order(uuid4(), Location(1, 1), Volume(2))
    assert order.status is OrderStatus.CREATED

    order.change_order_status(OrderStatus.ASSIGNED)
    assert order.status is OrderStatus.ASSIGNED

    order.change_order_status(OrderStatus.COMPLETED)
    assert order.status is OrderStatus.COMPLETED


@pytest.mark.parametrize(
    "current, target",
    [
        (OrderStatus.CREATED, OrderStatus.CREATED),
        (OrderStatus.CREATED, OrderStatus.COMPLETED),
        (OrderStatus.ASSIGNED, OrderStatus.CREATED),
        (OrderStatus.ASSIGNED, OrderStatus.ASSIGNED),
        (OrderStatus.COMPLETED, OrderStatus.CREATED),
        (OrderStatus.COMPLETED, OrderStatus.ASSIGNED),
        (OrderStatus.COMPLETED, OrderStatus.COMPLETED),
    ],
)
def test_invalid_transition_leaves_order_status_unchanged(
    current: OrderStatus, target: OrderStatus
):
    order = Order(uuid4(), Location(1, 1), Volume(2))
    if current is not OrderStatus.CREATED:
        order.change_order_status(OrderStatus.ASSIGNED)
    if current is OrderStatus.COMPLETED:
        order.change_order_status(OrderStatus.COMPLETED)

    with pytest.raises(ValueError, match="can't change order status"):
        order.change_order_status(target)

    assert order.status is current


def test_order_rejects_non_enum_status():
    order = Order(uuid4(), Location(1, 1), Volume(2))

    with pytest.raises(TypeError, match="new_status must be an OrderStatus"):
        order.change_order_status("assigned")  # type: ignore[arg-type]

    assert order.status is OrderStatus.CREATED
