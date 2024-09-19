import streamlit as st

st.set_page_config(
    page_title="Page 1",
    page_icon="📄",
    layout="centered"  # Atur layout menjadi default atau centered
)

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

page_image = """
    <style>
    [data-testid=stImage]{
    display: block;
    text-align: center;
    margin-left: auto;
    margin-right: auto;
    width: 30%;
    }
    </style>
"""
header_style = """
    <style>
    [data-testid=element-container]{
    text-align: center;
    }
    </style>
"""

st.markdown(header_style, unsafe_allow_html=True)
st.markdown(page_bg_color, unsafe_allow_html=True)
st.markdown(page_image, unsafe_allow_html=True)
st.header("Wotaku koi ni wa muzukashii")
st.image("wotakoi-cover.jpg")
st.subheader("Synopsis")
st.markdown("""
26-year-old Momose Narumi is a die-hard yaoi fangirl geek who recently switched jobs, in hopes of being able to present an image of a perfect, beautiful young lady. However, her hopes are crashed when she reunites with her middle school classmate Nifuji Hirotaka, an avid gamer nerd that knows about her secret. Both reconnect over alcohol and Hirotaka promises he will not tell on Narumi's geek secret, commenting on how love is difficult for people like them because others think they're "abnormal" and "weird". Two weeks later, Narumi invites Hirotaka out for drinks again but is unable to finish her work on time, prompting Hirotaka to stay back and help her before they go out. As they drink, Hirotaka asks Narumi out, offering to help her pass her game levels as a benefit. Excited, Narumi accepts.
""")

st.subheader("Data source")
