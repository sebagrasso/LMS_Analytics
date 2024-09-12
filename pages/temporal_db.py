import streamlit as st
import streamlit.components.v1 as components


st.header("Temporal Data Analytics")
st.write("_____________________")


plot_file = open('files/8_1_temporal_df.html','r', encoding='utf-8')
plot = plot_file.read()

# st.markdown(plot,unsafe_allow_html=True)
components.html(plot, scrolling=True, 
                width=1500, 
                height=1300
                )