import streamlit as st
import altair as alt
import pandas as pd
from vega_datasets import data

st.set_page_config(layout="wide")

# display title
st.title("Massachusetts Airbnb Listings")
st.write(
    "Let's explore and look at the relationships between neighborhoods, reviews, and prices."
)

# Load and clean data
df = pd.read_csv("listings.csv")
df["price"] = df["price"].replace('[\$,]', '', regex=True).astype(float)

df_viz = df[[
    "neighbourhood_cleansed", "price", "room_type",
    "number_of_reviews", "review_scores_rating"
]].dropna()

# 1. Average Price by Neighborhood
chart1 = alt.Chart(df_viz).mark_bar().encode(
    x=alt.X("neighbourhood_cleansed:N", sort="-y", title="Neighborhoods cleansed"),
    y="mean(price):Q",
    tooltip=["neighbourhood_cleansed", "mean(price):Q"]
).properties(title="Average Airbnb Price by Neighborhood", width=600).configure_axisX(labelAngle=-45)

# 2. Price Distribution by Room Type
chart2 = alt.Chart(df_viz).mark_boxplot(extent='min-max').encode(
    x="room_type:N",
    y=alt.Y("price:Q", scale=alt.Scale(domain=[0, 2000])),
    color="room_type:N"
).properties(title="Price Distribution by Room Type", width=400)

# 3. Review Score vs. Price
chart3 = alt.Chart(df_viz).mark_circle(opacity=0.5).encode(
    x=alt.X("price:Q", scale=alt.Scale(domain=[0, 500])),
    y="review_scores_rating:Q",
    color="room_type:N",
    tooltip=["price", "review_scores_rating"]
).properties(title="Review Score vs. Price", width=500).interactive()

st.altair_chart(chart1, use_container_width=True)
st.altair_chart(chart2, use_container_width=True)
st.altair_chart(chart3, use_container_width=True)


# Apply filters and sidebar 
st.sidebar.header("Filters")
neighborhoods = ['All'] + sorted(df['neighbourhood_cleansed'].unique())
neighborhood = st.sidebar.selectbox("Neighborhood", neighborhoods)
price_range = st.sidebar.slider("Price Range", int(df['price'].min()), int(df['price'].max()), (5000, 100000))
room_types = st.sidebar.multiselect("Room Type(s)", options=df['room_type'].unique(), default=list(df['room_type'].unique()))
score_range = st.sidebar.slider("Review Score Range", 1.0, 5.0, (3.0, 5.0), step=0.1)

df_filtered = df[
    (df['room_type'].isin(room_types)) &
    (df['price'] >= price_range[0]) & (df['price'] <= price_range[1]) &
    (df['review_scores_rating'] >= score_range[0]) & (df['review_scores_rating'] <= score_range[1])
]
if neighborhood != 'All':
    df_filtered = df_filtered[df_filtered['neighbourhood_cleansed'] == neighborhood]

