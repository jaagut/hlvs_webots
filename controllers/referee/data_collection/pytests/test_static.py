import data_collection.match_info as mi


# Create a test StaticMatchInfo object
def _create_static_match_info(id: str = "test_id") -> mi.StaticMatchInfo:
    match_type = mi.MatchType.ROUNDROBIN
    league_sub_type = mi.LeagueSubType.KID
    simulation = mi.Simulation(True, 0, 8)
    field = mi.Field("test_location_id", "test_location_name", 6.0, 9.0, 1.0)
    ball = mi.StaticBall("test_ball_id", 0.5, "test_ball_texture", 0.14)
    teams = mi.StaticTeams(
        mi.StaticTeam(
            "test_team_1",
            "test_team_1_name",
            mi.TeamColor.RED,
            mi.StaticPlayer("test_player_1", 0.5, 20, "test_platform_1", mi.Camera("test_camera_1", 42, 1.0, 42, 42)),
            mi.StaticPlayer("test_player_2", 0.5, 20, "test_platform_2", mi.Camera("test_camera_2", 42, 1.0, 42, 42)),
            mi.StaticPlayer("test_player_3", 0.5, 20, "test_platform_3", mi.Camera("test_camera_3", 42, 1.0, 42, 42)),
            mi.StaticPlayer("test_player_4", 0.5, 20, "test_platform_4", mi.Camera("test_camera_4", 42, 1.0, 42, 42))
        ),
        mi.StaticTeam(
            "test_team_2",
            "test_team_2_name",
            mi.TeamColor.BLUE,
            mi.StaticPlayer("test_player_5", 0.5, 20, "test_platform_5", mi.Camera("test_camera_5", 42, 1.0, 42, 42)),
            mi.StaticPlayer("test_player_6", 0.5, 20, "test_platform_6", mi.Camera("test_camera_6", 42, 1.0, 42, 42)),
            mi.StaticPlayer("test_player_7", 0.5, 20, "test_platform_7", mi.Camera("test_camera_7", 42, 1.0, 42, 42)),
            mi.StaticPlayer("test_player_8", 0.5, 20, "test_platform_8", mi.Camera("test_camera_8", 42, 1.0, 42, 42))
        )
    )
    kick_off_team = "test_team_1"

    static_match_info = mi.StaticMatchInfo(
        id, match_type, league_sub_type, simulation, field, ball, teams, kick_off_team
    )

    assert static_match_info.id == id
    assert static_match_info.match_type == match_type
    assert static_match_info.league_sub_type == league_sub_type
    assert static_match_info.simulation == simulation
    assert static_match_info.field == field
    assert static_match_info.ball == ball
    assert static_match_info.teams == teams

    return static_match_info


def test_create_static_match_info():
    _create_static_match_info()


def test_json_dump_and_load_static_match_info():
    static_match_info = _create_static_match_info()

    # Dump the object to a JSON string
    json_string = static_match_info.to_json()  # type: ignore

    # Load the object from the JSON string
    json_static_match_info = mi.StaticMatchInfo.from_json(json_string)

    assert (
        json_static_match_info == static_match_info
    ), f"StaticMatchInfo does not match:\nFROM JSON: {json_static_match_info}\nFROM OBJECT: {static_match_info}"


if __name__ == "__main__":
    test_create_static_match_info()
    test_json_dump_and_load_static_match_info()
