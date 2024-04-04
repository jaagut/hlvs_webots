#!/usr/bin/python3

from typing import List, Optional, Tuple, Dict

import os
import sys

import pandas as pd
import robocup_extension_pb2

class TeamCommMessage:
    def __init__(self, raw: str) -> None:
        self.raw = raw

        # Extract time, sender IP, port and message
        splits = self.raw[1:-2].split(", ")  # Remove encapsulating brackets and newline, then split
        self.time = float(splits[0])
        self.sender_IP = splits[1][1:-1]  # Remove quotes
        self.sender_port = int(splits[2])
        self.message = None
        raw_message = splits[3]
        # Interpret "b'\n\x07'" kind string as byte array
        if raw_message.startswith("b'") and raw_message[-1] == "'":
            self.message = eval(raw_message)


class Message:
    def __init__(self, raw: str) -> None:
        self.raw = raw
        self.raw_bouncing_header = self.raw[:11]
        self.raw_bouncing_body = self.raw[11:]

        self.blue_IPs: List[str] = []
        self.red_IPs: List[str] = []
        self.team_comm_message: Optional[TeamCommMessage] = None

        if self.defines_team():
            self.blue_IPs = self.get_blue_team_IPs()
            self.red_IPs = self.get_red_team_IPs()
        
        if self.is_team_comm():
            self.team_comm_message = TeamCommMessage(self.raw_bouncing_body)

    def is_team_comm(self) -> bool:
        return self.raw_bouncing_body[0] == "["

    def defines_team(self) -> bool:
        return self.raw_bouncing_body.startswith("Robots in team ")

    def get_blue_team_IPs(self) -> List[str]:
        """
        Example raw body: "Robots in team blue are ['172.31.13.184', '172.31.15.77', '172.31.1.9', '172.31.8.39']"
        We want to return the list of IPs
        """
        # Check if the message is a team definition
        if not self.defines_team() or not self.raw_bouncing_body[15:19] == "blue":
            return []
        # Extract the list of IPs
        raw_IPs = self.raw_bouncing_body[25:-2]  # Remove the "Robots in team blue are " and the last "]\n"
        raw_IPs = raw_IPs.split(", ")  # Split the IPs
        raw_IPs = [raw_IP[1:-1] for raw_IP in raw_IPs]  # Remove the quotes
        return raw_IPs

    def get_red_team_IPs(self) -> List[str]:
        """
        Example raw body: "Robots in team red are ['172.31.13.184', '172.31.15.77', '172.31.1.9', '172.31.8.39']"
        We want to return the list of IPs
        """
        # Check if the message is a team definition
        if not self.defines_team() or not self.raw_bouncing_body[15:18] == "red":
            return []
        # Extract the list of IPs
        raw_IPs = self.raw_bouncing_body[24:-2]  # Remove the "Robots in team red are " and the last "]"
        raw_IPs = raw_IPs.split(", ")  # Split the IPs
        raw_IPs = [raw_IP[1:-1] for raw_IP in raw_IPs]  # Remove the quotes
        return raw_IPs


def parse_bouncing_log(bouncing_log: List[str]) -> List[Message]:
    messages = []
    for raw_message in bouncing_log:
        try:
            messages.append(Message(raw_message))
        except:
            pass
    return messages

def get_team_proto_messages(messages: List[Message]) -> Tuple[List[robocup_extension_pb2.Message], List[robocup_extension_pb2.Message]]:
    # Get the team IPs
    blue_IPs = []
    red_IPs = []
    for message in messages:
        if message.blue_IPs:
            blue_IPs = message.blue_IPs
        if message.red_IPs:
            red_IPs = message.red_IPs
        if blue_IPs and red_IPs:
            break

    # Assign the messages to the teams
    blue_messages = []
    red_messages = []

    for message in messages:
        if message.team_comm_message:
            if message.team_comm_message.sender_IP in blue_IPs:
                blue_messages.append(message)
            elif message.team_comm_message.sender_IP in red_IPs:
                red_messages.append(message)

    # Try to parse the messages
    blue_proto: List[robocup_extension_pb2.Message] = []
    red_proto: List[robocup_extension_pb2.Message] = []

    for message in blue_messages:
        if message.team_comm_message.message:
            try:
                proto = robocup_extension_pb2.Message()
                proto.ParseFromString(message.team_comm_message.message)
                blue_proto.append(proto)
            except Exception as e:
                print(e)

    for message in red_messages:
        if message.team_comm_message.message:
            try:
                proto = robocup_extension_pb2.Message()
                proto.ParseFromString(message.team_comm_message.message)
                red_proto.append(proto)
            except Exception as e:
                print(e)

    return blue_proto, red_proto

