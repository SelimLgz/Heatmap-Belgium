import pandas as pd
import geopandas as gpd
import numpy as np
from branca.colormap import linear
from unidecode import unidecode

# Show the sheet names in the Excel file
xls = pd.ExcelFile("Heatmap Liege/Population_par_commune.xlsx")
# print(xls.sheet_names)

# Load population data
pop_df = pd.read_excel(xls, sheet_name='Population en 2024', skiprows=1)
# print(pop_df.head())
# Clean the population data
# print(pop_df.columns)
pop_df_clean = pop_df[[' Code INS', 'Lieu de Résidence', 'Total']].copy()
# Remove the first two rows which are not needed
pop_df_clean = pop_df_clean.drop(index=[0, 1])
# print(pop_df_clean.head())

# Load the map
geo_df = gpd.read_file("Heatmap Liege/communesgemeente-belgium.geojson")
# print(geo_df.columns)
# print(geo_df['mun_name_upper_fr'].unique())

def remove_accents(text):
    if pd.isnull(text):
        return ""
    return unidecode(str(text))

geo_df['mun_name_upper_fr'] = geo_df['mun_name_upper_fr'].astype(str).str.strip().str.lower().apply(remove_accents)
pop_df_clean['Lieu de Résidence'] = pop_df_clean['Lieu de Résidence'].astype(str).str.strip().str.lower().apply(remove_accents)

# Due to a naming error, we need to rename a municipality
geo_df.loc[geo_df['mun_name_upper_fr'] == 'zwalm', 'mun_name_upper_fr'] = 'zwalin'

# Merge the two tables
merged = geo_df.merge(pop_df_clean, left_on="mun_name_upper_fr", right_on="Lieu de Résidence", how="left")
print(merged['Total'].isnull().sum(), "missing population values after merge")
print(list(merged[merged['Total'].isnull()]['mun_name_upper_fr']))


import folium
from folium.features import Choropleth

# Create a map centered on Liège
m = folium.Map(location=[50.6, 5.6], zoom_start=8)

import numpy as np


# Define custom bins (adjust values to your data)
bins = [0, 10000, 20000, 40000, 80000, 130000, 190000, 250000, 310000, 390000, 500000, 560000]

folium.Choropleth(
    geo_data=merged,
    data=merged,
    columns=['Lieu de Résidence', 'Total'],
    key_on='feature.properties.mun_name_upper_fr',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Population by municipality in 2024',
    bins=bins
).add_to(m)

# Add custom icons for clubs
clubs = [
    {"name": "Anderlecht", "lat": 50.83415112259992, "lon": 4.29891755948624, \
     "logo": "Heatmap Liege/Logo/Anderlecht.png"},

    {"name": "Antwerp", "lat": 51.23244563352655, "lon": 4.472093472865853, \
     "logo": "Heatmap Liege/Logo/Antwerp.png"},

     {"name": "Beerschot", "lat": 51.18515949226264, "lon": 4.382210848856054, \
     "logo": "Heatmap Liege/Logo/Beerschot.png"},

     {"name": "Bruges", "lat": 51.19330505127287, "lon": 3.180100739052433, \
     "logo": "Heatmap Liege/Logo/Bruges.png"},

     {"name": "Cercle de Bruges", "lat": 51.19330505127287, "lon": 3.180100739052433, \
     "logo": "Heatmap Liege/Logo/Cercle de Bruges.png"},

     {"name": "Charleroi", "lat": 50.414220562376265, "lon": 4.452750627166207, \
     "logo": "Heatmap Liege/Logo/Charleroi.png"},

     {"name": "Dender", "lat": 50.8841080141755, "lon": 4.072654014377263, \
     "logo": "Heatmap Liege/Logo/Dender.png"},

     {"name": "Gantoise", "lat": 51.01646440861245, "lon": 3.733546694254544, \
     "logo": "Heatmap Liege/Logo/Gantoise.png"},

     {"name": "Genk", "lat": 51.00505489986331, "lon": 5.533362586232373, \
     "logo": "Heatmap Liege/Logo/Genk.png"},

     {"name": "Kortrijk", "lat": 50.830438262036196, "lon": 3.2490187465830513, \
     "logo": "Heatmap Liege/Logo/Kortrijk.png"},

     {"name": "Leuven", "lat": 50.86838821201999, "lon": 4.694395216215148, \
     "logo": "Heatmap Liege/Logo/Leuven.png"},

     {"name": "Liege", "lat": 50.609854432689545, "lon": 5.543357514011962, \
     "logo": "Heatmap Liege/Logo/Liege.png"},

     {"name": "Mechelen", "lat": 51.03783180885648, "lon": 4.471613256103485, \
     "logo": "Heatmap Liege/Logo/Mechelen.png"},

     {"name": "Saint truidense", "lat": 50.81353810128787, "lon": 5.166297971733279, \
     "logo": "Heatmap Liege/Logo/Saint truidense.png"},

     {"name": "USG", "lat": 50.817815456549255, "lon": 4.329338801355258, \
     "logo": "Heatmap Liege/Logo/USG.png"},

     {"name": "Westerlo", "lat": 51.09487534320355, "lon": 4.928956299856769, \
     "logo": "Heatmap Liege/Logo/Waterlo.png"}
]


for club in clubs:
    icon = folium.CustomIcon(club["logo"], icon_size=(40, 40))
    folium.Marker(
        location=[club["lat"], club["lon"]],
        icon=icon,
        tooltip=club["name"]
    ).add_to(m)

# Save the map to an HTML file

m.save("heatmap.html")
