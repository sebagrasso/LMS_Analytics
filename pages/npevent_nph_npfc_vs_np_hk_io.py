import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats
import os

# @st.cache_data
h_punzado_tramo_id = pd.read_parquet('files/h_punzado_tramo_id')
np_dec_comparison = pd.read_parquet('files/np_dec_comparison')

st.header("Np-EUR Estimation vs Reservoir Properties")
st.write("_____________________")

def create_plot(identificador, capa, evento, start_year, end_year, estimacion_np, xaxes_feature, log, trendline):
    filtered_data = h_punzado_tramo_id.copy()
    if identificador != ["all"]:
        filtered_data = filtered_data[filtered_data['identificador'].isin(identificador)]
    if capa != ["all"]:
        filtered_data = filtered_data[filtered_data['capa'].apply(lambda x: any(c in x for c in capa))]
    if evento != ["all"]:
        filtered_data = filtered_data[filtered_data['evento'].isin(evento)]
    
    filtered_data = filtered_data[(filtered_data['year'] >= start_year) & (filtered_data['year'] <= end_year)]
    fig = make_subplots(rows=1, cols=2, horizontal_spacing=0.08, subplot_titles=["Np real vs NpH (Dec)", f"Espesor Punzado vs {estimacion_np} (Dec)"])
    
    max_val = max(np_dec_comparison['np_[mm3]'].max(), np_dec_comparison['NpH'].max())
    x_line = np.linspace(0, max_val, 10)
    y_line_plus_15,  y_line_minus_15 = x_line * 1.15, x_line * 0.85
    
    fig.add_trace(go.Scatter(x=x_line, y=y_line_plus_15, mode='lines', name='+15%', line=dict(color='orange', dash='dash'), opacity=0.2, showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_line, y=y_line_minus_15, mode='lines', name='-15%', line=dict(color='orange', dash='dash'), opacity=0.2, showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=x_line, y=x_line, mode='lines', name='Igualdad', line=dict(color='gray', dash='dot'), opacity=0.2, showlegend=False), row=1, col=1)
    
    xplot_npevent = go.Scatter(x=filtered_data[xaxes_feature], y=filtered_data[estimacion_np], name='NpEvent_hk', mode="markers", 
                                marker=dict(color=filtered_data["year"], colorscale="viridis", colorbar=dict(title="Año")),
                                text=filtered_data.apply(lambda row: f"Well: {row['identificador']}<br>Year: {row['year']}<br>{xaxes_feature}: {int(row[xaxes_feature])}<br>{estimacion_np}: {int(row[estimacion_np])}<br>NCapas: {row['n_capas']}<br>Capas: {row['capa']}", axis=1),
                                hoverinfo='text', showlegend=False)
    fig.add_trace(xplot_npevent, row=1, col=2)

    # xplot_nph = go.Scatter(x=np_dec_comparison['np_[mm3]'], y=np_dec_comparison['NpH'], name='NpH_np', mode="markers", 
    #                         marker=dict(color="darkgreen"),
    #                         text=np_dec_comparison.apply(lambda row: f"Well: {row['identificador']}<br>Np: {int(row['np_[mm3]'])}<br>NpH: {int(row['NpH'])}", axis=1),
    #                         hoverinfo='text', showlegend=False)
    # fig.add_trace(xplot_nph, row=1, col=1)

    highlighted_data = np_dec_comparison.copy()
    non_highlighted_data = pd.DataFrame()
    
    if identificador != ["all"]:
        highlighted_data = np_dec_comparison[np_dec_comparison['identificador'].isin(identificador)]
        non_highlighted_data = np_dec_comparison[~np_dec_comparison['identificador'].isin(identificador)]
    
    if not non_highlighted_data.empty:
        fig.add_trace(go.Scatter(
            x=non_highlighted_data['np_[mm3]'],
            y=non_highlighted_data['NpH'],
            name='NpH_np',
            mode="markers",
            marker=dict(color="darkgreen", size=8),
            text=non_highlighted_data.apply(lambda row: f"Well: {row['identificador']}<br>Np: {int(row['np_[mm3]'])}<br>NpH: {int(row['NpH'])}", axis=1),
            hoverinfo='text',
            showlegend=False
        ), row=1, col=1)
    
    if not highlighted_data.empty:
        fig.add_trace(go.Scatter(
            x=highlighted_data['np_[mm3]'],
            y=highlighted_data['NpH'],
            name='NpH_np',
            mode="markers",
            marker=dict(
                color="orange" if identificador != ["all"] else "darkgreen", 
                size=14 if identificador != ["all"] else 8, 
                symbol="star" if identificador != ["all"] else "circle"
            ),
            text=highlighted_data.apply(lambda row: f"Well: {row['identificador']}<br>Np: {int(row['np_[mm3]'])}<br>NpH: {int(row['NpH'])}", axis=1),
            hoverinfo='text',
            showlegend=False
        ), row=1, col=1)

    if trendline:
        try:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x=filtered_data[xaxes_feature], y=filtered_data[estimacion_np])
            trendline_y = slope * filtered_data[xaxes_feature] + intercept
            fig.add_trace(go.Scatter(x=filtered_data[xaxes_feature], y=trendline_y, mode='lines', 
                                     text=f'Trendline (R²={r_value**2:.2f})', hoverinfo='text',
                                     line=dict(color='lightblue', dash='dash'), showlegend=False), row=1, col=2)
        except:
            pass
    maxnp1 = max(np_dec_comparison['np_[mm3]'].max(), np_dec_comparison['NpH'].max())
    fig.update_xaxes(title="Np Real [mm3]", range=[0, maxnp1], row=1, col=1)
    fig.update_yaxes(title="NpH Declinatory Estimation [mm3]", range=[0, maxnp1], row=1, col=1)
    
    fig.update_xaxes(title="Hk [m]", row=1, col=2)
    if log:
        fig.update_yaxes(title=f"{estimacion_np} [mm3]", type="log", row=1, col=2)
    else:
        fig.update_yaxes(title=f"{estimacion_np} [mm3]", row=1, col=2)
    fig.update_layout(height=700, 
                    #   width=1300, 
                      template='plotly_white'
                      )
    return fig

