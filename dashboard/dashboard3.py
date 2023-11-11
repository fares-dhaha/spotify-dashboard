import panel as pn
import hvplot.pandas
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holoviews as hv
import plotly.express as px
import plotly.figure_factory as ff
import pickle
import plotly.graph_objects as go
import os
from graphs.plots import *

go.layout.Template().layout.paper_bgcolor = "#f7f7f7"




results_path = "../model/Results"

precision_recall_df = pd.read_csv(os.path.join(results_path,"precision_recall.csv"))
precision_recall = pn.pane.Plotly(precision_recall_curve(precision_recall_df["precision"],precision_recall_df["recall"]))

roc_df = pd.read_csv(os.path.join(results_path,"tpr_fpr.csv"))
roc = pn.pane.Plotly(roc_curve(roc_df.tpr,roc_df.fpr,roc_df.roc_auc[0]))

# Load the object from the pickle file
with open(os.path.join(results_path,'confusion_train.pkl'), 'rb') as f:
    confusion_train = pickle.load(f)

with open(os.path.join(results_path,'confusion_test.pkl'), 'rb') as f:
    confusion_test = pickle.load(f)




classification_report_train = pn.widgets.Tabulator(pd.read_csv(os.path.join(results_path,"classification_report_train.csv"),index_col=0).T.loc[:,["Sad","Happy"]],width=600,layout='fit_columns')
classification_report_test = pn.widgets.Tabulator(pd.read_csv(os.path.join(results_path,"classification_report_test.csv"),index_col=0).T.loc[:,["Sad","Happy"]],width=600,layout='fit_columns')
features_importance = pd.read_csv(os.path.join(results_path,"features_importance.csv")).sort_values(by=["feature importance"],ascending=False)

with open('sidebar.html', 'r') as file:
    # Read the content of the file
    sidebar_content = file.read()

template = pn.template.FastGridTemplate(
	title="ML Results",
    sidebar=[pn.pane.HTML(sidebar_content)],
    accent_base_color="88d8b0", header_background="#1DB954", prevent_collision=True

)
template.main[:3,:] = pn.Tabs(("Confusion Matrix - Train",pn.pane.Plotly(display_confusion_matrix(confusion_train,["Sad","Happy"], "Confusion Matrix Train"))),("Classification Report - Train",pn.Column(classification_report_train)))
template.main[3:6,:] = pn.Tabs(("Confusion Matrix - Test",pn.pane.Plotly(display_confusion_matrix(confusion_test,["Sad","Happy"], "Confusion Matrix Test"))),("Classification Report - Test",pn.Column(classification_report_test)))
template.main[6:9,:] = pn.Tabs(("Precision Recall Curve",precision_recall),("ROC Curve",roc))
template.main[9:12,:] = pn.pane.Plotly(display_features_importance(features_importance))


template.servable()
