import streamlit as st
import streamlit.components.v1 as components


st.header("Controls vs Production")
st.write("_____________________")

plot_file = open('files/4_1_controles_vs_prod_crossplots.html','r', encoding='utf-8')
plot = plot_file.read()

plot_file2 = open('files/4_2_controles_vs_prod_charts.html','r', encoding='utf-8')
plot2 = plot_file2.read()

components.html(plot, 
                width=1500, 
                height=520
                )

components.html(plot2,
                width=1500, 
                height=4000
                )