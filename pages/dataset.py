import streamlit as st
import pandas as pd

df = pd.read_csv('processed.csv')
st.dataframe(df)

# CSS for styling the Streamlit app
page_bg_color = """
<style>
[data-testid="stHeader"]{
background-color: #10101C
}

[data-testid="stAppViewContainer"]{
background-color: #10101C
}
</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

st.markdown(
    """
    Hello this is home page!
    """ 
)
