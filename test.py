"""Test API access and db mirroring."""

from cbcentral.localdb.announcement import LocalAnnounceRegistry
from cbcentral.localdb.game import LocalGameRegistry
from cbcentral.localdb.tournament import LocalTournamentRegistry
from cbcentral.localdb.player import LocalPlayerRegistry
from cbcentral.api import ChainballCentralAPI

import logging

DB_PATH = "db"
SFX_PATH = "sfx"

if __name__ == "__main__":

    logging.basicConfig(
        level=logging.NOTSET,
        format="%(asctime)s - %(name)s -" " %(levelname)s - %(message)s",
    )

    logging.root.setLevel(logging.NOTSET)
    logger = logging.getLogger("cbcentral")
    logger.info("Starting test")

    api = ChainballCentralAPI(
        "http://www.chainball.online",
        "API_KEY",
    )
    game_registry = LocalGameRegistry(DB_PATH)
    tournament_registry = LocalTournamentRegistry(DB_PATH)
    announcement_registry = LocalAnnounceRegistry(DB_PATH)
    player_registry = LocalPlayerRegistry(DB_PATH, SFX_PATH)

    # download data
    game_registry.update_registry(api)
    tournament_registry.update_registry(api)
    announcement_registry.update_registry(api)
    player_registry.update_registry(api)

    # save
    game_registry.commit_registry()
    tournament_registry.commit_registry()
    announcement_registry.commit_registry()
    player_registry.commit_registry()
