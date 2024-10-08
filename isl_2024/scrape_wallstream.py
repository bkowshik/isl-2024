"""Match commentary."""

# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/03_scrape_wallstream.ipynb.

# %% auto 0
__all__ = ['parent_dir', 'log_dir', 'data_dir', 'match_ids', 'fetch_wallstream']

# %% ../nbs/03_scrape_wallstream.ipynb 2
import warnings
warnings.filterwarnings('ignore')

import json
import logging
import os
import requests

# NOTE: Had to install the package with the following command for the import to work.
# python3 -m pip install -e '.[dev]'
from .utils import *

# %% ../nbs/03_scrape_wallstream.ipynb 4
try:
    # This will work when running as a script
    script_dir = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # This will work when running in a Jupyter notebook
    script_dir = os.getcwd()

parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
log_dir = os.path.join(parent_dir, 'logs')
data_dir = os.path.join(parent_dir, 'data/wallstream')

if not os.path.exists(log_dir):
    os.makedirs(log_dir)

if not os.path.exists(data_dir):
    os.makedirs(data_dir)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', filename=os.path.join(log_dir, 'scrape_wallstream.log'), filemode='a')

# %% ../nbs/03_scrape_wallstream.ipynb 6
def fetch_wallstream(match_id):
    url = f"https://www.indiansuperleague.com/functions/wallstream/?sport_id=2&client_id=5KEUfrMT/+2lgecJyh42zA==&match_id={match_id}"
    headers = {
        'accept': '*/*',
        'referer': 'https://www.indiansuperleague.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        logging.info('API request successful. Content length: {}'.format(len(response.content)))
        with open(os.path.join(data_dir, f'{match_id}.txt'), 'a') as f:
            f.write(response.text + "\n")
    else:
        logging.error('API request failed. Status code: {}'.format(response.status_code))

# %% ../nbs/03_scrape_wallstream.ipynb 7
# Fetch IDs of live matches using the matches summary.
match_ids = get_live_matches()
logging.info('Live matches: {} [{}]'.format(len(match_ids), ', '.join(match_ids)))

for match_id in match_ids:
    fetch_wallstream(match_id)
