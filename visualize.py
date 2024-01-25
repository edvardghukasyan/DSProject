import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#plot: Points by Team
def points_by_name(league_table, country):
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Points', y='Team', data=league_table.sort_values(by='Points', ascending=False))
    plt.title(f'Points by Team - {country}')
    plt.xlabel('Points')
    plt.ylabel('Team')
    # Save the plot to a file
    plt.savefig(f'{country}_points_by_team.png')
    plt.close()
    return f'{country}_points_by_team.png'

#plot: Distribution of Goals Scored
def distribution_goals(league_table):
    plt.figure(figsize=(8, 6))
    sns.histplot(league_table['GoalsFor'], kde=True, bins=10)
    plt.title('Distribution of Goals Scored')
    plt.xlabel('Goals Scored')
    plt.ylabel('Frequency')
    # Save the plot to a file
    plt.savefig(f'distribution_goals.png')
    plt.close()
    return 'distribution_goals.png'

#plot: Points and Goal Difference per team

def points_and_goals(league_table):
    plt.figure(figsize=(14, 7))
    sns.barplot(x='Points', y='Team', data=league_table.sort_values('Points', ascending=False), label='Points', color='blue')
    sns.barplot(x='GoalDifference', y='Team', data=league_table.sort_values('Points', ascending=False), label='Goal Difference', color='orange')
    plt.xlabel('Points / Goal Difference')
    plt.ylabel('Team')
    plt.legend()
    plt.title('Points and Goal Difference per Team')
    # Save the plot to a file
    plt.savefig(f'points_goals.png')
    plt.close()
    return 'points_goals.png'


#plot: Distribution of Home vs Away Wins

def distribution_home_vs_away_wins(data):
    home_wins = data['FTR'].value_counts()['H']
    away_wins = data['FTR'].value_counts()['A']
    plt.figure(figsize=(8, 8))
    plt.pie([home_wins, away_wins], labels=['Home Wins', 'Away Wins'], autopct='%1.1f%%', startangle=140)
    plt.title('Distribution of Home vs Away Wins')
    # Save the plot to a file
    plt.savefig(f'distribution_home_away.png')
    plt.close()
    return 'distribution_home_away.png'

#plot: Goals For vs Goals Against per team

def goals_for_vs_against(league_table):
    plt.figure(figsize=(10, 8))
    for _, row in league_table.iterrows():
        plt.scatter(row['GoalsFor'], row['GoalsAgainst'])
        plt.annotate(row['Team'], (row['GoalsFor'], row['GoalsAgainst']), fontsize=8)

    max_goals = max(league_table['GoalsFor'].max(), league_table['GoalsAgainst'].max())
    plt.plot([0, max_goals], [0, max_goals], 'k--')

    plt.title('Goals For vs Goals Against per Team')
    plt.xlabel('Goals For')
    plt.ylabel('Goals Against')
    plt.legend(fontsize='small')
    # Save the plot to a file
    plt.savefig(f'goals_for_against.png')
    plt.close()
    return 'goals_for_against.png'


    

