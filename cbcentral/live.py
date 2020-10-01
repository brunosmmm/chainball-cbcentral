"""Live updates."""

import json

from cbcentral.api import ChainballCentralAPI


def push_event(handler: ChainballCentralAPI, game_uuid, evt_type, evt_desc):
    """Push event to server."""
    post_data = {"evt_type": evt_type, "evt_data": evt_desc}
    data_dump = {"payload": json.dumps(post_data)}
    handler.push_post_request(
        data_dump, sub_api="api", path=f"games/{game_uuid}/push_event/"
    )


def game_start(
    handler: ChainballCentralAPI, game_uuid, start_time, player_order
):
    """Start game."""
    order = ",".join(player_order)
    post_data = {"start_time": start_time, "player_order": order}
    data_dump = {"payload": json.dumps(post_data)}
    handler.push_post_request(
        data_dump, sub_api="api", path=f"games/{game_uuid}/start_game/"
    )


def game_end(
    handler: ChainballCentralAPI(),
    game_uuid,
    reason,
    winner,
    running_time,
    remaining_time,
):
    """End game."""
    post_data = {
        "reason": reason,
        "winner": winner,
        "running_time": running_time,
        "remaining_time": remaining_time,
    }
    data_dump = {"payload": json.dumps(post_data)}
    handler.push_post_request(
        data_dump, sub_api="api", path=f"games/{game_uuid}/stop_game/"
    )
