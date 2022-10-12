from bs4 import BeautifulSoup as bs
import requests
import lxml
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

APIKEY = os.environ.get('STEAM_APIKEY')

#  http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key=XXXXXXXXXXXXXXXXX&steamid=76561197960434622&format=json
def owned_games_url(userid):
    prefix = 'http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='
    url = prefix + APIKEY + '&steamid=' + userid + '&format=json'
    return(call(url))

def call(url):
    response = requests.get(url)
    try:
        json_response = response.json()['response']['games']
    except KeyError:
        print(response.json())
        return response.json()
    return json_response

def create_games_dict(json_response):
    appid_list = []
    playtime_list = []
    for line in json_response:
        appid_list.append(line['appid'])
        playtime_list.append(line['playtime_forever'])
    game_dict = dict(zip(appid_list, playtime_list))
    return game_dict

def get_all(userid):
    try:
        json_response = owned_games_url(userid)
        game_dict = create_games_dict(json_response)
        df = handle_df(json_response)
        summary = get_summaries(df)
        return(df, get_summaries(df))
    except requests.exceptions.JSONDecodeError:
        print('No information found, please make sure your information is non-private')

def get_app_names():
    response = requests.get('https://api.steampowered.com/ISteamApps/GetAppList/v2/')
    app_df = pd.DataFrame(response.json()['applist']['apps'])
    app_df = app_df[app_df['name'] != '']
    return app_df

def handle_df(game_dict):
    df = pd.DataFrame(game_dict).drop(['playtime_windows_forever',
        'playtime_mac_forever', 'playtime_linux_forever'], axis=1) 
    _ = df[~df['playtime_2weeks'].isnull()]
    df['playtime_hours'] = _['playtime_2weeks'].apply(lambda x: x /60)
    app_df = get_app_names()
    df = df.merge(app_df, on='appid', how='left')
    return df

def get_summaries(df):
    summary = {}
    summary['total_h'] = round(df.playtime_forever.sum()/60,2)
    summary['games_owned'] = df.appid.nunique()
    summary['games_never_played'] = round(df[df['playtime_forever'] == 0]['appid'].count(),2)
    mask = ~df['playtime_2weeks'].isnull()
    summary['playtime_hr_2weeks'] = round(df[mask]['playtime_2weeks'].sum()/60,2)
    summary['daily_2weeks'] = round(summary['playtime_hr_2weeks']/14, 2)
    return summary









# Falc: 76561198011821616
# Steve: 76561197981558881
# Gate: 76561198027985875
    # pic2 = plt.pie([daily_avg, day_sleep, day_work, day_max - day_sleep - day_work - daily_avg],
    #     labels = ['video_games', '8hr sleep', 'day_work', 'remaining_time'],
    #     autopct=lambda x: '{:.0f}'.format(x*24/100))

# print(sum(game_dict.values()))
# print(str(sum(game_dict.values())/60) + 'hrs')
# print(str(sum(game_dict.values())/60/16) + 'waking days')
# put table in html to display df