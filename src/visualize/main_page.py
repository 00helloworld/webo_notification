import streamlit as st
from password_check import check_password
from get_data import *


# python -m streamlit run src/visualize/main_page.py --server.port 8502
# streamlit run src/visualize/main_page.py --server.port 8502 会出现import自己的包报错

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
st.markdown(
    r"""
    <style>
    .stDeployButton {
            visibility: hidden;
        }
    </style>
    """, unsafe_allow_html=True
)
hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

if 'key' not in st.session_state:
    st.session_state['rerun_counter'] = 0



if not check_password():
    st.stop()  # Do not continue if check_password is not True.


st.write('# Status!')

if st.button("Refresh Data"):
    st.session_state['rerun_counter'] += 1

st.write('# Data')
df = get_table()
st.write(df)

st.write('# Info Log')
info_log = get_log('info')
st.write(info_log)

st.write('# Error Log')
error_log = get_log('error')
st.write(error_log)