def insert_new_columns_to_df(df: pd.DataFrame) -> pd.DataFrame:
    # TODO: This adds a lot of new sparse columns
    # Consider using a sparse dataframe instead
    # An filter intelligently which columns are strictly necessary from the input data

    # Generate column names
    columns = []

    for team in [1, 2]:
        for player_id in range(1, 4+1):
            base_name = f'teams.team{team}.player{player_id}'

            # Skip if the player is not in the match
            if f'{base_name}.id' not in df.columns:
                continue

            base_name += '.team_comm'

            columns.append(f'{base_name}.self_localization.pose.position.x')
            columns.append(f'{base_name}.self_localization.pose.position.y')
            columns.append(f'{base_name}.self_localization.pose.position.z')
            for i in range(3*3):
                columns.append(f'{base_name}.self_localization.covariance.{i}')

            columns.append(f'{base_name}.walk_command.x')
            columns.append(f'{base_name}.walk_command.y')
            columns.append(f'{base_name}.walk_command.z')

            columns.append(f'{base_name}.target_pose.pose.position.x')
            columns.append(f'{base_name}.target_pose.pose.position.y')
            columns.append(f'{base_name}.target_pose.pose.position.z')
            for i in range(3*3):
                columns.append(f'{base_name}.target_pose.pose.covariance.{i}')

            columns.append(f'{base_name}.kick_target.x')
            columns.append(f'{base_name}.kick_target.y')

            columns.append(f'{base_name}.ball.position.x')
            columns.append(f'{base_name}.ball.position.y')
            columns.append(f'{base_name}.ball.position.z')
            columns.append(f'{base_name}.ball.velocity.x')
            columns.append(f'{base_name}.ball.velocity.y')
            columns.append(f'{base_name}.ball.velocity.z')
            for i in range(3*3):
                columns.append(f'{base_name}.ball.covariance.{i}')

            # Other players
            for others_team in [1, 2, "_unknown"]:
                others_player_ids = list(range(1, 4+1))
                if others_team == team:
                    others_player_ids.remove(player_id)
                if others_team == "_unknown":
                    # There is no mapping, therefore we use placeholders
                    others_player_ids = list(range(1, 7+1))
                for others_player_id in others_player_ids:
                    others_base_name = f'{base_name}.others.team{others_team}.player{others_player_id}'
                    columns.append(f'{others_base_name}.pose.position.x')
                    columns.append(f'{others_base_name}.pose.position.y')
                    columns.append(f'{others_base_name}.pose.position.z')
                    columns.append(f'{others_base_name}.confidence')
                    for i in range(3*3):
                        columns.append(f'{others_base_name}.covariance.{i}')

            # Extensions
            columns.append(f'{base_name}.time_to_ball')
            columns.append(f'{base_name}.role')
            columns.append(f'{base_name}.action')

    # New temporary dataframe to concat with the original one
    new_df = pd.DataFrame(columns=columns)
    return pd.concat([df, new_df], axis=1)

