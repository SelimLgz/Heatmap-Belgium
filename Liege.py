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

# Save the map to an HTML file
m.save("heatmap.html")
