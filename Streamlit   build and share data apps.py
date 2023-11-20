import streamlit as st 
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn import metrics
from scipy.spatial.distance import cdist

#######  Configuration de la page ########

header_left,header_mid,header_right = st.columns([0.5,6,0.5],gap='large')

st.title("🚗 Analyse du dataset des voitures")


#######  Import des données ########
@st.cache_data
def load_df():
    df_cars = pd.read_csv("https://raw.githubusercontent.com/murpi/wilddata/master/quests/cars.csv", sep=",") 
    df_cars["continent"] = df_cars['continent'].apply(lambda x : x.strip())
    df_cars = df_cars.sort_values(by='continent')
    return df_cars
df_cars = load_df()

continents_unique = df_cars["continent"].unique()
continents_with_all = ["All"] + list(continents_unique)


# Widgets dans la barre latérale
with st.sidebar:
    st.title("Options")
    selected_continent = st.sidebar.selectbox("Continent", continents_with_all)


st.markdown("## Heatmap ")

# Filtrer les données en fonction du continent sélectionné
if selected_continent != "All":
    filtered_df = df_cars[df_cars['continent'] == selected_continent]
else:
    filtered_df = df_cars

fig, ax = plt.subplots()
sns.heatmap(filtered_df.iloc[:,:-1].corr(), center=0, cmap="YlGnBu", annot=True)
plt.title(f"Correlation heatmap - Continent : {selected_continent}")
st.pyplot(fig)



st.markdown("## Line plot ")

fig4, ax = plt.subplots()
sns.lineplot(data=filtered_df, x="year", y="hp")
st.pyplot(fig4)


st.markdown("## Regplot ")

fig3, ax = plt.subplots()
sns.regplot(data = filtered_df, x='year', y='cylinders', )
st.pyplot(fig3)


st.markdown("## KMeans ")

X = df_cars[['mpg', 'cylinders', 'cubicinches', 'hp', 'weightlbs', 'time-to-60', 'year']]

modelKM = KMeans(n_clusters=3, random_state=3)
modelKM.fit(X)
modelKM.cluster_centers_

fig2, axes = plt.subplots(figsize=(15, 5), nrows=1, ncols=2)

sns.scatterplot(x=X.cylinders, y=X.cubicinches, hue=modelKM.labels_, ax=axes[0])
sns.scatterplot(data = df_cars, x='cylinders', y='cubicinches', hue='continent', ax=axes[1])
st.pyplot(fig2)


st.markdown("🦝")