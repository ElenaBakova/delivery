import pytest
from microarch.delivery.core.domain.model.location.location import (
    MAX_LOCATION,
    MIN_LOCATION,
    Location,
)


def test_equal_coordinates_are_equal_location():
    assert Location(1, 1) == Location(1, 1)


def test_not_equal_coordinates_are_not_equal_location():
    assert Location(1, 2) != Location(5, 1)
    assert Location(1, 2) != Location(1, 9)


@pytest.mark.parametrize(
    "start, destination, expected",
    [((1, 1), (4, 5), 7), ((3, 3), (3, 3), 0), ((10, 10), (1, 1), 18)],
)
def test_distance_calculation(start, destination, expected):
    assert Location(*start).distance(Location(*destination)) == expected


def test_distance_to_itself_is_zero():
    location = Location(3, 4)

    assert location.distance(location) == 0


@pytest.mark.parametrize(
    "value, name",
    [(("str", 9), "X"), ((9, "str"), "Y"), ((None, "str"), "X"), ((9, None), "Y")],
)
def test_throws_type_error(value, name):
    with pytest.raises(TypeError, match=f"{name} must be an integer"):
        Location(*value)


@pytest.mark.parametrize(
    "value, name",
    [
        ((MIN_LOCATION - 1, 1), "X"),
        ((-1 * MIN_LOCATION, 1), "X"),
        ((MAX_LOCATION + 1, 1), "X"),
        ((-(MAX_LOCATION + 1), 1), "X"),
        ((1, MIN_LOCATION - 1), "Y"),
        ((1, -1 * MIN_LOCATION), "Y"),
        ((1, MAX_LOCATION + 1), "Y"),
        ((1, -(MAX_LOCATION + 1)), "Y"),
    ],
)
def test_throws_value_error(value, name):
    with pytest.raises(
        ValueError,
        match=f"{name} must be in range \\[{MIN_LOCATION}, {MAX_LOCATION}\\]",
    ):
        Location(*value)


@pytest.mark.parametrize(
    "start, destination, expected",
    [
        ((5, 5), (5, 5), False),
        ((5, 5), (4, 5), True),
        ((5, 5), (6, 5), True),
        ((5, 5), (5, 4), True),
        ((5, 5), (5, 6), True),
        ((5, 5), (4, 4), False),
        ((5, 5), (4, 6), False),
        ((5, 5), (6, 4), False),
        ((5, 5), (6, 6), False),
        ((5, 5), (3, 5), False),
        ((5, 5), (7, 5), False),
        ((5, 5), (5, 3), False),
        ((5, 5), (5, 7), False),
        ((5, 5), (1, 1), False),
    ],
)
def test_is_adjacent(start, destination, expected):
    assert Location(*start).is_adjacent(Location(*destination)) is expected
