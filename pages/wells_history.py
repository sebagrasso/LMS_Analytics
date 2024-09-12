import streamlit as st
import streamlit.components.v1 as components


st.header("Wells History Chart")
st.write("_____________________")

plot_file = open('files/3_wells_history_chart.html','r', encoding='utf-8')
plot = plot_file.read()

# st.markdown(plot,unsafe_allow_html=True)
components.html(plot, scrolling=True, 
                width=1500, 
                height=1300
                )