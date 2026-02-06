from dataclasses import dataclass, field
from typing import Dict, List, Optional


PLACE_TYPES = {
    "hospital",
    "house",
    "street",
    "market",
    "park",
}


@dataclass(frozen=True)
class Place:
    place_id: str
    name: str
    place_type: str
    description: str
    connections: List[str] = field(default_factory=list)


PLACES: Dict[str, Place] = {
    "house_01": Place(
        place_id="house_01",
        name="Small House",
        place_type="house",
        description="A cozy house with a small garden out front.",
        connections=["street_01"],
    ),
    "street_01": Place(
        place_id="street_01",
        name="Main Street",
        place_type="street",
        description="A busy street connecting several key locations.",
        connections=["house_01", "market_01", "park_01", "hospital_01"],
    ),
    "market_01": Place(
        place_id="market_01",
        name="Local Market",
        place_type="market",
        description="A bustling market with food and supplies.",
        connections=["street_01"],
    ),
    "park_01": Place(
        place_id="park_01",
        name="Community Park",
        place_type="park",
        description="A quiet park with benches and walking paths.",
        connections=["street_01"],
    ),
    "hospital_01": Place(
        place_id="hospital_01",
        name="City Hospital",
        place_type="hospital",
        description="A hospital providing medical services.",
        connections=["street_01"],
    ),
}


def get_place(place_id: str) -> Optional[Place]:
    """
    Resolve a place by ID.
    """
    return PLACES.get(place_id)
