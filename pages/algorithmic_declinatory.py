import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pickle
import os

@st.cache_data
def load_pickle(file_path):
    if os.path.exists(file_path):
        with open(file_path, "rb") as f:
            return pickle.load(f)
    else:
        st.error(f"File not found: {file_path}")
        return None
    
def hyperbolic_decline(t, qi, di, b):
    return qi / (1 + b * di * t) ** (1/b)

df = pd.read_parquet('files/prod_oil_field_todecline')
decline_df = load_pickle("files/decline_df")
np_dec_comparison = pd.read_parquet('files/np_dec_comparison')

st.header("Algorithmic Declinarory")
st.write("_____________________")

well = st.selectbox(label="Select Well", options=np.sort(df.identificador.unique()))

df_well = df[df.identificador == well]
dec_periods = decline_df[decline_df.identificador==well].decline_periods.tolist()
dec_params = decline_df[decline_df.identificador==well][["qi","di","b"]].values

fig = make_subplots(rows=6, cols=1, subplot_titles=["Oil Rate", "Liquid Rate", "Declinatory Summary"], 
                    vertical_spacing=0.1, 
                    shared_xaxes=True, 
                    specs=[[{"rowspan": 4, "secondary_y": True}], 
                           [None],
                           [None],
                           [None],
                           [{"rowspan": 2, "secondary_y": True}], 
                           [None]])

fig.add_trace(go.Scatter(x=df_well.fecha, y=df_well["qo_[m3/dc]"], name="Qo [m3/dc]", mode="lines", line=dict(color="green")), 
              row=1, col=1, secondary_y=False)
fig.add_trace(go.Scatter(x=df_well.fecha, y=df_well["ql_[m3/dc]"], name="Ql [m3/dc]", mode="lines", line=dict(color="black")), 
              row=5, col=1, secondary_y=False)
fig.add_trace(go.Scatter(x=df_well.fecha, y=df_well["ql_pct_change_cum"], mode="lines", name="Ql pct_change_cum", line=dict(color="magenta", dash="dot", width=3)),
              row=5, col=1, secondary_y=True)

fig.add_trace(go.Scatter(x=df_well[df_well.estado==1].fecha, y=df_well[df_well.estado==1]["estado"], mode="markers", 
                         name="Estados",
                         text=df_well[df_well.estado==1].apply(lambda row: f"{row['capa_estado']}<br>{row['fecha'].strftime('%m-%Y')}", axis=1),
                         hoverinfo='text', marker=dict(color="brown")), 
              row=1, col=1, secondary_y=True)

fig.add_trace(go.Scatter(x=df_well[df_well.estimulacion.isnull()==False].fecha, y=df_well[df_well.estimulacion.isnull()==False]["estimulacion"], mode="markers", 
                         name="Estimulaciones",
                         text=df_well[df_well.estimulacion.isnull()==False].apply(lambda row: f"{row['capa_estim']}<br>{row['fecha'].strftime('%m-%Y')}", axis=1),
                         hoverinfo='text', marker=dict(color="salmon")), 
              row=1, col=1, secondary_y=True)
fig.add_trace(go.Scatter(x=df_well[df_well.inyeccion_start==1].fecha, y=df_well[df_well.inyeccion_start==1]["inyeccion"], mode="markers", 
                         name="Inyeccion",
                         text=df_well[df_well.inyeccion_start==1].apply(lambda row: f"{row['inyector']}<br>{row['fecha'].strftime('%m-%Y')}", axis=1),
                         hoverinfo='text', marker=dict(color="blue")), 
              row=1, col=1, secondary_y=True)
fig.add_trace(go.Scatter(x=df_well[df_well.inyeccion_capa.isnull()==False].fecha, y=df_well[df_well.inyeccion_capa.isnull()==False]["inyeccion_capa"], mode="markers", 
                         name="Inyeccion x Capa",
                         text=df_well[df_well.inyeccion_capa.isnull()==False].apply(lambda row: f"{row['inyector']}<br>{row['capa_iny']}<br>{row['fecha'].strftime('%m-%Y')}", axis=1),
                         hoverinfo='text', marker=dict(color="blue", size=1.5), opacity=0.5), 
              row=1, col=1, secondary_y=True)

for i, ((start_evento_date, end_history_date, qmax_start_date, end_evento, t), (qi, di, b)) in enumerate(zip(dec_periods, dec_params)):
    q = hyperbolic_decline(t, qi, di, b)
    decline_dates = qmax_start_date + pd.to_timedelta(t, unit='D')
    fig.add_trace(go.Scatter(x=decline_dates, y=q, 
                             mode='lines', line=dict(color='orange', dash='dot'),
                             name=f'Declinación {qmax_start_date.date()}'), 
                  row=1, col=1, secondary_y=False)

fig.update_yaxes(title="Oil Rate [m3/dc]", row=1, col=1, secondary_y=False)
fig.update_yaxes(title="Estados", row=1, col=1, secondary_y=True, showgrid=False)
fig.update_yaxes(title="Liquid Rate [m3/dc]", row=5, col=1, secondary_y=False)
fig.update_yaxes(title="pct_change", row=5, col=1, secondary_y=True, showgrid=False)
fig.update_xaxes(title="Date", row=5, col=1)
fig.update_layout(title={"text":f"Production - Well {well}", 'x':0.5, 'xanchor':'center', 'font':{'size':24}},
                  height=700,
                  width=1500,
                  showlegend=True,
                  legend=dict(x=1, y=0.5, xanchor='left', yanchor='middle', orientation='v'))

table = decline_df[decline_df.identificador==well][['tramo', 'identificador', 'evento', 'fecha_evento', 
                                                    'capa_estado', 'capa_estimulacion', 'capa_inyeccion', 
                                                    'qi', 'di', 'b', 
                                                    'NpH', 'NpFC', 'NpEvent']]

st.plotly_chart(fig)
st.dataframe(table, hide_index=True, use_container_width=True)

st.write("_____________________")

left, mid, right = st.columns(3, vertical_alignment="bottom")

np_df = np_dec_comparison[np_dec_comparison['identificador'] == well]
fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=np_df['identificador'],
    y=np_df['np_[mm3]'],
    name='np_[mm3]',
    orientation='v',
    marker=dict(color='green')))
fig2.add_trace(go.Bar(
    x=np_df['identificador'],
    y=np_df['NpH'],
    name='NpH',
    orientation='v',
    marker=dict(color='salmon')))
fig2.add_trace(go.Bar(
    x=np_df['identificador'],
    y=np_df['NpFC'],
    name='NpFC',
    orientation='v',
    marker=dict(color='lightblue')))
fig2.update_layout(
    barmode='group', 
    # height=600,
    # title='Comparación de Np Real Yacimiento y NpH estimado por declinatoria',
    yaxis_title='Valor',
    xaxis_title='Identificador',
    template='plotly_white',
    bargap=.4, 
    margin=dict(l=0, r=0, t=1, b=150),
    legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.001,
            xanchor="center",
            x=0.5,
            font=dict(
                size=12,
                color="black"
            )
        ),
)
mid.plotly_chart(fig2, use_container_width=True)
