import pandas as pd
import json
from visualize import points_by_name, distribution_goals, points_and_goals, goals_for_vs_against
from get_team import get_team_by_rank, get_team_by_goals_for_rank, get_team_by_goal_difference_rank

def load_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def perform_analysis(data):
    for country, league_data in data.items():
        print(f"\nAnalyzing data for {country}:")

        league_table = pd.read_json(league_data['league_table'])
        data = pd.read_json(league_data['data'])

        print(f"Visualizing Points by Team for {country}")
        points_by_name(league_table)

        print(f"Visualizing Distribution of Goals Scored for {country}")
        distribution_goals(league_table)

        print(f"Visualizing Points and Goals for {country}")
        points_and_goals(league_table)

        print(f"Visualizing Distribution of for Goals vs against Goals for {country}")
        goals_for_vs_against(league_table)

        rank = 1
        team = get_team_by_rank(rank, league_table)
        print(f"Team at rank {rank} in {country}: {team}")

        team = get_team_by_goals_for_rank(rank, league_table)
        print(f"Team at goals rank {rank} in {country}: {team}")

        team = get_team_by_goal_difference_rank(rank, league_table)
        print(f"Team at goals difference rank {rank} in {country}: {team}")

if __name__ == "__main__":
    file_path = 'football_data.json'
    all_data = load_data(file_path)
    perform_analysis(all_data)
