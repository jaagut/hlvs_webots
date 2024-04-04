#!/usr/bin/python3

from typing import Dict

import json
import sys


def fill_in_additional_player_data(data_collection: Dict, additional_data: Dict):
    """
    Fills in the additional player data to the data collection (in place)

    :param data_collection: Dict from the data collection json file
    :type data_collection: Dict
    :param additional_data: Dict from the additional data json file
    :type additional_data: Dict
    """
    # Iterate over teams and players in the data collection
    for team in data_collection["teams"].values():
        for player_key in ["player1", "player2", "player3", "player4"]:
            # Get the player from the team
            player = team[player_key]

            if player is None:
                continue

            # Get the player's platform to match the additional data
            player_platform = player["platform"]

            # Get the additional data for the player
            player_additional_data = additional_data[player_platform]

            # Add the additional data to the player
            player.update(player_additional_data)


if __name__ == "__main__":
    # Load the path to the additional data json file
    with open(sys.argv[1], "r") as f:
        additional_data = json.load(f)

    data_collection_path = sys.argv[2]

    # Load the data collection json file
    with open(data_collection_path, "r") as f:
        data_collection = json.load(f)

    # Fill in the additional data
    fill_in_additional_player_data(data_collection, additional_data)

    # Save the modified data collection json file
    with open(data_collection_path, "w") as f:
        json.dump(data_collection, f, indent=4)
