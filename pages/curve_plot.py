import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import random
import math

# @st.cache_data
wells_df_global_logs_rmn_filt = pd.read_parquet('files/wells_df_global_logs_rmn_filt')

st.header("Global Well logs plot")
st.write("_____________________")


def generate_color_list(logs, seed, alpha=1):
    random.seed(seed)  # Set seed for reproducibility
    colors = []
    for _ in logs:
        r = lambda: random.randint(0, 255)
        color = f'rgba({r()},{r()},{r()},{alpha})'
        colors.append(color)
    return colors

def plot_well_logs(df, well_name, list_logs, colors):
    df = df[df['identificador'] == well_name].reset_index(drop=True).set_index("depth")
    nrows = 1
    ncols = math.ceil(len(list_logs) / nrows)
    subplot_titles = [log for log in list_logs]
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=subplot_titles, shared_yaxes=True)
    if "capa" in list_logs:
        unique_capas = df['capa'].unique()
        capa_colors = generate_color_list(unique_capas, seed=42, alpha=1)
        capa_color_map = dict(zip(unique_capas, capa_colors))
        for capa in unique_capas:
            mask = df['capa'] == capa
            if capa == "-":
                pass
            else:
                fig.add_trace(go.Scatter(
                    x=[0] * sum(mask),
                    y=df[mask].index,
                    mode='markers',
                    marker=dict(color=capa_color_map[capa], symbol='square', size=30),
                    name=capa,
                    text=df[mask].reset_index().apply(lambda row: f"Capa: {row['capa']}<br>Depth: {row['depth']}", axis=1),
                    hoverinfo="text",
                    showlegend=False
                ), row=1, col=1)
                
                y_mean = df[mask].index.values.mean()
                fig.add_trace(go.Scatter(
                    x=[0],
                    y=[y_mean],
                    mode='markers+text',
                    marker=dict(color=capa_color_map[capa], symbol='square', size=10),
                    text=[capa],
                    textposition='middle center',
                    textfont=dict(color='white', family='Arial', size=10),
                    name=capa,
                    hoverinfo="text",
                    showlegend=False
                ), row=1, col=1)
        fig.update_xaxes(title_text='', showgrid=False, showticklabels=False, zeroline=False, range=[-0.5, 0.5], row=1, col=1)
        
    for i, log in enumerate([c for c in list_logs if c!="capa"]):
        row = (i // ncols) + 1
        col = (i+1 % ncols) + 1
        fig.add_trace(go.Scatter(x=df[log], y=df.index, name=log), row=row, col=col)
        if "perm" in log:
            fig.update_xaxes(title_text=log, type="log", row=row, col=col)
        else:
            fig.update_xaxes(title_text=log, row=row, col=col)

    fig.update_yaxes(title_text = "DEPTH", autorange="reversed", row=1, col=1)
    fig.update_layout(title_text=well_name, title_font = dict(size=30), height=1000, showlegend=True)
    return fig

logs=['capa', 'lithology_', 'res_deep:1', 'res_shallow:1', 'sped', 'vcl', 'phie', 'sw', 'dmrperm', 'edmperm']
colors = generate_color_list(logs, seed=10, alpha=0.8)
well_options = wells_df_global_logs_rmn_filt.identificador.unique()
# well_options = wells_df_global_logs_rmn_filt[["identificador", "dmrperm", "edmperm"]].dropna(subset=["dmrperm", "edmperm"]).identificador.unique()
identificador = st.selectbox(label="Select Well", options=well_options)

fig = plot_well_logs(wells_df_global_logs_rmn_filt.dropna(subset=logs, how="all"), identificador, logs, colors)
st.plotly_chart(fig, use_container_width=True)

st.write("_____________________")
def plot_logs_dists(df, list_logs):
    nrows=1
    ncols = math.ceil(len(list_logs) / nrows)
    if "capa" in logs:
        subplot_titles =  ["top capas"] + [log for log in logs if log != "capa"]
    else:
        subplot_titles =  [log for log in logs]
    fig = make_subplots(rows=nrows, cols=ncols, subplot_titles=subplot_titles, horizontal_spacing=0.02)

    for i, log in enumerate(logs):
        row = (i // ncols) + 1
        col = (i % ncols) + 1
        if log == "capa":
            df_capa = df[df.capa!="-"].loc[:,log].value_counts().reset_index().sort_values(by="count").iloc[-20:]
            fig.add_trace(go.Bar(x=df_capa["count"], y=df_capa.capa, orientation="h", opacity=0.8, name=log), row=row, col=col)
        else:
            # fig.add_trace(go.Histogram(x=df.loc[:,log].dropna(), nbinsx=50, opacity=0.6, name=log), row=row, col=col)
            fig.add_trace(go.Box(y=df.loc[:,log].dropna(), opacity=0.6, name=log), row=row, col=col)
            fig.update_xaxes(title_text=log, row=row, col=col)

    fig.update_layout(
                    # title_text="Logs distributions", title_font = dict(size=30), 
                    height=400,
                    margin=dict(l=0, r=0, t=20, b=10),
                    showlegend=True)
    return fig


fig2 = plot_logs_dists(wells_df_global_logs_rmn_filt[wells_df_global_logs_rmn_filt.identificador==identificador], logs)
st.plotly_chart(fig2, use_container_width=True)

st.subheader("Logs Distributions")
st.write("_____________________")