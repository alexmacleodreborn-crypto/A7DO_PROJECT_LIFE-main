"""Scenario definition for the A7DO Born Person World."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass(frozen=True)
class Scenario:
    name: str
    places: Dict[str, Place]

    def describe_world(self) -> str:
        lines = [f"Scenario: {self.name}", "", "Places and connections:"]
        for place_id in sorted(self.places):
            place = self.places[place_id]
            connections = ", ".join(sorted(place.connections))
            lines.append(
                f"- {place.name} ({place.place_type}, {place_id}): "
                f"{place.description} Connections: {connections}."
            )
        return "\n".join(lines)


@dataclass(frozen=True)
class Place:
    place_id: str
    name: str
    place_type: str
    description: str
    connections: List[str] = field(default_factory=list)



def _connect(place: Place, connections: Iterable[str]) -> Place:
    return Place(
        place_id=place.place_id,
        name=place.name,
        place_type=place.place_type,
        description=place.description,
        connections=list(connections),
    )


HOUSE = Place(
    place_id="house_01",
    name="Family House",
    place_type="house",
    description="A modest home where the A7DO person begins life.",
)
HOSPITAL = Place(
    place_id="hospital_01",
    name="Birth Hospital",
    place_type="hospital",
    description="A small hospital where births and checkups take place.",
)
SCHOOL = Place(
    place_id="school_01",
    name="Neighborhood School",
    place_type="school",
    description="A local school that anchors early learning and social growth.",
)
LANGUAGE_CENTER = Place(
    place_id="language_01",
    name="Language Learning Center",
    place_type="learning_center",
    description=(
        "A center for spoken and written language practice through shared, "
        "embodied activities."
    ),
)
MARKET = Place(
    place_id="market_01",
    name="Community Market",
    place_type="market",
    description="A market for food, supplies, and daily exchanges.",
)
STREET_MAIN = Place(
    place_id="street_01",
    name="Main Street",
    place_type="street",
    description="The main street connecting homes, services, and parks.",
)
STREET_WEST = Place(
    place_id="street_02",
    name="West Street",
    place_type="street",
    description="A quieter street leading toward the park and school.",
)
PARK = Place(
    place_id="park_01",
    name="Green Park",
    place_type="park",
    description="A park with open space for play and recovery.",
)
SPATIAL_PLAZA = Place(
    place_id="plaza_01",
    name="Spatial Plaza",
    place_type="plaza",
    description=(
        "An open 3D space with landmarks, elevation changes, and paths for "
        "navigation practice."
    ),
)


PLACES: Dict[str, Place] = {
    "house_01": _connect(HOUSE, ["street_01"]),
    "hospital_01": _connect(HOSPITAL, ["street_01"]),
    "language_01": _connect(LANGUAGE_CENTER, ["street_02"]),
    "school_01": _connect(SCHOOL, ["street_02"]),
    "market_01": _connect(MARKET, ["street_01"]),
    "street_01": _connect(
        STREET_MAIN, ["house_01", "hospital_01", "market_01", "street_02"]
    ),
    "street_02": _connect(
        STREET_WEST, ["street_01", "park_01", "school_01", "language_01", "plaza_01"]
    ),
    "park_01": _connect(PARK, ["street_02"]),
    "plaza_01": _connect(SPATIAL_PLAZA, ["street_02"]),
}


A7DO_BORN_PERSON_WORLD = Scenario(
    name="A7DO Born Person World",
    places=PLACES,
)
