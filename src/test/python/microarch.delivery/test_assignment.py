import uuid
from uuid import UUID

import pytest
from microarch.delivery.core.domain.model.courier.assignment import (
    Assignment,
    AssignmentStatus,
)
from microarch.delivery.core.domain.model.courier.volume import Volume
from microarch.delivery.core.domain.model.location.location import Location


@pytest.mark.parametrize(
    "orderId, volume, location, status",
    [
        ("9", Volume(9), Location(1, 1), AssignmentStatus.ASSIGNED),
        (uuid.uuid4(), 9, Location(1, 1), AssignmentStatus.ASSIGNED),
        (uuid.uuid4(), Volume(9), (1, 2), AssignmentStatus.ASSIGNED),
        (uuid.uuid4(), Volume(9), Location(1, 1), "assigned"),
    ],
)
def test_invalid_init_arguments(
    orderId: UUID,
    volume: Volume,
    location: Location,
    status: AssignmentStatus,
):
    with pytest.raises(TypeError, match="argument is not assignable to the field"):
        Assignment(orderId, volume, location, status)


def test_invalid_status():
    with pytest.raises(
        ValueError, match="can't create assignment with status = completed"
    ):
        Assignment(
            orderId=uuid.uuid4(),
            volume=Volume(9),
            location=Location(1, 1),
            status=AssignmentStatus.COMPLETED,
        )


def test_complete_assignment():
    assignment = Assignment(
        orderId=uuid.uuid4(),
        volume=Volume(9),
        location=Location(2, 1),
        status=AssignmentStatus.ASSIGNED,
    )

    assert assignment.status == AssignmentStatus.ASSIGNED

    assignment.complete(Location(2, 2))

    assert assignment.status == AssignmentStatus.COMPLETED


def test_complete_completed_assignment():
    assignment = Assignment(
        orderId=uuid.uuid4(),
        volume=Volume(9),
        location=Location(2, 1),
        status=AssignmentStatus.ASSIGNED,
    )

    assert assignment.status == AssignmentStatus.ASSIGNED

    assignment.complete(Location(2, 2))

    assert assignment.status == AssignmentStatus.COMPLETED

    with pytest.raises(ValueError, match="can't complete not assigned assignment"):
        assignment.complete(Location(3, 1))


def test_complete_assignment_from_incorrect_cell():
    assignment = Assignment(
        orderId=uuid.uuid4(),
        volume=Volume(9),
        location=Location(6, 4),
        status=AssignmentStatus.ASSIGNED,
    )

    assert assignment.status == AssignmentStatus.ASSIGNED

    with pytest.raises(
        ValueError, match="can't complete order when courier is not in adjacent cell"
    ):
        assignment.complete(Location(10, 9))
