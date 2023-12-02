import requests
import pandas as pd
from nba_api.stats.endpoints import leaguegamefinder

player_name = 'Avdija'
substitution_action_type = 'substitution'
headers = {
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-nba-stats-token': 'true',
    'x-nba-stats-origin': 'stats',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-Mode': 'cors',
    'Referer': 'https://stats.nba.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
}


def format_df(df):
    for index, row in df.iterrows():
        df.at[index, 'clock'] = df.at[index, 'clock'].replace("PT", "")
        df.at[index, 'clock'] = df.at[index, 'clock'].replace("M", "")
        df.at[index, 'clock'] = df.at[index, 'clock'].replace(".00S", "")
        df.at[index, 'clock'] = df.at[index, 'clock'][:2] + ':' + df.at[index, 'clock'][2:]
    return df


def get_subs_time(gameId):
    play_by_play_url = f"https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{gameId}.json"
    response = requests.get(url=play_by_play_url, headers=headers).json()
    subs_plays = []
    play_by_play = response['game']['actions']
    for play in play_by_play:
        if play['actionType'] == substitution_action_type and play['playerName'] == player_name:
            subs_plays.append(play)
    return format_df(pd.DataFrame(subs_plays))


gamefinder = leaguegamefinder.LeagueGameFinder(season_nullable='2023-24',
                                               league_id_nullable='00',
                                               season_type_nullable='Regular Season')
washington_games = []
games = pd.DataFrame(gamefinder.get_data_frames()[0][["TEAM_NAME", "GAME_ID"]])
for index, game in games.iterrows():
    if game['TEAM_NAME'] == 'Washington Wizards':
        washington_games.append(game['GAME_ID'])
game_id = washington_games[0]

df = get_subs_time(game_id)

print(df[['period', 'clock', 'subType', 'playerName']])
