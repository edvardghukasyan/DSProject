from data_processing import get_data
import json

def update_data():
    countries = ['England', 'Spain', 'Germany', 'Italy']
    urls = {
        'England': "https://www.football-data.co.uk/mmz4281/2324/E0.csv",
        'Spain': "https://www.football-data.co.uk/mmz4281/2324/SP1.csv",
        'Germany': "https://www.football-data.co.uk/mmz4281/2324/D1.csv",
        'Italy': "https://www.football-data.co.uk/mmz4281/2324/I1.csv"
    }

    all_data = {}
    for country in countries:
        data, league_table = get_data(urls[country])
        all_data[country] = {
            'data': data.to_json(),
            'league_table': league_table.to_json()
        }

    with open('football_data.json', 'w') as file:
        json.dump(all_data, file)

if __name__ == '__main__':
    update_data()
