"""Game registry."""

from cbcentral.registry import LocalRegistry
from cbcentral.registry.entry import LocalRegistryEntry
from cbcentral.util import id_from_url
from cbcentral.queries import query_games


class GameEntry(LocalRegistryEntry):
    """Game registry entry."""

    _index = "identifier"
    _fields = [
        "identifier",
        "sequence",
        "description",
        "tournament",
        "events",
        "players",
        "duration",
        "start_time",
        "game_status",
        "court",
    ]

    def __init__(
        self,
        identifier,
        sequence,
        description,
        tournament,
        events,
        players,
        duration,
        start_time,
        game_status,
        court,
        **kwargs,
    ):
        """Initialize."""
        super().__init__(**kwargs)
        self._identifier = identifier
        self._sequence = sequence
        self._description = description
        self._tournament = self._get_tournament_id(tournament)
        self._events = events
        self._players = [id_from_url(player) for player in players]
        self._duration = duration
        self._start_time = start_time
        self._status = game_status
        if court is None:
            self._court = None
        else:
            self._court = id_from_url(court)

    @staticmethod
    def _get_tournament_id(tournament):
        """Get tournament id."""
        if isinstance(tournament, int):
            return tournament
        if isinstance(tournament, str):
            return int(id_from_url(tournament))

        raise TypeError("invalid type")

    @property
    def identifier(self):
        """Get identifier."""
        return self._identifier

    @property
    def sequence(self):
        """Get sequence number."""
        return self._sequence

    @property
    def description(self):
        """Get description."""
        return self._description

    @property
    def tournament(self):
        """Get tournament id."""
        return self._tournament

    @property
    def events(self):
        """Get events."""
        return self._events

    @property
    def players(self):
        """Get players."""
        return self._players

    @property
    def court(self):
        """Get court."""
        return self._court

    @property
    def duration(self):
        """Get duration."""
        return self._duration

    @property
    def start_time(self):
        """Get start time."""
        return self._start_time

    @property
    def game_status(self):
        """Get status."""
        return self._status


class LocalGameRegistry(LocalRegistry):
    """Game registry retrieved from server."""

    def __init__(self, db_path):
        """Initialize."""
        super().__init__("game_registry", GameEntry, db_path)
        self.game_wrapper = None

    def update_registry(self, api_obj):
        """Update registry."""
        upstream_games = query_games(api_obj)
        self.build_registry(upstream_games)

    def value_changed(self, entry_index, field_name, old_value, new_value):
        """Value changed callback."""
        if field_name == "game_status":
            if old_value == "NYET" and new_value == "NEXT":
                # announce
                if self.game_wrapper is not None:
                    game_entry = self[entry_index]
                    if game_entry.court is not None:
                        self.game_wrapper.announce_next_game(
                            game_entry.court, game_entry.players
                        )
