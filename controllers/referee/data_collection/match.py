from typing import List

from data_collection.match_info.ball import Ball
from data_collection.match_info.field import Field
from data_collection.match_info.simulation import Simulation
from data_collection.match_info.static import MatchType
from data_collection.match_info.team import Teams
from data_collection.step import Step


class Match:
    def __init__(
        self,
        id: str,
        type: MatchType,
        simulation: Simulation,
        field: Field,
        ball: Ball,
        teams: Teams,
    ) -> None:
        """Holds data about a match.

        :param id: Match id
        :type id: str
        :param type: Type of this match (KnockOut, RoundRobin, DropIn)
        :type type: MatchType
        :param simulation: Simulation data
        :type simulation: Simulation
        :param field: Field data
        :type field: Field
        :param ball: Ball data
        :type ball: Ball
        :param teams: Team data
        :type teams: Teams
        """
        self.id: str = id
        self.type: MatchType = type
        self.simulation: Simulation = simulation
        self.field: Field = field
        self.ball: Ball = ball
        self.teams: Teams = teams

        self.steps: List[Step] = []

    def add_step(self, step: Step) -> None:
        """Add a step to the match.

        :param step: Step data
        :type step: Step
        """
        self.steps.append(step)

    def current_step(self) -> Step:
        """Get the current step.

        :raises Exception: If there are no steps in the match
        :return: Current step
        :rtype: Step
        """
        if len(self.steps) == 0:
            raise Exception("No steps in match")
        return self.steps[-1]