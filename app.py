import streamlit as st
from st_screen_stats import WindowQueryHelper
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# Config to make the overall web body wider
st.set_page_config(layout="wide")

# This will be the variable that get into condition checking
helper_screen_stats = WindowQueryHelper()
is_screen_large = helper_screen_stats.minimum_window_size(
    min_width=1000,
    key="window_size_check",
)

df = pd.read_csv("processed.csv")
sorted_df = df.sort_values(by=["subjectivity", "polarity", "sentiment"])

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

# Scatter plot using Matplotlib
plotFig = px.scatter_matrix(
    df, dimensions=["subjectivity", "polarity"], color="sentiment"
)

# Pie chart using Matplotlib
pieFig = px.pie(
    df,
    names="sentiment",
    title="Sentiment Distribution",
)

# Line plot using Matplotlib
lineFig = px.line(
    sorted_df,
    x="subjectivity",
    y="polarity",
    color="sentiment",
    title="Polarity over time",
)

# Correlation matrix using heatmap with plotly
corr_matrix = df[["polarity", "subjectivity"]].corr()
heatmap = ff.create_annotated_heatmap(
    z=corr_matrix.values,
    x=list(corr_matrix.columns),
    y=list(corr_matrix.index),
    colorscale="Viridis",
)

# Word Cloud
positive_text = " ".join(df[df["sentiment"] == "positive"]["clean_text"])
wordcloud = WordCloud(width=1600, height=800).generate(positive_text)
fig, ax = plt.subplots()
ax.imshow(wordcloud, interpolation="bilinear")
ax.axis("off")
ax.set_title("Word Cloud for Positive Sentiments")

# Display all the plots
if is_screen_large["status"]:
    with st.container():
        # First row
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Scatter Plot")
            st.plotly_chart(plotFig)  # Scatter plot
        with col2:
            st.subheader("Line Plot")
            st.plotly_chart(lineFig)  # Line Plot
        # Second row
        col3, col4 = st.columns(2)
        with col3:
            st.subheader("Pie Chart")
            st.plotly_chart(pieFig)  # Pie chart
        with col4:
            st.subheader("Heatmap")
            st.plotly_chart(heatmap)  # Heatmap
else:
    st.subheader("Scatter Plot")
    st.plotly_chart(plotFig)
    st.subheader("Line Plot")
    st.plotly_chart(lineFig)
    st.subheader("Pie Chart")
    st.plotly_chart(pieFig)
    st.subheader("Heatmap")
    st.plotly_chart(heatmap)

# Display Word Cloud
st.pyplot(fig)
