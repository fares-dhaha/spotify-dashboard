import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holoviews as hv
import plotly.express as px
import plotly.figure_factory as ff


def top_histogram(dataset):
    fig= px.bar(dataset,x="track_genre",y="popularity")
    fig.update_layout(paper_bgcolor='#f7f7f7')
    return fig

def create_pie(dataset,genre):
    if genre == "All":
        pie_data = dataset.artists.value_counts().sort_values(ascending=False).to_frame("number of songs").reset_index().iloc[:10]
    else:
        pie_data = dataset.loc[dataset.track_genre==genre,"artists"].value_counts().sort_values(ascending=False).to_frame("number of songs").reset_index().iloc[:10]
    pie_data = pie_data.rename(columns={"index":"artist"})
    fig = px.pie(pie_data,values="number of songs",names="artist",hole=0.3,width=500, height=400)
    fig.update_layout(paper_bgcolor='#f7f7f7')
    return fig

def top_artists_per_genre(dataset,genre):
    if genre=="All":
        d = dataset.groupby("artists").popularity.mean().to_frame().reset_index().sort_values(by=["popularity"],ascending=False).iloc[:10]
    else:
        d = dataset.loc[dataset.track_genre==genre,:].groupby("artists").popularity.mean().to_frame().reset_index().sort_values(by=["popularity"],ascending=False).iloc[:10]
    d = d.rename(columns={"index":"artist"})
    fig= px.bar(d,x="artists",y="popularity")
    fig.update_layout(paper_bgcolor='#f7f7f7')
    return fig
