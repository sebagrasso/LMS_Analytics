import streamlit as st
import streamlit.components.v1 as components


st.header("Declinatory estimation vs Np")
st.write("_____________________")

plot_file2 = open('files/9_2_np_vs_eur.html','r', encoding='utf-8')
plot2 = plot_file2.read()

plot_file3 = open('files/9_3_Hpunz_eur_prorr.html','r', encoding='utf-8')
plot3 = plot_file3.read()

plot_file4 = open('files/9_4_Hpunz_eur_prorr_capa.html','r', encoding='utf-8')
plot4 = plot_file4.read()

plot_file5 = open('files/9_5_Hpunz_eur_prorr_pozo.html','r', encoding='utf-8')
plot5 = plot_file5.read()


components.html(plot2,
                width=1500, 
                height=650
                )

components.html(plot3,
                width=1500, 
                height=920
                )

components.html(plot4,
                width=1600, 
                height=920
                )

components.html(plot5,
                width=1600, 
                height=920
                )