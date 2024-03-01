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

palette = ["#ac491a", "#644c90"]
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

#%% Alcohol

data["Increased/Higer risk drinking %"] = 100*data["Increased/Higer risk drinking"]

# Factor by ethnicity
fig = plt.figure(figsize = (6,4))
sns.barplot(data, x="Ethnic Group", y = "Increased/Higer risk drinking %", hue = "Gender",
            palette = palette, hue_order = ["Female", "Male"])
plt.ylabel("% of HC Attendees with increased/higher\nrisk drinking levels")
plt.xlabel("")
fig.savefig("../output/alcohol/alcohol-eth.png", bbox_inches = "tight", dpi = 300)

# Factor by IMD
fig = plt.figure(figsize = (6,4))
sns.barplot(data, x="GP IMD Quintile", y = "Increased/Higer risk drinking %", hue = "Gender",
            palette = palette, hue_order = ["Female", "Male"])
plt.ylabel("% of HC Attendees with increased/higher\nrisk drinking levels")
plt.xlabel("")
plt.xticks([0,1,2,3,4], 
           ["1\n(Most deprived)", "2", "3","4", "5\n(Least deprived)"])
fig.savefig("../output/alcohol/alcohol-IMD.png", bbox_inches = "tight", dpi = 300)


# Factor inequality matrix
data["Increased/Higer\nrisk drinking"] = data["Increased/Higer risk drinking"]
for gender in list(genders.keys()):
    data_i = data[data["Gender"] == gender]
    title = "Increased/Higer\nrisk drinking" 
    
    count_pivot = Mat.get_pivot(
        data_i,
        eth_col = "Ethnic Group", 
        IMD_col = "GP IMD Quintile",
        mode="count"
        )
    
    perc_pivot = Mat.get_pivot(
        data_i,
        column = title,
        eth_col = "Ethnic Group", 
        IMD_col = "GP IMD Quintile",
        mode="percentage"
        )
    
    fig = Mat.inequality_map(count_pivot, 
                       perc_pivot = perc_pivot, 
                       palette = genders[gender]["Palette"],
                       title = title + "(" + gender + ")",
                       ttest = True)
    
    fig.savefig("../output/alcohol/alcohol-matrix-{}.png".format(gender.lower()),
                bbox_inches = "tight", dpi = 300)
    
#%% Inactivity

data["Broad_activity_term"] =  data["Broad_activity_term"].fillna("Unknown")
data.value_counts("Broad_activity_term")
print("Activity data missing for {:3.3}% of cases".format(100*10863/len(data)))

# Filter out unknown cases
data3 = data[data["Broad_activity_term"] != "Unknown"]
data3["Inactive"] = data3["Broad_activity_term"] == "inactive"
data3["Inactive %"] = 100*data3["Inactive"]

# Factor by ethnicity
fig = plt.figure(figsize = (6,4))
sns.barplot(data3, x="Ethnic Group", y = "Inactive %", hue = "Gender",
            palette = palette, hue_order = ["Female", "Male"])
plt.ylabel("% of HC Attendees asked\nwho are physically inactive")
plt.xlabel("")
fig.savefig("../output/inactivity/inactivity-eth.png", bbox_inches = "tight", dpi = 300)

# Factor by IMD
fig = plt.figure(figsize = (6,4))
sns.barplot(data3, x="GP IMD Quintile", y = "Inactive %", hue = "Gender",
            palette = palette, hue_order = ["Female", "Male"])
plt.ylabel("% of HC Attendees asked\nwho are physically inactive")
plt.xlabel("")
plt.xticks([0,1,2,3,4], 
           ["1\n(Most deprived)", "2", "3","4", "5\n(Least deprived)"])
fig.savefig("../output/inactivity/inactivity-IMD.png", bbox_inches = "tight", dpi = 300)


# Factor inequality matrix
data3["Physical Inactivity"] = data3["Inactive"]
for gender in list(genders.keys()):
    data_i = data3[data3["Gender"] == gender]
    title = "Physical Inactivity"
    
    count_pivot = Mat.get_pivot(
        data_i,
        eth_col = "Ethnic Group", 
        IMD_col = "GP IMD Quintile",
        mode="count"
        )
    
    perc_pivot = Mat.get_pivot(
        data_i,
        column = title,
        eth_col = "Ethnic Group", 
        IMD_col = "GP IMD Quintile",
        mode="percentage"
        )
    
    fig = Mat.inequality_map(count_pivot, 
                       perc_pivot = perc_pivot, 
                       palette = genders[gender]["Palette"],
                       title = title + "(" + gender + ")",
                       ttest = True)
    
    fig.savefig("../output/inactivity/inactivity-matrix-{}.png".format(gender.lower()),
                bbox_inches = "tight", dpi = 300)
    