def fill_df_with_data(df: pd.DataFrame, blue_proto: List[robocup_extension_pb2.Message], red_proto: List[robocup_extension_pb2.Message]):
    def handle_team(df: pd.DataFrame, msgs, current_team: int, current_other_team: int) -> pd.DataFrame:
        for msg in msgs:
            row = {}  # This is where we collect the data from this message
            player_id = msg.current_pose.player_id
            my_team_id = msg.current_pose.team
            base_name = f'teams.team{current_team}.player{player_id}.team_comm'

            time = msg.timestamp.seconds + msg.timestamp.nanos * 1e-9

            # Skip if msg time is greater than the last time in the dataframe
            if time >= df['time'].iloc[-1]:
                continue

            idx = df['time'][df['time'] > time].index[0]  # Find the index of the first row with a time greater than the message time

            # Insert self localization
            row[f'{base_name}.self_localization.pose.position.x'] = msg.current_pose.position.x
            row[f'{base_name}.self_localization.pose.position.y'] = msg.current_pose.position.y
            row[f'{base_name}.self_localization.pose.position.z'] = msg.current_pose.position.z
            row[f'{base_name}.self_localization.pose.covariance.0'] = msg.current_pose.covariance.x.x
            row[f'{base_name}.self_localization.pose.covariance.1'] = msg.current_pose.covariance.x.y
            row[f'{base_name}.self_localization.pose.covariance.2'] = msg.current_pose.covariance.x.z
            row[f'{base_name}.self_localization.pose.covariance.3'] = msg.current_pose.covariance.y.x
            row[f'{base_name}.self_localization.pose.covariance.4'] = msg.current_pose.covariance.y.y
            row[f'{base_name}.self_localization.pose.covariance.5'] = msg.current_pose.covariance.y.z
            row[f'{base_name}.self_localization.pose.covariance.6'] = msg.current_pose.covariance.z.x
            row[f'{base_name}.self_localization.pose.covariance.7'] = msg.current_pose.covariance.z.y
            row[f'{base_name}.self_localization.pose.covariance.8'] = msg.current_pose.covariance.z.z

            # Insert walk command
            row[f'{base_name}.walk_command.x'] = msg.walk_command.x
            row[f'{base_name}.walk_command.y'] = msg.walk_command.y
            row[f'{base_name}.walk_command.z'] = msg.walk_command.z

            # Insert target pose
            row[f'{base_name}.target_pose.pose.position.x'] = msg.target_pose.position.x
            row[f'{base_name}.target_pose.pose.position.y'] = msg.target_pose.position.y
            row[f'{base_name}.target_pose.pose.position.z'] = msg.target_pose.position.z
            row[f'{base_name}.target_pose.covariance.0'] = msg.target_pose.covariance.x.x
            row[f'{base_name}.target_pose.covariance.1'] = msg.target_pose.covariance.x.y
            row[f'{base_name}.target_pose.covariance.2'] = msg.target_pose.covariance.x.z
            row[f'{base_name}.target_pose.covariance.3'] = msg.target_pose.covariance.y.x
            row[f'{base_name}.target_pose.covariance.4'] = msg.target_pose.covariance.y.y
            row[f'{base_name}.target_pose.covariance.5'] = msg.target_pose.covariance.y.z
            row[f'{base_name}.target_pose.covariance.6'] = msg.target_pose.covariance.z.x
            row[f'{base_name}.target_pose.covariance.7'] = msg.target_pose.covariance.z.y
            row[f'{base_name}.target_pose.covariance.8'] = msg.target_pose.covariance.z.z

            # Insert kick target
            row[f'{base_name}.kick_target.x'] = msg.kick_target.x
            row[f'{base_name}.kick_target.y'] = msg.kick_target.y

            # Insert ball observation
            row[f'{base_name}.ball.position.x'] = msg.ball.position.x
            row[f'{base_name}.ball.position.y'] = msg.ball.position.y
            row[f'{base_name}.ball.position.z'] = msg.ball.position.z
            row[f'{base_name}.ball.velocity.x'] = msg.ball.velocity.x
            row[f'{base_name}.ball.velocity.y'] = msg.ball.velocity.y
            row[f'{base_name}.ball.velocity.z'] = msg.ball.velocity.z
            row[f'{base_name}.ball.covariance.0'] = msg.ball.covariance.x.x
            row[f'{base_name}.ball.covariance.1'] = msg.ball.covariance.x.y
            row[f'{base_name}.ball.covariance.2'] = msg.ball.covariance.x.z
            row[f'{base_name}.ball.covariance.3'] = msg.ball.covariance.y.x
            row[f'{base_name}.ball.covariance.4'] = msg.ball.covariance.y.y
            row[f'{base_name}.ball.covariance.5'] = msg.ball.covariance.y.z
            row[f'{base_name}.ball.covariance.6'] = msg.ball.covariance.z.x
            row[f'{base_name}.ball.covariance.7'] = msg.ball.covariance.z.y
            row[f'{base_name}.ball.covariance.8'] = msg.ball.covariance.z.z

            # Insert other players
            current_team_count = current_other_team_count = unknown_count = -1
            count = 0
            for i, other in enumerate(msg.others):
                # Determine team (mine, opponent, or unknown)
                if other.team == my_team_id:
                    others_team = current_team
                    current_team_count += 1
                    count = current_team_count
                elif other.team != 0:
                    others_team = current_other_team
                    current_other_team_count += 1
                    count = current_other_team_count
                else:
                    others_team = "_unknown"
                    unknown_count += 1
                    count = unknown_count
                # We ignore the player_id field because no team detects the player number

                others_base_name = f'{base_name}.others.team{others_team}.player{count}'
                
                # Insert pose
                row[f'{others_base_name}.pose.position.x'] = other.position.x
                row[f'{others_base_name}.pose.position.y'] = other.position.y
                row[f'{others_base_name}.pose.position.z'] = other.position.z

                # Insert confidence
                confidence = None
                if len(msg.other_robot_confidence) > i:
                    confidence = msg.other_robot_confidence[i]
                row[f'{others_base_name}.confidence'] = confidence

                # Insert covariance
                row[f'{others_base_name}.covariance.0'] = other.covariance.x.x
                row[f'{others_base_name}.covariance.1'] = other.covariance.x.y
                row[f'{others_base_name}.covariance.2'] = other.covariance.x.z
                row[f'{others_base_name}.covariance.3'] = other.covariance.y.x
                row[f'{others_base_name}.covariance.4'] = other.covariance.y.y
                row[f'{others_base_name}.covariance.5'] = other.covariance.y.z
                row[f'{others_base_name}.covariance.6'] = other.covariance.z.x
                row[f'{others_base_name}.covariance.7'] = other.covariance.z.y
                row[f'{others_base_name}.covariance.8'] = other.covariance.z.z

            # Insert extensions
            row[f'{base_name}.time_to_ball'] = msg.time_to_ball
            row[f'{base_name}.role'] = msg.role
            row[f'{base_name}.action'] = msg.action

            # Insert the column data from row into the dataframe at the index
            for col, value in row.items():
                df.at[idx, col] = value

        return df

    # Blue is team1, red is team2
    # Insert blue data
    df = handle_team(df, blue_proto, 1, 2)
    df = handle_team(df, red_proto, 2, 1)

    return df

