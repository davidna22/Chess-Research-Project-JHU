import requests
import logging
import urllib
import json
import numpy as np
import ndjson
import pandas as pd
import time


## Modified Requestor Class from open Source
## Berserk Repo
class LichessRequestor():
    
    """Encapsulates the logic for making a request.
    :param session: the authenticated session object
    :type session: :class:`requests.Session`
    :param str base_url: the base URL for requests
    :param Token: API Token taken from user account
    """
    def __init__(self, Token = "", base_url = ""):
        self.session = requests.session()
        self.token = Token
        self.session.headers = {'Authorization': f'Bearer {Token}'}
        self.base_url = base_url

    def request(self, method, path, converter=None, **kwargs):
        """Make a request for a resource in a paticular format.
        :param str method: HTTP verb
        :param str path: the URL suffix
        :param fmt: JSON Handler
        :param func converter: function to handle field conversions
        :return: response
        """
        url = urllib.parse.urljoin(self.base_url, path)
        kwargs['headers'] = {"Accept": "application/x-ndjson"}
        try:
            response = self.session.request(method, url, **kwargs)
        except requests.RequestException as e:
            raise exceptions(e)

        return response

    def close(self):
        self.session.close()

    def get(self, **kwargs):
        """Convenience method to make a GET request."""
        return self.request('GET', **kwargs)
    
    
    def parse(response, convert=False):
        """Method to parse data.
        :param bool convert: if true, return dataframe else json
        """
        if convert:
            return
        else:
            return response.json(cls=ndjson.Decoder)
        

    def parse_team(user_data):
        """Method to parse user data (profile, country, rating, num games)
        return dataframe of user data
        """
        data = {'id': [], 'Blitz_Games': [], 'Blitz_rating': [], 'Bullet_Games': [], 'Bullet_rating': [], 
        'Rapid_Games': [], 'Rapid_rating': [], 'country': []}
        for user in user_data:
            data['id'].append(user['id'])
            data['Blitz_Games'].append(user['perfs']['blitz']['games'])
            data['Blitz_rating'].append(user['perfs']['blitz']['rating'])
            data['Bullet_Games'].append(user['perfs']['bullet']['games'])
            data['Bullet_rating'].append(user['perfs']['bullet']['rating'])
            data['Rapid_Games'].append(user['perfs']['rapid']['games'])
            data['Rapid_rating'].append(user['perfs']['rapid']['rating'])
            if 'profile' in user:
                if 'country' in user['profile']:
                    data['country'].append(user['profile']['country'])
                else:
                    data['country'].append("No Country")
            else:
                data['country'].append("No Country")
            
        
        return pd.DataFrame(data)
    
    def parse_games(game_data, Requestor):
        data = {'gameid': [], 'white_id': [], 'white_rating': [], 'white_country': [], 'white_games': [], 'white_win_last_10': [],
                'white_inaccuracies': [], 'white_mistakes': [], 'white_blunder':[], 'white_acpl': [],
                'black_id': [], 'black_rating': [], 'black_country': [], 'black_games': [], 'black_win_last_10': [],
                'black_inaccuracies': [], 'black_mistakes': [], 'black_blunder':[], 'black_acpl': [],
                'game_type': [], 'opening': [], 'winner': [], 'win_by': []}
        for game in game_data:
            data['gameid'].append(game['id'])
            data['white_id'].append(game['players']['white']['user']['id'])
            data['white_rating'].append(game['players']['white']['rating'])
            data['white_inaccuracies'].append(game['players']['white']['analysis']['inaccuracy'])
            data['white_mistakes'].append(game['players']['white']['analysis']['mistake'])
            data['white_blunder'].append(game['players']['white']['analysis']['blunder'])
            data['white_acpl'].append(game['players']['white']['analysis']['acpl'])
            data['black_id'].append(game['players']['black']['user']['id'])
            data['black_rating'].append(game['players']['black']['rating'])
            data['black_inaccuracies'].append(game['players']['black']['analysis']['inaccuracy'])
            data['black_mistakes'].append(game['players']['black']['analysis']['mistake'])
            data['black_blunder'].append(game['players']['black']['analysis']['blunder'])
            data['black_acpl'].append(game['players']['black']['analysis']['acpl'])
            data['game_type'].append(game['speed'])
            if 'opening' in game:
                data['opening'].append(game['opening']['name'])
            else:
                data['opening'].append("Unknown")
            
            if 'winner' in game:
                data['winner'].append(game['winner'])
            else:
                data['winner'].append(game['status'])
            
            data['win_by'].append(game['status'])
            
            data['white_country'].append("NEEDFILL")
            ## Fill this value temporarily with the game created at time
            data['white_games'].append(-1)
                
            
            data['white_win_last_10'].append(game['createdAt'])
    
            ## Black details
            data['black_country'].append("NEEDFILL")   
            data['black_games'].append(-1)
         
                    
            data['black_win_last_10'].append(-1)

        return pd.DataFrame(data)
    
    ## Data type must be a list/dictionary for speed purposes
    def parse_countries(data_list):
        games_data = data_list
        for index in range(len(games_data['gameid'])):
            game_type = games_data['game_type'][index]
            API_URL = 'https://lichess.org/'
            AccessToken = "lip_FdeTEN7DhU3ge3Eg8Shu"
            
            ## White details
            api = LichessRequestor(Token = AccessToken, base_url = API_URL)
            white_id = games_data['white_id'][index]
            if(np.isnan(games_data['white_games'][index])):
                path_white = f'api/user/{white_id}'

                white = LichessRequestor.parse(api.get(path=path_white))       
                if 'profile' in white[0]:
                    if 'country' in white[0]['profile']:
                        games_data['white_country'][index] = (white[0]['profile']['country'])
                    else:
                        games_data['white_country'][index] = ("No Country")
                else:
                    games_data['white_country'][index] = "No Country"

                try:
                    games_data['white_games'][index] = white[0]['perfs'][game_type]['games']
                except:
                    games_data['white_games'][index] = -1
                    pass
                
                
            ## Black details
            if(np.isnan(games_data['black_games'][index])):
                api = LichessRequestor(Token = AccessToken, base_url = API_URL)
                black_id = games_data['black_id'][index]
                path_black = f'api/user/{black_id}'
                black = LichessRequestor.parse(api.get(path=path_black))       
                if 'profile' in black[0]:
                    if 'country' in black[0]['profile']:
                        games_data['black_country'][index] = (black[0]['profile']['country'])
                    else:
                        games_data['black_country'][index] = ("No Country")
                else:
                    games_data['black_country'][index] = "No Country"

                try:
                    games_data['black_games'][index] = black[0]['perfs'][game_type]['games']
                except:
                    games_data['black_games'][index] = -1
                    pass
    
        return pd.DataFrame(games_data)
    
    
    ## Data type must be a list/dictionary for speed purposes
    def parse_winstreak(data_list):
        games_data_list = data_list
        for index in range(len(games_data_list['gameid'])):
            print(index)
            game_type = games_data_list['game_type'][index]
            game_time = games_data_list['white_win_last_10'][index]
            API_URL = 'https://lichess.org/'
            AccessToken = "lip_FdeTEN7DhU3ge3Eg8Shu"
            params = {
                'max': 10,
                'until': game_time,
                'rated': True,
                'perfType': game_type, 
                'tags': False,
                'moves': False,
                'clock': False
            }
            
            ## White details
            white_id = games_data_list['white_id'][index]
            path_wg = f'api/games/user/{white_id}' 
            api = LichessRequestor(Token = AccessToken, base_url = API_URL)
            
            ## Some JSON Decode errors because of API
            while True:
                try:
                    white_games = LichessRequestor.parse(api.get(path=path_wg, params=params))
                except ValueError:
                    print("JSON Error - White")
                    print(api.get(path=path_wg, params=params).content)
                    time.sleep(2)
                    continue
                break;
            
            wins = 0
            for g in white_games:
                if 'winner' in g:
                    winner = g['winner']
                    if (white_id == g['players'][winner]['user']['id']):
                        wins += 1 
            games_data_list['white_win_last_10'][index] = wins
            
            
            api.close()
            time.sleep(0.5)
                          
            ## black details
            black_id = games_data_list['black_id'][index]
            path_bg = f'api/games/user/{black_id}' 
            api = LichessRequestor(Token = AccessToken, base_url = API_URL)
            
            ## Some JSON Decode errors because of API
            while True:
                try:
                    black_games = LichessRequestor.parse(api.get(path=path_bg, params=params))
                except ValueError:
                    print("JSON Error - Black")
                    print(api.get(path=path_bg, params=params).content)
                    games_data_list['black_win_last_10'][index] = -1
                    time.sleep(2)
                    continue;
                break;
            
            wins = 0
            for g in black_games:
                if 'winner' in g:
                    winner = g['winner']
                    if (black_id == g['players'][winner]['user']['id']):
                        wins += 1
            games_data_list['black_win_last_10'][index] = wins
            
            
            api.close()
            time.sleep(0.5)
    
        return pd.DataFrame(games_data)