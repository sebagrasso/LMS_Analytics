import streamlit as st
import streamlit.components.v1 as components


st.header("Controls vs Production Timeseries")
st.write("_____________________")

plot_file = open('files/4_2_controles_vs_prod_charts.html','r', encoding='utf-8')
plot = plot_file.read()

# st.markdown(plot,unsafe_allow_html=True)
components.html(plot,
                width=1500, 
                height=4000
                )