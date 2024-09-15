import datetime
import os
import json
from shiny import App, render, ui
import pandas as pd

app_ui = ui.page_fluid(
    ui.page_navbar(
        ui.nav_panel(
            "Home",
            ui.input_date_range("daterange", "", start="2024-09-13", end = datetime.date.today(), separator="-", min = "2024-09-13", max = "2024-12-31"),
            ui.output_data_frame("matches_df"),
        ),
        title="⚽️ Indian Super League, 2024",
        id="page",
        bg="#F5F5F5",
    ),
)

def server(input, output, session):

    @render.text
    def value():
        return f"{input.daterange()[0]} to {input.daterange()[1]}"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(script_dir)
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    log_dir = os.path.join(parent_dir, 'logs')
    data_dir = os.path.join(parent_dir, 'data')

    @render.data_frame
    def matches_df():

        with open(os.path.join(data_dir, 'matches.txt'), encoding='utf-8') as f:
            matches = json.loads(f.readlines()[-1])['matches']

        df = []
        for match in matches:
            df.append({
                'start_at': match['start_date'],
                'end_at': match['end_date'],
                'home_team': match['participants'][0]['name'],
                'away_team': match['participants'][1]['name'],
                'score': match['winning_margin'],
            })
        df = pd.DataFrame(df)
        df['date'] = pd.to_datetime(df['start_at']).dt.strftime("%Y-%m-%d")
        df['start_at'] = pd.to_datetime(df['start_at'])
        df['end_at'] = pd.to_datetime(df['start_at'])
        df['start_time'] = pd.to_datetime(df['start_at']).dt.strftime("%H:%M")
        df['end_time'] = pd.to_datetime(df['end_at']).dt.strftime("%H:%M")
        df['match_id'] = df.index + 1
        print(df.head())

        df_render = df.sort_values(by="start_at", ascending=False) \
            .loc[(df['date'] >= str(input.daterange()[0])) & (df['date'] <= str(input.daterange()[1])),
                ["match_id", "date", "start_time", "end_time", "home_team", "away_team", "score"]] \
            .rename(columns={
                "match_id": "Match No.",
                "date": "Date",
                "start_time": "Start",
                "end_time": "End",
                "home_team": "Home Team",
                "away_team": "Away Team",
                "score": "Score"
            })
        return render.DataGrid(
            df_render,
            width="100%"
        )

app = App(app_ui, server)