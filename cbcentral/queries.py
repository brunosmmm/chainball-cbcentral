"""Query information using central API."""


def query_players(api_obj):
    """Query registered players from central server."""
    return api_obj.central_api_get(sub_api="api", path="players")


def query_tournaments(api_obj):
    """Query tournaments."""
    return api_obj.central_api_get(sub_api="api", path="tournaments")


def query_games(api_obj):
    """Query games."""
    return api_obj.central_api_get(sub_api="api", path="games")


def query_announcements(api_obj):
    """Query announcements."""
    return api_obj.central_api_get(sub_api="api", path="announce")


def get_sfx_data(player, api_obj):
    """Get player SFX data."""
    return api_obj.central_api_get(
        sub_api="api", path=f"players/{player}/get_sfx_data"
    )
