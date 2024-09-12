import streamlit as st
import streamlit.components.v1 as components


st.header("Submergence vs Liquid")
st.write("_____________________")

plot_file = open('files/4_3_submergence_vs_liquid.html','r', encoding='utf-8')
plot = plot_file.read()

components.html(plot,
                width=1500, 
                height=4000
                )