import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holoviews as hv
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go


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


def display_correlation_matrix(matrix):
    fig = px.imshow(matrix)
    fig.update_layout(paper_bgcolor='#f7f7f7')
    return fig

def create_scatter(data,x,y):
    fig= px.scatter(data,x=x,y=y,width=800,height=400)
    fig.update_layout(paper_bgcolor='#f7f7f7')
    return fig

def create_countplot(data,x,color="None"):
    if color == "None":
        fig= px.histogram(data,x=x)
    else:
        fig = px.histogram(data,x=x,color=color)
    fig.update_layout(paper_bgcolor='#f7f7f7')
    return fig


def create_barplot(data, x, color="None"):
    if color == "None":
        bar_data = data[x].value_counts().sort_values(ascending=False).to_frame("count").reset_index()
        bar_data.rename(columns={"index":x},inplace=True)
        fig = px.bar(bar_data, x=x, y="count",  barmode="group")
    else:
        bar_data = data.groupby([x,color]).count().iloc[:,0].to_frame("count").reset_index()
        fig = px.bar(bar_data, x=x, y="count", color=color, barmode="group")
    fig.update_layout(paper_bgcolor='#f7f7f7')
    return fig

def create_histogram(data, col):
    fig= px.histogram(data,x=col)
    fig.update_layout(paper_bgcolor='#f7f7f7')
    return fig


def precision_recall_curve(precision,recall):
    # Create a Plotly figure for the precision-recall curve
    fig = go.Figure()

    # Add the precision-recall curve trace
    fig.add_trace(
        go.Scatter(x=recall, y=precision, mode='lines', name='Precision-Recall Curve')
    )

    # Set axis labels and layout
    fig.update_layout(
        title='Precision-Recall Curve',
        xaxis=dict(title='Recall'),
        yaxis=dict(title='Precision'),
        paper_bgcolor='#f7f7f7',
        showlegend=True
    )
    return fig


def roc_curve(tpr,fpr, roc_auc):

    # Create a Plotly figure for the ROC curve
    fig = go.Figure()

    # Add the ROC curve trace
    fig.add_trace(
        go.Scatter(x=fpr, y=tpr, mode='lines', name=f'ROC Curve (AUC={roc_auc:.2f})')
    )

    # Add a diagonal line representing random guessing
    fig.add_trace(
        go.Scatter(x=[0, 1], y=[0, 1], mode='lines', line=dict(dash='dash'), name='Random')
    )

    # Set axis labels and layout
    fig.update_layout(
        title='Receiver Operating Characteristic (ROC) Curve',
        xaxis=dict(title='False Positive Rate'),
        yaxis=dict(title='True Positive Rate'),
        showlegend=True,
        paper_bgcolor='#f7f7f7'
    )

    # Show the plot
    return fig



def display_confusion_matrix(matrix, class_labels, title):
    # Define class labels
    # Create confusion matrix heatmap
    fig = ff.create_annotated_heatmap(z=matrix, x=class_labels, y=class_labels, colorscale='Viridis')

    # Update the layout to add labels and title
    fig.update_layout(
        width=650,height=400,
        title_text=title,
        title_x=0.5,
        title_y=0.1,
        xaxis=dict(title='Predicted label'),
        yaxis=dict(title='True label'),
        plot_bgcolor='lightgrey', # Set the background color of the plot area
        paper_bgcolor='#f7f7f7',  # Set the background color of the entire figure
    )

    return fig

def display_features_importance(features_importance):
    fig = px.bar(features_importance,x="feature",y="feature importance")
    fig.update_layout(
        title='Classifier Features Importance',
        xaxis=dict(title='Feature'),
        yaxis=dict(title='Importance'),
        showlegend=True,
        paper_bgcolor='#f7f7f7'
    )
    return fig