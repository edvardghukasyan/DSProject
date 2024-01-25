import pandas as pd
import numpy as np

def get_team_by_rank(rank, league_table):
    try:
        adjusted_rank = rank - 1
        if 0 <= adjusted_rank < len(league_table):
            return league_table.iloc[adjusted_rank]['Team']
        else:
            return "Rank out of range"
    except Exception as e:
        return f"An error occurred: {e}"


def get_team_by_goals_for_rank(rank, league_table):
    try:
        sorted_table = league_table.sort_values(by='GoalsFor', ascending=False).reset_index(drop=True)
        adjusted_rank = rank - 1
        if 0 <= adjusted_rank < len(sorted_table):
            team = sorted_table.iloc[adjusted_rank]['Team']
            goals_for = sorted_table.iloc[adjusted_rank]['GoalsFor']
            return team, goals_for
        else:
            return "Rank out of range", None
    except Exception as e:
        return f"An error occurred: {e}", None


def get_team_by_goal_difference_rank(rank, league_table):
    try:
        sorted_table = league_table.sort_values(by='GoalDifference', ascending=False).reset_index(drop=True)

        adjusted_rank = rank - 1
        if 0 <= adjusted_rank < len(sorted_table):
            team = sorted_table.iloc[adjusted_rank]['Team']
            goal_difference = sorted_table.iloc[adjusted_rank]['GoalDifference']
            return team, goal_difference
        else:
            return "Rank out of range", None
    except Exception as e:
        return f"An error occurred: {e}", None


def get_rank_by_team(team_name, league_table):
    try:
        team_row = league_table[league_table['Team'] == team_name]
        if not team_row.empty:
            rank = team_row.iloc[0]['Rank']
            return int(rank) if isinstance(rank, np.int64) else rank
        else:
            return "Team not found in league table"
    except Exception as e:
        return f"An error occurred: {e}"

