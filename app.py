import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

# Título con tu nombre
st.title("Susana Ortiz")

df = pd.read_csv("airbnb.csv")

# Barra lateral de filtros
st.sidebar.header("Filtros")
neigh_group = st.sidebar.multiselect("Selecciona un grupo de vecindario", df["neighbourhood_group"].unique())
neigh = st.sidebar.multiselect("Selecciona vecindarios", df["neighbourhood"].unique())
room_type = st.sidebar.multiselect("Selecciona tipo de habitación", df["room_type"].unique())

df_filtered = df.copy()
if neigh_group:
    df_filtered = df_filtered[df_filtered["neighbourhood_group"].isin(neigh_group)]
if neigh:
    df_filtered = df_filtered[df_filtered["neighbourhood"].isin(neigh)]
if room_type:
    df_filtered = df_filtered[df_filtered["room_type"].isin(room_type)]

# Tabs
tab1, tab2 = st.tabs(["Exploración", "Relaciones"])

with tab1:
    st.subheader("Datos Básicos")
    st.dataframe(df_filtered[["name", "neighbourhood_group", "neighbourhood", "room_type", "price", "reviews_per_month"]].head())

    st.subheader("Mapa")
    st.map(df_filtered.dropna(subset=["latitude", "longitude"]), latitude="latitude", longitude="longitude")

    st.subheader("Boxplot por Neighbourhood Group")
    fig1 = px.box(df_filtered[df_filtered["price"]<600], x="neighbourhood_group", y="price")
    st.plotly_chart(fig1)

    st.subheader("Top Hosts")
    top = st.radio("¿Cuántos top hosts quieres ver?", [3, 5, 10, 20])
    df_host = df_filtered.groupby(["host_id", "host_name"]).size().reset_index(name="count")
    df_host["host"] = df_host["host_id"].astype(str) + "---" + df_host["host_name"]
    df_top_host = df_host.sort_values(by="count", ascending=False).head(top)
    fig2 = px.bar(df_top_host, x="count", y="host", orientation='h', hover_name="host_name")
    st.plotly_chart(fig2)

with tab2:
    st.subheader("Relación: Tipo de habitación vs Número de personas")
    fig3 = px.box(df_filtered[df_filtered["price"]<600], x="room_type", y="minimum_nights")
    st.plotly_chart(fig3)

    st.subheader("Precio por tipo de habitación")
    fig4 = px.box(df_filtered[df_filtered["price"]<600], x="room_type", y="price")
    st.plotly_chart(fig4)

    st.subheader("Top reviews por mes")
    df_top_reviews = df_filtered.sort_values(by="reviews_per_month", ascending=False).dropna(subset=["reviews_per_month"]).head(10)
    fig5 = px.bar(df_top_reviews, x="reviews_per_month", y="name", orientation='h', color="neighbourhood")
    st.plotly_chart(fig5)

    st.subheader("Relación: Número de reviews vs Precio")
    fig6 = px.scatter(df_filtered[df_filtered["price"]<600], x="number_of_reviews", y="price", color="room_type", hover_data=["name"])
    st.plotly_chart(fig6)