# def main():
# st.title('Data Visualization Dashboard')
identificador_options = ["all"] + sorted(h_punzado_tramo_id['identificador'].unique().tolist())
evento_options = ["all"] + sorted(h_punzado_tramo_id['evento'].unique().tolist())
min_year = int(h_punzado_tramo_id['year'].min())
max_year = int(h_punzado_tramo_id['year'].max())
col1, col2 = st.columns(2)
with col1:
    identificador = st.multiselect('Well:', options=identificador_options, default=["all"])
    capa_options = ["all"] + sorted(list(set(capa.strip() for capas in h_punzado_tramo_id['capa'].unique() for capa in capas.split(','))))
    evento = st.multiselect('Evento:', options=evento_options, default=["all"])
    capa = st.multiselect('Capa:', options=capa_options, default=["all"])
    start_year, end_year = st.slider('Year Range:', min_value=min_year, max_value=max_year, value=(min_year, max_year))
with col2:
    xaxes_feature = st.selectbox('Feature (x):', options=["Hk"], index=0)
    estimacion_np = st.selectbox('Estimador Np (y):', options=["NpEvent", "NpH", "NpFC"], index=0)
    log = st.checkbox('Log y', value = False)
    trendline = st.checkbox('Trendline', value = True)

fig = create_plot(identificador, capa, evento, start_year, end_year, estimacion_np, xaxes_feature, log, trendline)
    
st.plotly_chart(fig, use_container_width=True)

# if __name__ == "__main__":
#     main()

st.write("_____________________")

fig2 = go.Figure()
fig2.add_trace(go.Bar(
    x=np_dec_comparison['identificador'],
    y=np_dec_comparison['np_[mm3]'],
    name='np_[mm3]',
    orientation='v',
    marker=dict(color='green')))
fig2.add_trace(go.Bar(
    x=np_dec_comparison['identificador'],
    y=np_dec_comparison['NpH'],
    name='NpH',
    orientation='v',
    marker=dict(color='salmon')))
fig2.add_trace(go.Bar(
    x=np_dec_comparison['identificador'],
    y=np_dec_comparison['NpFC'],
    name='NpFC',
    orientation='v',
    marker=dict(color='lightblue')))
fig2.update_layout(
    barmode='group', 
    height=600,
    # title='Comparación de Np Real Yacimiento y NpH estimado por declinatoria',
    yaxis_title='Valor',
    xaxis_title='Identificador',
    template='plotly_white',
    bargap=.4, 
    legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.001,
            xanchor="center",
            x=0.5,
            font=dict(
                size=15,
                color="black"
            )
        ),
)
st.plotly_chart(fig2, use_container_width=True)
