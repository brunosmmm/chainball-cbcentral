"""Announcement registry."""

from cbcentral.registry import LocalRegistry
from cbcentral.registry.entry import LocalRegistryEntry
from cbcentral.util import id_from_url
from cbcentral.queries import query_announcements


class AnnouncementEntry(LocalRegistryEntry):
    """Announcement."""

    _index = "identifier"
    _fields = ["identifier", "players", "court"]

    def __init__(self, identifier, players, court, **kwargs):
        """Initialize."""
        super().__init__(**kwargs)
        self._identifier = identifier
        self._players = [id_from_url(player) for player in players]
        if court is None:
            self._court = None
        else:
            self._court = id_from_url(court)

    @property
    def players(self):
        """Get players."""
        return self._players

    @property
    def identifier(self):
        """Get identifier."""
        return self._identifier

    @property
    def court(self):
        """Get court."""
        return self._court


class LocalAnnounceRegistry(LocalRegistry):
    """Get announcements from server."""

    def __init__(self, db_path):
        """Initialize."""
        super().__init__("announce_registry", AnnouncementEntry, db_path)

    def update_registry(self, api_obj):
        """Update registry."""
        upstream_announcements = query_announcements(api_obj)
        self.build_registry(upstream_announcements)
        self.commit_registry()

    # def new_entry(self, content):
    #     """New entry."""
    #     if self.game_wrapper is not None:
    #         self.game_wrapper.announce_next_game(
    #             content.court, content.players
    #         )
