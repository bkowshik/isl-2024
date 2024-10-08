# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_utils.ipynb.

# %% auto 0
__all__ = ['parent_dir', 'log_dir', 'data_dir', 'get_live_matches']

# %% ../nbs/00_utils.ipynb 2
import warnings
warnings.filterwarnings('ignore')

import json
import os
import requests
import datetime
import pytz

import pandas as pd

# %% ../nbs/00_utils.ipynb 4
try:
    # This will work when running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # This will work when running in a Jupyter notebook
    script_dir = os.getcwd()

parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
log_dir = os.path.join(parent_dir, 'logs')
data_dir = os.path.join(parent_dir, 'data')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# %% ../nbs/00_utils.ipynb 6
def get_live_matches(now = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))):
    with open(os.path.join(data_dir, 'matches.txt'), 'r') as f:
        logs = f.readlines()

    latest = logs[-1]
    matches = json.loads(latest)['matches']

    matches_df = []
    for match in matches:
        matches_df.append({
            'start_at': match['start_date'],
            'end_at': match['end_date'],
            'game_id': match['game_id'],
        })

    matches_df = pd.DataFrame(matches_df)
    matches_df['start_at'] = pd.to_datetime(matches_df['start_at'])
    matches_df['end_at'] = pd.to_datetime(matches_df['end_at'])

    live_matches = matches_df[
        (now >= matches_df["start_at"] - datetime.timedelta(minutes = 15)) &
        (now <= matches_df["end_at"] + datetime.timedelta(minutes = 30))
    ]
    game_ids = list(live_matches['game_id'].values)
    return(game_ids)
