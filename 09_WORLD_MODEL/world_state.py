class WorldState:
    """
    Descriptive world model.
    Holds the current state of the organism and environment.
    NO learning, NO planning, NO decisions.
    """

    def __init__(self, default_place=None):
        self._state = {
            "energy": None,
            "strain": None,
            "last_action": None,
            "last_sensation": None,
            "time": None,
            "current_place": None,
            "known_places": [],
        }
        if default_place is not None:
            self.update_location(default_place)

    def update(self, **kwargs):
        """
        Update known world variables.
        Only overwrites provided keys.
        """
        for key, value in kwargs.items():
            if key in self._state:
                self._state[key] = value

    def snapshot(self):
        """
        Return a read-only snapshot of the current world state.
        """
        return dict(self._state)

    def update_location(self, place_id):
        """
        Update the current place and track known places.
        """
        self._state["current_place"] = place_id
        if place_id not in self._state["known_places"]:
            self._state["known_places"].append(place_id)
