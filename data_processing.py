from scraping import scrape_data
import pandas as pd

#processing data
def process_data(data):
    if data is not None:
        processed_data = data[['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']]
        processed_data = processed_data.dropna()
        return processed_data
    else:
        return None

#calculating each team points
def calculate_points(row):
    if row['FTR'] == 'H':
        return {'HomePoints': 3, 'AwayPoints': 0}
    elif row['FTR'] == 'A':
        return {'HomePoints': 0, 'AwayPoints': 3}
    else:
        return {'HomePoints': 1, 'AwayPoints': 1}

#creating table for that league
def create_league_table(data):
    points_data = []
    for _, row in data.iterrows():
        match_points = calculate_points(row)
        points_data.append({
            'Team': row['HomeTeam'],
            'Points': match_points['HomePoints'],
            'GoalsFor': row['FTHG'],
            'GoalsAgainst': row['FTAG']
        })
        points_data.append({
            'Team': row['AwayTeam'],
            'Points': match_points['AwayPoints'],
            'GoalsFor': row['FTAG'],
            'GoalsAgainst': row['FTHG']
        })

    points_df = pd.DataFrame(points_data)

    league_table = points_df.groupby('Team').agg({
        'Points': 'sum',
        'GoalsFor': 'sum',
        'GoalsAgainst': 'sum'
    }).reset_index()

    league_table['GoalDifference'] = league_table['GoalsFor'] - league_table['GoalsAgainst']
    league_table = league_table.sort_values(by=['Points', 'GoalDifference'], ascending=False)

    league_table = league_table.reset_index()
    del league_table["index"]

    league_table["Rank"] = range(1, len(league_table) + 1)

    new_order = ["Rank", "Team", "Points", "GoalsFor", "GoalsAgainst", "GoalDifference"]
    league_table = league_table[new_order]

    return league_table

#get scrapped data and league's table data
def get_data(url):
    data = scrape_data(url)

    processed_data = process_data(data)
    league_table = create_league_table(processed_data)

    return data, league_table
