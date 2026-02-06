from dataclasses import dataclass
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional


_ENV_ROOT = Path(__file__).resolve().parent


def _load_module(name: str, filename: str):
    path = _ENV_ROOT / filename
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


home_mod = _load_module("world_home", "home.py")
society_mod = _load_module("world_society", "society.py")
nature_mod = _load_module("world_nature", "nature.py")
weather_mod = _load_module("world_weather", "weather_system.py")
places_mod = _load_module("world_places", "places.py")

HomeEnvironment = home_mod.HomeEnvironment
SocietyEnvironment = society_mod.SocietyEnvironment
NatureEnvironment = nature_mod.NatureEnvironment
WeatherSystem = weather_mod.WeatherSystem
Place = places_mod.Place
PLACES = places_mod.PLACES
get_place = places_mod.get_place


@dataclass
class World:
    home: HomeEnvironment
    society: SocietyEnvironment
    nature: NatureEnvironment
    weather: WeatherSystem
    places: Dict[str, Place]
    world_state: Optional[object] = None

    @classmethod
    def create(
        cls,
        world_state: Optional[object] = None,
        default_place: Optional[str] = "house",
    ) -> "World":
        world = cls(
            home=HomeEnvironment(),
            society=SocietyEnvironment(),
            nature=NatureEnvironment(),
            weather=WeatherSystem(),
            places=dict(PLACES),
            world_state=world_state,
        )
        if default_place is not None:
            world.move_to(default_place)
        return world

    def list_places(self) -> List[Place]:
        return list(self.places.values())

    def move_to(self, place_id: str) -> Place:
        place = get_place(place_id)
        if place is None:
            raise ValueError(f"Unknown place_id: {place_id}")
        if self.world_state is not None and hasattr(self.world_state, "update_location"):
            self.world_state.update_location(place_id)
        return place
