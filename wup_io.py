"""
==== Source for the data used in this visualization ====
    United Nations, Department of Economic and Social
    Affairs, Population Division (2018).
    World Urbanization Prospects: The 2018 Revision, Online Edition.

File 22: Annual Population of Urban Agglomerations
         with 300,000 Inhabitants or More in 2018,
         by Country, 1950-2035 (thousands)

====  Original license used for the UN data ====
Copyright © 2018 by United Nations, made available under
a Creative Commons license CC BY 3.0 IGO:
http://creativecommons.org/licenses/by/3.0/igo/
"""

# NOTE: the .csv file was converted in LibreOffice
# original file link:
#https://esa.un.org/unpd/wup/Download/Files/WUP2018-F22-Cities_Over_300K_Annual.xls

import pandas as pd

def preprocess_wup2018(fname="data/WUP2018-F22-Cities_Over_300K_Annual.csv"):
    df = pd.read_csv(fname, thousands=" ", skiprows=16, index_col=4)

    # adding some basics on the UN-projected city growth, 2018-2035
    df["growthabs"] = df["2035"] - df["2018"]
    df["growthperc"] = df["growthabs"] / df["2018"] * 100

    return df
