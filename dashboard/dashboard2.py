import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holoviews as hv
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
from graphs.plots import *

## reading data
data=pd.read_csv("../model/spotify.csv")
data.drop(columns=[data.columns[0]],inplace=True)
data.album_name = data.album_name.str.replace(r':[^)]*|\([^)]*\)','',regex=True).str.strip()
top_genres = data.groupby("track_genre").popularity.mean().to_frame().reset_index().sort_values(by=["popularity"],ascending=False).iloc[:10]
correlation_matrix = data.corr()
categorical_cols = ["sentiment","explicit","key","mode","track_genre"]
pn.extension('plotly','tabulator')

stats = data.describe().T.reset_index()
missing_values = (100 * data.isnull().sum() / data.shape[0]).reset_index(name="missing")
stats = pd.merge(stats, missing_values,how="left",on="index")
stats.rename(columns={"index":"feature"},inplace=True)



content_fn = lambda x: pn.pane.Plotly(create_histogram(data,x["feature"]))

col_width = str(100/(stats.shape[1]))+"%"
tabulator = pn.widgets.Tabulator(stats,widths={k:col_width for k in stats}, pagination="remote", page_size=5,  row_content=content_fn, embed_content=False,
                                configuration={
    'clipboard': True,
    'rowHeight': 50,
})





dataset_viewer = pn.Column(tabulator, sizing_mode='stretch_width',width_policy='max')








def top_artists_per_genre(dataset,genre):
    if genre=="All":
        d = dataset.groupby("artists").popularity.mean().to_frame().reset_index().sort_values(by=["popularity"],ascending=False).iloc[:10]
    else:
        d = dataset.loc[dataset.track_genre==genre,:].groupby("artists").popularity.mean().to_frame().reset_index().sort_values(by=["popularity"],ascending=False).iloc[:10]
    d = d.rename(columns={"index":"artist"})
    return px.bar(d,x="artists",y="popularity")



def create_pie(dataset,genre):
    if genre == "All":
        pie_data = dataset.artists.value_counts().sort_values(ascending=False).to_frame("number of songs").reset_index().iloc[:10]
    else:
        pie_data = dataset.loc[dataset.track_genre==genre,"artists"].value_counts().sort_values(ascending=False).to_frame("number of songs").reset_index().iloc[:10]
    pie_data = pie_data.rename(columns={"index":"artist"})
    fig = px.pie(pie_data,values="number of songs",names="artist",hole=0.3,width=500, height=400)
    return fig




numerical_cols = list(data.select_dtypes(include=[float, int]).columns)


x_scatter = pn.widgets.Select(name="X", value="popularity", options=numerical_cols)
y_scatter = pn.widgets.Select(name="Y", value="popularity", options=numerical_cols,)



scatter_plot = pn.bind(create_scatter,data=data,x=x_scatter,y=y_scatter)




x_count = pn.widgets.Select(name="x", value="popularity", options=numerical_cols)
color_count = pn.widgets.Select(name="color", value="None", options=categorical_cols+["None"])

count_plot = pn.bind(create_countplot,data=data,x=x_count,color=color_count)





x = pn.widgets.Select(name="x",value="sentiment",options=categorical_cols)
color = pn.widgets.Select(name="color",value="None",options=categorical_cols+["None"])
barplot = pn.Column(pn.Row(x,color),pn.pane.Plotly(pn.bind(create_barplot, data=data, x=x, color=color)))

    

with open('sidebar.html', 'r') as file:
    # Read the content of the file
    sidebar_content = file.read()


template = pn.template.FastGridTemplate(
	title="Statistical Analysis",
    sidebar = [pn.pane.HTML(sidebar_content)],
    accent_base_color="88d8b0", header_background="#1DB954", prevent_collision=True
)

template.main[:3,:] = pn.Tabs(("Dataset Statistics",dataset_viewer),("Correlation Matrix",pn.pane.Plotly(display_correlation_matrix(correlation_matrix))))
template.main[3:6,:] = pn.Column(pn.pane.Markdown("# Scatter plot"),pn.Row(x_scatter,y_scatter),scatter_plot)
template.main[6:9,:] = pn.Tabs(("Continuous Variable - Histogram",pn.Column(pn.Row(x_count, color_count), count_plot)), ("Categorical Variable - Barplot",barplot))


template.servable()
