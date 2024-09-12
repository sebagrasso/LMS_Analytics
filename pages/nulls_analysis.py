import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

st.header("Log null analysis")
st.write("_____________________")

path = 'files/2_1_logs_null_analysis.png'
image = mpimg.imread(path)
st.image(image, use_column_width=True)