if __name__ == "__main__":
    match_dir = sys.argv[1]

    # Read the bouncing log file
    with open(os.path.join(match_dir, "bouncing_log.txt"), "r") as f:
        bouncing_log: List[str] = f.readlines()

    # Parse the bouncing log file
    messages = parse_bouncing_log(bouncing_log)

    # Get the team proto messages
    blue_proto, red_proto = get_team_proto_messages(messages)
    print(len(red_proto))
    exit(0)

    # Load the match data collection
    # Find files that match the pattern "referee_data_collection_*.feather"
    feather_file = None
    data_collection_dir = os.path.join(match_dir, "data_collection")
    for file in os.listdir(data_collection_dir):
        if file.startswith("referee_data_collection_") and file.endswith(".feather"):
            feather_file = file
            break

    if feather_file is None:
        print("No referee data collection file found")
        exit(1)

    # Load the data
    referee_data_collection = pd.read_feather(os.path.join(data_collection_dir, feather_file))

    # Insert new columns
    referee_data_collection = insert_new_columns_to_df(referee_data_collection)

    # Fill the new columns with the proto messages
    referee_data_collection = fill_df_with_data(referee_data_collection, blue_proto, red_proto)

    # Save the new dataframe as feather
    feather_file = feather_file.replace(".feather", "_with_team_communication.feather")
    #referee_data_collection.to_feather(os.path.join(data_collection_dir, feather_file))
