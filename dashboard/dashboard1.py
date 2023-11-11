"""
    Exploring dataset Dashboard
"""


import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holoviews as hv
import plotly.express as px
import plotly.figure_factory as ff
from graphs.plots import *


pn.extension(sizing_mode="stretch_width")
pn.extension('plotly','tabulator')
## reading data
data=pd.read_csv("../model/spotify.csv")
data.drop(columns=[data.columns[0]],inplace=True)
data.album_name = data.album_name.str.replace(r':[^)]*|\([^)]*\)','',regex=True).str.strip()
df = data
df.artists = df.artists.str.split(";")
df = df.explode("artists")
most_popular_artists = df.groupby("artists").popularity.mean().to_frame().reset_index().sort_values(by=["popularity"],ascending=False)
top_genres = data.groupby("track_genre").popularity.mean().to_frame().reset_index().sort_values(by=["popularity"],ascending=False).iloc[:10]





tabulator = pn.widgets.Tabulator(data,widths=100, pagination="remote", page_size=5,
                                configuration={
    'clipboard': True, 'rowHeight':55
})
dataset_viewer = pn.Column(tabulator, sizing_mode='stretch_width',width_policy='max')



top_genres_hist = pn.Column(pn.pane.Plotly(top_histogram(dataset=top_genres)))





genre_selector = pn.widgets.Select(name="genre", value="All", options=["All"]+list(data.track_genre.unique()))
most_popular_artist_per_genre = pn.Column(genre_selector, pn.pane.Plotly(pn.bind(top_artists_per_genre,dataset=df,genre=genre_selector)))



genre = pn.widgets.Select(name="genre", value="All", options=["All"]+list(data.track_genre.unique()))


top_artists_pie = pn.Column(genre, pn.pane.Plotly(pn.bind(create_pie,dataset=df,genre=genre)))



template = pn.template.FastGridTemplate(
	title="Explore Dataset",
    sidebar=[pn.pane.HTML("""
        <h1>Spotify Dashboard</h1>
        <h2>Explore more:</h2>
        <ul>
            <h3><li><a href='http://localhost:5006/dashboard1'>Explore Dataset</a></li></h3>
            <h3><li><a href='http://localhost:5006/dashboard2'>Statistical Analysis</a></li></h3>
            <h3><li><a href='http://localhost:5006/dashboard3'>Machine Learning</a></li></h3> 
                        
        </ul>
    """)],
    accent_base_color="88d8b0", header_background="#1DB954", prevent_collision=True

)

template.main[:3,:] = pn.Column(pn.pane.Markdown("# Soptify Dataset"),dataset_viewer,sizing_mode="stretch_width")
template.main[3:6,:5] = pn.Tabs(("Artists with most songs per genre",pn.Column(top_artists_pie)), ("Most popular artists per genre",most_popular_artist_per_genre),sizing_mode="stretch_width")
template.main[3:6,7:] = pn.Column(pn.pane.Markdown("## Most popular genres"),top_genres_hist,sizing_mode="stretch_width")



template.servable()
