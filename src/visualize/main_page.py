import streamlit as st
from password_check import check_password
from get_data import *

# conda deactivate 服务器上需要
# python -m streamlit run src/visualize/main_page.py --server.port 8502
# nohup python -m streamlit run src/visualize/main_page.py --server.port 8502 > log_streamlit.log &

# streamlit run src/visualize/main_page.py --server.port 8502 会出现import自己的包报错
# 服务器上import configs报错，改成config_examle就好了，怀疑是有重名的包

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

def color_filter(val):
    color = '#99FF99' if val=='YES' else 'transparent'
    return f'background-color: {color}'

st.write('# Data')
df = get_table()
# st.write(df)  # 这两个本身效果一样，下面的可以做css效果
st.dataframe(df.style.applymap(color_filter, subset=['notify_flag', 'latest_flag']))

st.write('# Info Log')
info_log = get_log('info')
st.write(info_log)

st.write('# Error Log')
error_log = get_log('error')
st.write(error_log)