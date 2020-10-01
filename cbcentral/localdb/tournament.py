"""Tournament registry."""

from cbcentral.registry.entry import LocalRegistryEntry
from cbcentral.registry import LocalRegistry
from cbcentral.util import id_from_url
from cbcentral.localdb import LOCALDB_LOGGER
from cbcentral.queries import query_tournaments


class TournamentEntry(LocalRegistryEntry):
    """Tournament registry entry."""

    _index = "id"
    _fields = [
        "id",
        "season",
        "description",
        "event_date",
        "players",
        "status",
        "games",
    ]

    def __init__(
        self,
        id,
        season,
        description,
        event_date,
        players,
        status,
        games,
        **kwargs,
    ):
        """Initialize."""
        super().__init__(**kwargs)
        self._id = id
        self._season = id_from_url(season)
        self._description = description
        self._date = event_date
        # abbreviate player data
        self._players = [id_from_url(player) for player in players]
        self._status = status
        # also abbreviate
        self._games = self._get_game_ids(games)

    @staticmethod
    def _get_game_ids(games):
        """Get game ids."""
        ret = []
        for game in games:
            if isinstance(game, int):
                ret.append(game)
            elif isinstance(game, str):
                ret.append(int(id_from_url(game)))
            else:
                raise TypeError("invalid type")

        return ret

    @property
    def id(self):
        """Get id."""
        return self._id

    @property
    def season(self):
        """Get season."""
        return self._season

    @property
    def description(self):
        """Get description."""
        return self._description

    @property
    def event_date(self):
        """Get date."""
        return self._date

    @property
    def players(self):
        """Get Players."""
        return self._players

    @property
    def status(self):
        """Get status."""
        return self._status

    @property
    def games(self):
        """Get games."""
        return self._games


class LocalTournamentRegistry(LocalRegistry):
    """Tournament registry retrieved from central server."""

    def __init__(self, db_path):
        """Initialize."""
        super().__init__("tournament_registry", TournamentEntry, db_path)
        LOCALDB_LOGGER.info("local tournament registry loaded")

    def update_registry(self, api_obj):
        """Update registry."""
        LOCALDB_LOGGER.info("updating game registry from central server")
        upstream_tournaments = query_tournaments(api_obj)
        self.build_registry(upstream_tournaments)
