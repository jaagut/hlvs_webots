from dataclasses import dataclass
from enum import IntEnum, unique
from typing import Optional, Tuple

from dataclasses_json import DataClassJsonMixin

from .player import Player, StaticPlayer


@unique
class TeamColor(IntEnum):
    """Enum for team colors.
    Inferred from the GameState struct
    """

    BLUE = 0
    RED = 1
    YELLOW = 2
    BLACK = 3
    WHITE = 4
    GREEN = 5
    ORANGE = 6
    PURPLE = 7
    BROWN = 8
    GRAY = 9


@dataclass(frozen=True)
class StaticTeam:
    """Static information about a team.

    :param id: Team id
    :type id: str
    :param name: Team name
    :type name: str
    :param color: Team color
    :type color: TeamColor
    :param player1: First player
    :type player1: StaticPlayer
    :param player2: Second player
    :type player2: StaticPlayer
    :param player3: Third player
    :type player3: StaticPlayer
    :param player4: Fourth player
    :type player4: StaticPlayer
    """

    id: str
    name: str
    color: TeamColor

    player1: StaticPlayer
    player2: StaticPlayer
    player3: StaticPlayer
    player4: StaticPlayer


@dataclass(frozen=True)
class StaticTeams:
    """Static information about the teams.

    :param team1: First team
    :type team1: StaticTeam
    :param team2: Second team
    :type team2: StaticTeam
    """

    team1: StaticTeam
    team2: StaticTeam

    def get_teams(self) -> Tuple[StaticTeam, StaticTeam]:
        """Returns the teams.

        :return: Teams
        :rtype: Tuple[StaticTeam, StaticTeam]
        """
        return self.team1, self.team2

    def get_team_by_id(self, id: str) -> StaticTeam:
        """Returns the team with the given id.

        :param id: Id of the team
        :type id: str
        :raises ValueError: If no team with the given id exists
        :return: Team with the given id
        :rtype: StaticTeam
        """
        for team in self.get_teams():
            if team.id == id:
                return team
        raise ValueError(f"Team with id {id} not found")

    def get_team_by_color(self, color: TeamColor) -> StaticTeam:
        """Returns the team with the given color.

        :param color: Color of the team
        :type color: TeamColor
        :raises ValueError: If no team with the given color exists
        :return: Team with the given color
        :rtype: StaticTeam
        """
        for team in self.get_teams():
            if team.color == color:
                return team
        raise ValueError(f"Team with color {color} not found")

    def red(self) -> StaticTeam:
        """Returns the red team.

        :raises ValueError: If no red team exists
        :return: Red team
        :rtype: StaticTeam
        """
        return self.get_team_by_color(TeamColor.RED)

    def blue(self) -> StaticTeam:
        """Returns the blue team.

        :raises ValueError: If no blue team exists
        :return: Blue team
        :rtype: StaticTeam
        """
        return self.get_team_by_color(TeamColor.BLUE)

    def get_team_by_name(self, name: str) -> StaticTeam:
        """Returns the team with the given name.

        :param name: Name of the team
        :type name: str
        :raises ValueError: If no team with the given name exists
        :return: Team with the given name
        :rtype: StaticTeam
        """
        for team in self.get_teams():
            if team.name == name:
                return team
        raise ValueError(f"Team with name {name} not found")


@dataclass
class Team(DataClassJsonMixin):
    """Dynamic data about a team.
    :param id: Team id
    :type id: str
    :param player1: First player, defaults to None
    :type player1: Optional[Player], optional
    :param player2: Second player, defaults to None
    :type player2: Optional[Player], optional
    :param player3: Third player, defaults to None
    :type player3: Optional[Player], optional
    :param player4: Fourth player, defaults to None
    :type player4: Optional[Player], optional
    :param score: Score, defaults to 0
    :type score: int, optional
    :param penalty_shots: Penalty shots, defaults to 0
    :type penalty_shots: int, optional
    :param single_shots: Single shots (bits represent penalty shot success), defaults to 0
    :type single_shots: int, optional
    """

    id: str

    player1: Optional[Player] = None
    player2: Optional[Player] = None
    player3: Optional[Player] = None
    player4: Optional[Player] = None

    score: int = 0
    penalty_shots: int = 0
    single_shots: int = 0  # TODO: What is this?


@dataclass(frozen=True)
class Teams(DataClassJsonMixin):
    """Holds both teams.

    :param team1: First team
    :type team1: Team
    :param team2: Second team
    :type team2: Team
    """

    team1: Team
    team2: Team

    def get_teams(self) -> Tuple[Team, Team]:
        """Returns the teams.

        :return: Teams
        :rtype: Tuple[Team, Team]
        """
        return self.team1, self.team2

    def get_team_by_id(self, id: str) -> Team:
        """Returns the team with the given id.

        :param id: Id of the team
        :type id: str
        :raises ValueError: If no team with the given id exists
        :return: Team with the given id
        :rtype: Team
        """
        for team in self.get_teams():
            if team.id == id:
                return team
        raise ValueError(f"Team with id {id} not found")
