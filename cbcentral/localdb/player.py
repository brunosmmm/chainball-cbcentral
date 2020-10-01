"""Player registry."""
import os
import base64

from cbcentral.registry.entry import LocalRegistryEntry
from cbcentral.registry import LocalRegistry
from cbcentral.localdb import LOCALDB_LOGGER
from cbcentral.queries import query_players, get_sfx_data
from cbcentral.api import CBCentralAPIError
from cbcentral.util import md5_sum


class PlayerEntry(LocalRegistryEntry):
    """Locally cached player description."""

    _index = "username"
    _fields = ["name", "display_name", "username", "sfx_md5"]

    def __init__(self, name, display_name, username, sfx_md5, **kwargs):
        """Initialize."""
        super().__init__(**kwargs)
        self._name = name
        self._dispname = display_name
        self._username = username
        self._sfx_md5 = sfx_md5

    @property
    def name(self):
        """Get name."""
        return self._name

    @property
    def display_name(self):
        """Get display name."""
        return self._dispname

    @property
    def username(self):
        """Get username."""
        return self._username

    @property
    def sfx_md5(self):
        """Get sfx md5 sum."""
        return self._sfx_md5


class LocalPlayerRegistry(LocalRegistry):
    """Local player registry."""

    def __init__(self, db_path, sfx_path=None):
        super().__init__("player_registry", PlayerEntry, db_path)
        self._sfx_path = sfx_path

        # build registry
        LOCALDB_LOGGER.info("local player registry loaded")

    def update_registry(self, api_obj):
        """Update registry with information from central server."""
        LOCALDB_LOGGER.info("updating player registry from central server")
        upstream_players = query_players(api_obj)
        self.build_registry(upstream_players)
        self._check_for_sfx_updates(api_obj)

    @staticmethod
    def _write_sfx_b64_data(data, dest):
        """Decode and write data."""
        decoded_data = base64.b64decode(data)
        try:
            with open(dest, "wb") as sfx_data_file:
                sfx_data_file.write(decoded_data)
        except OSError:
            return False
        return True

    def _check_for_sfx_updates(self, api_obj):
        """Check for SFX updates."""
        if self.sfx_path is None:
            return
        for player in self:
            failed = False
            player_sfx_path = os.path.join(self.sfx_path, player.username)
            if os.path.exists(player_sfx_path):
                download_and_write = False
                try:
                    cur_md5sum = md5_sum(player_sfx_path)
                except OSError:
                    LOCALDB_LOGGER.warning("failed to calculate SFX checksum")
                    continue
                if cur_md5sum != player.sfx_md5:
                    download_and_write = True
                    LOCALDB_LOGGER(
                        f"updating SFX data for player '{player.username}'"
                    )
            else:
                download_and_write = True
            if download_and_write is True:
                # SFX data has not been downloaded
                try:
                    data = get_sfx_data(player.username, api_obj)
                except CBCentralAPIError:
                    failed = True
                if failed is True or data["status"] != "ok":
                    LOCALDB_LOGGER.error("failed to retrieve SFX data")
                    continue

                if data["data"] is not None:
                    # write
                    LOCALDB_LOGGER.info(
                        f"writing SFX data for player '{player.username}'"
                    )
                    if (
                        self._write_sfx_b64_data(data["data"], player_sfx_path)
                        is False
                    ):
                        LOCALDB_LOGGER.error("failed to write SFX data")

    @property
    def sfx_path(self):
        """Get SFX path."""
        return self._sfx_path
