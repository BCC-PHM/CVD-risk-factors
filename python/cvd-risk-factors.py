# -*- coding: utf-8 -*-
"""
HC demographics for CVD work
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import EquiPy.Matrix as Mat

custom_params = {"axes.spines.right": False, "axes.spines.top": False}
sns.set_theme(style="ticks", rc=custom_params)

palette = ["#8172b3", "#dd8452"]
#%% Load and preprocess data
file = r"\\svwvap1126.addm.ads.brm.pri\PHSensitive$\Intelligence New\Themes\Health Checks\Health Check Results\HC-processed-2018-2022.xlsx"
data = pd.read_excel(file)

data["GP IMD Quintile"] = np.floor((data["IMD_Score"]+1)/2).astype(int)

data["Obesity %"] = 100*data["Obese"]

data["Ethnic Group"] =  data["Ethnicity_Broad"].fillna("Unknown")

data = data[data["Ethnic Group"] != "Other"]

# This is over-engineered
genders = {
    "Female" : {
        "Palette" : "Oranges"
        },
    "Male" : {
        "Palette" : "Purples"
        }
    }

#%% Obesity
data2 = data.copy()
# ethnicity sensitive threshold
data2["Obesity Threshold"] = np.where(data2['Ethnic Group'] == "Asian", 27.5,
                            np.where(data2['Ethnic Group'] == "Black", 27.5,
                            np.where(data2['Ethnic Group'] == "Mixed", 30,
                            np.where(data2['Ethnic Group'] == "Unknown", 30,
                            np.where(data2['Ethnic Group'] == "White", 30, 
                               'Error'))))).astype(float)

data2["Obese"] = data2["BMI"] >= data2["Obesity Threshold"]
data2["Obesity %"] = 100*data2["Obese"]

# Factor by ethnicity
fig = plt.figure(figsize = (6,4))
sns.barplot(data2, x="Ethnic Group", y = "Obesity %", hue = "Gender",
            palette = palette, hue_order = ["Female", "Male"])
plt.ylabel("% of HC Attendees with Obesity")
plt.xlabel("")
fig.savefig("../output/obesity/obesity-eth.png", bbox_inches = "tight", dpi = 300)

# Factor by IMD
fig = plt.figure(figsize = (6,4))
sns.barplot(data2, x="GP IMD Quintile", y = "Obesity %", hue = "Gender",
            palette = palette, hue_order = ["Female", "Male"])
plt.ylabel("% of HC Attendees with Obesity")
plt.xlabel("")
plt.xticks([0,1,2,3,4], 
           ["1\n(Most deprived)", "2", "3","4", "5\n(Least deprived)"])
fig.savefig("../output/obesity/obesity-IMD.png", bbox_inches = "tight", dpi = 300)

# Factor inequality matrix
for gender in list(genders.keys()):
    data_i = data2[data2["Gender"] == gender]
    title = "Obese (" + gender + ")" 
    data_i[title] = data_i["Obese"]
    
    count_pivot = Mat.get_pivot(
        data_i,
        eth_col = "Ethnic Group", 
        IMD_col = "GP IMD Quintile",
        mode="count"
        )
    
    perc_pivot = Mat.get_pivot(
        data_i,
        column = "Obese",
        eth_col = "Ethnic Group", 
        IMD_col = "GP IMD Quintile",
        mode="percentage"
        )
    
    fig = Mat.inequality_map(count_pivot, 
                       perc_pivot = perc_pivot, 
                       palette = genders[gender]["Palette"],
                       title = title,
                       ttest = True)
    
    fig.savefig("../output/obesity/obesity-matrix-{}.png".format(gender.lower()),
                bbox_inches = "tight", dpi = 300)
