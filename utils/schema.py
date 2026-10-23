"""Field names and labels for Excel exports."""
NUMERIC = ["consumption_mw", "nuclear_mw", "wind_mw", "solar_mw", "hydro_mw", "thermal_mw", "bioenergy_mw", "exchange_mw"]
GENERATION = ["nuclear_mw", "wind_mw", "solar_mw", "hydro_mw", "thermal_mw", "bioenergy_mw"]
RENEWABLES = ["wind_mw", "solar_mw", "hydro_mw", "bioenergy_mw"]
LABELS = {
    "consumption_mw": "Electricity demand",
    "nuclear_mw": "Nuclear", "wind_mw": "Wind", "solar_mw": "Solar",
    "hydro_mw": "Hydropower", "thermal_mw": "Thermal", "bioenergy_mw": "Bioenergy",
    "exchange_mw": "Physical exchanges",
}
SOURCE_HIST = "eco2mix-regional-cons-def"
SOURCE_LIVE = "eco2mix-regional-tr"
REGION_POINTS = {
    "Auvergne-Rhône-Alpes": (45.764, 4.836), "Bourgogne-Franche-Comté": (47.322, 5.042),
    "Bretagne": (48.117, -1.678), "Centre-Val de Loire": (47.903, 1.909),
    "Grand Est": (48.573, 7.752), "Hauts-de-France": (50.630, 3.057),
    "Île-de-France": (48.857, 2.352), "Normandie": (49.443, 1.099),
    "Nouvelle-Aquitaine": (44.838, -0.580), "Occitanie": (43.605, 1.444),
    "Pays de la Loire": (47.218, -1.554),
    "Provence-Alpes-Côte d'Azur": (43.296, 5.370),
}
