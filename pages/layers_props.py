import streamlit as st
import streamlit.components.v1 as components


st.header("Layers Properties")
st.write("_____________________")

plot_file = open('files/5_2_layers_properties.html','r', encoding='utf-8')
plot = plot_file.read()

components.html(plot, scrolling=True, 
                width=1500, 
                height=1300
                )