import streamlit as st
import streamlit.components.v1 as components


st.header("Producion Allocation")
st.write("_____________________")

plot_file = open('files/5_1_allocation_vs_total.html','r', encoding='utf-8')
plot = plot_file.read()

components.html(plot, scrolling=True, 
                width=1500, 
                height=1300
                )