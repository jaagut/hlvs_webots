from typing import List, Optional, Tuple

from data_collection.match_info.match_object import MatchObject
from data_collection.match_info.ball import Ball
from data_collection.match_info.team import Team, Teams
from data_collection.match_info.player import Player
from forceful_contact_matrix import ForcefulContactMatrix


class Step:
    def __init__(
        self,
        id: int,
        time: Tuple[int],
        time_to_calculate_simulation: Optional[Tuple[int]] = None,
    ) -> None:
        """Holds data about a step.

        :param id: Step id
        :type id: int
        :param time: Time of step (seconds, milliseconds)
        :type time: Tuple[int]
        :param time_to_calculate_simulation: Time to calculate simulation (seconds, milliseconds)
        :type time_to_calculate_simulation: Optional[Tuple[int]]
        """
        self.id: int = id
        self.time: Tuple[int] = time
        self.time_to_calculate_simulation: Optional[
            Tuple[int]
        ] = time_to_calculate_simulation

        self.ball: Optional[Ball] = None
        self.teams: Optional[Teams] = None
        self.collision_matrix: Optional[ForcefulContactMatrix] = None
        # TODO: GameController events

        def set_ball(self, ball: Ball) -> None:
            """Set ball data.

            :param ball: Ball data
            :type ball: Ball
            """
            self.ball = ball

        def set_teams(self, teams: Teams) -> None:
            """Set team data.

            :param teams: Team data
            :type teams: Teams
            """
            self.teams = teams

        def set_collision_matrix(self, collision_matrix: ForcefulContactMatrix) -> None:
            """Set collision matrix.

            :param collision_matrix: Collision matrix
            :type collision_matrix: ForcefulContactMatrix
            """
            self.collision_matrix = collision_matrix