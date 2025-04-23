import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

st.title("Susana Ortiz")

df = pd.read_csv("airbnb.csv")

st.sidebar.header("Filters")
neigh_group = st.sidebar.multiselect("Select the neighborhood group", df["neighbourhood_group"].unique())
neigh = st.sidebar.multiselect("Select the neighborhood", df["neighbourhood"].unique())
room_type = st.sidebar.multiselect("Select the type of room", df["room_type"].unique())
price_min, price_max = st.sidebar.slider("Price range:", min_value=int(df["price"].min()), max_value=int(df["price"].clip(upper=1000).max()), value=(int(df["price"].min()), int(df["price"].clip(upper=1000).max())))

df_filtered = df.copy()
df_filtered = df_filtered[ (df_filtered["price"] >= price_min) & (df_filtered["price"] <= price_max)]

if neigh_group:
    df_filtered = df_filtered[df_filtered["neighbourhood_group"].isin(neigh_group)]
if neigh:
    df_filtered = df_filtered[df_filtered["neighbourhood"].isin(neigh)]
if room_type:
    df_filtered = df_filtered[df_filtered["room_type"].isin(room_type)]

tab1, tab2 = st.tabs(["Search results", "Relations"])

with tab1:
    st.subheader("Airbnbs found")
    st.dataframe(df_filtered[["name", "neighbourhood_group", "neighbourhood", "room_type", "price", "reviews_per_month"]].head())

    st.subheader("Map")
    st.map(df_filtered.dropna(subset=["latitude", "longitude"]), latitude="latitude", longitude="longitude")

    st.subheader("Top Hosts")
    top = st.radio("Number of Top Hosts you want to see", [3, 5, 10, 20])
    df_host = df_filtered.groupby(["host_id", "host_name"]).size().reset_index(name="count")
    df_host["host"] = df_host["host_id"].astype(str) + "---" + df_host["host_name"]
    df_top_host = df_host.sort_values(by="count", ascending=False).head(top)
    fig2 = px.bar(df_top_host, x="count", y="host", orientation='h', hover_name="host_name")
    st.plotly_chart(fig2)

with tab2:
    st.subheader("Type of room vs Number of persons")
    fig3 = px.box(df_filtered[df_filtered["price"]<600], x="room_type", y="minimum_nights")
    st.plotly_chart(fig3)

    st.subheader("Price per Room type")
    fig4 = px.box(df_filtered[df_filtered["price"]<600], x="room_type", y="price")
    st.plotly_chart(fig4)

    st.subheader("Top reviews per month")
    df_top_reviews = df_filtered.sort_values(by="reviews_per_month", ascending=False).dropna(subset=["reviews_per_month"]).head(10)
    fig5 = px.bar(df_top_reviews, x="reviews_per_month", y="name", orientation='h', color="neighbourhood")
    st.plotly_chart(fig5)

    st.subheader("Number of reviews per Price")
    fig6 = px.scatter(df_filtered[df_filtered["price"]<600], x="number_of_reviews", y="price", color="room_type", hover_data=["name"])
    st.plotly_chart(fig6)
