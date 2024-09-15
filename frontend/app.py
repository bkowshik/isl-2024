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
    parent_dir = os.path.abspath(os.path.join(script_dir, os.pardir))
    log_dir = os.path.join(parent_dir, 'logs')
    data_dir = os.path.join(parent_dir, 'data/clean') # Shiny app will use cleaned datasets.

    @render.data_frame
    def matches_df():

        df = pd.read_csv(os.path.join(data_dir, 'matches.csv'), parse_dates=["start_at", "end_at"])
        df['date'] = df['start_at'].dt.strftime("%Y-%m-%d")
        df['start_time'] = df['start_at'].dt.strftime("%I:%M %p")
        df['end_time'] = df['end_at'].dt.strftime("%I:%M %p")

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
