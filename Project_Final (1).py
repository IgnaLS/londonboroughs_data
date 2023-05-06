#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import json
from urllib.request import urlopen
import plotly.express as px
import plotly.graph_objects as go


# In[2]:


import os

os.chdir(r"C:\Università\Luiss\2nd semester\Data Visualization\Project work\FINAL\2")


# In[3]:


london_map = json.load(open("london_boroughs.json", "r"))


# In[4]:


london_map["features"][0].keys()


# In[5]:


london_map["features"][0]["properties"]


# In[6]:


london_map["features"][0]


# In[7]:


borough_id_map = {}
for feature in london_map["features"]:
    feature["code"] = feature["properties"]["code"]
    borough_id_map[feature["properties"]["name"]] = feature["code"]


# In[8]:


borough_id_map


# In[9]:


london_data = pd.read_csv("london_boroughs.csv")
london_data.head(4)


# In[10]:


london_data.area = london_data.area.str.capitalize()


# In[11]:


london_data.columns


# In[12]:


import plotly.io as pio
pio.renderers.default = "jupyterlab"


# **Note:**
# 
# We’ll have to set the ‘featureidkey’ to our case. The ‘featureidkey’ indicates the key to the joint in the geojson file, while ‘locations’ does the same, but for the DataFrame. 

# **Mapbox**

# In[13]:


london_data.sort_values(by = "median_salary", ascending = True)


# 
# 

# #### Median salary

# In[59]:


fig = px.choropleth_mapbox(london_data,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "median_salary",
                    range_color = (28000, 62000),
                    hover_name = "area",
                    hover_data = ["population_size"],
                    title = "Greater London Area",
                    mapbox_style = "carto-positron",
                    color_continuous_scale = "Viridis",
                    #color_continuous_midpoint = 0,
                    opacity = 0.8,
                    center = {"lat": 51.489, "lon": -0.12765},
                    labels = {"code":"Code", "population_size":"Population",
                             "median_salary":"Median Salary (%)"},
                    zoom = 8.5)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})        # just remove margin
fig.show()


# 
# 

# ### What are the most populated boroughs?

# In[63]:


fig = px.choropleth_mapbox(london_data,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "population_size",
                    # range_color = (28000, 62000),
                    hover_name = "area",
                    # hover_data = ["population_size"],
                    title = "Population size by borough in the GLA",
                    mapbox_style = "carto-positron",
                    color_continuous_scale = "Viridis_r",
                    #color_continuous_midpoint = 0,
                    opacity = 0.8,
                    center = {"lat": 51.489, "lon": -0.12765},
                    labels = {"code":"Code", "population_size":"Population",
                             "median_salary":"Median Salary (%)"},
                    zoom = 8.5)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})        # just remove margin
fig.show()


# 
# 

# #### Loading 'london_data_2' (all the details about it in the "Cleaning and Scraping" file)

# In[15]:


london_data_2 = pd.read_csv("london_data_2.csv")
london_data_2.head()


# 
# 

# #### Remain results at Brexit referendum

# In[60]:


fig = px.choropleth_mapbox(london_data_2,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Remain",
                    color_continuous_scale = "Viridis",
                    range_color = (30, 80),
                    hover_name = "area",
                    hover_data = ["Votes Cast", "Turnout"],
                    title = "Brexit Referendum in the GLA, Remain (%)",
                    mapbox_style = "carto-positron",
                    #color_continuous_midpoint = 0,
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "population_size":"Population",
                             "Remain":"Remain %"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# #### Turnout at Brexit Referendum

# In[18]:


fig = px.choropleth_mapbox(london_data_2,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Turnout",
                    color_continuous_scale = "Viridis",
                    range_color = (59, 83),
                    hover_name = "area",
                    hover_data = ["Votes Cast", "Turnout"],
                    title = "Brexit Referendum in the GLA, Turnout (%)",
                    mapbox_style = "carto-positron",
                    #color_continuous_midpoint = 0,
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "population_size":"Population",
                             "Turnout":"Turnout %"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# In[ ]:





# ### Using data elaborated in the "Cleaning and Scraping" file

# In[19]:


pd.set_option('display.max_columns', 55)


# In[20]:


london_data_5 = pd.read_csv("london_data_4.csv")


# In[21]:


london_data_5.head()


# In[22]:


len(london_data_5)


# In[23]:


london_data_5.info()


# In[24]:


# Select rows with at least one NaN value
london_data_5[london_data_5.isna().any(axis=1)]


# 
# 

# ### General EDA

# In[96]:


import matplotlib.pyplot as plt

corr_matrix = london_data_5.drop(columns = ["code", "mean_salary", "area_size", "no_of_houses",
                                                        "Votes Cast", "Leave", "Largest migrant population by country of birth (2011)",
                                                         "(New) Largest migrant population by country of birth (2011)",
                                                         "Second largest migrant population by country of birth (2011)",
                                                         "Proportion of 16-18 year olds who are NEET (%) (2014)", "% working-age with a disability (2015)",
                                                        "Homes Owned outright, (2014) %", "Total carbon emissions (2013)",
                                                        "Household Waste Recycling Rate, 2014/15", "Happiness score 2011-14 (out of 10)",
                                                        "Childhood Obesity Prevalance (%) 2014/15", "Political control in council"]).corr()

# Plot the correlation matrix
plt.matshow(corr_matrix)

plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=90)
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)
plt.colorbar()
plt.show()


# In[97]:


pd.plotting.scatter_matrix(london_data_5.drop(columns = ["code", "mean_salary", "area_size", "no_of_houses",
                                                        "Votes Cast", "Leave", "Largest migrant population by country of birth (2011)",
                                                         "(New) Largest migrant population by country of birth (2011)",
                                                         "Second largest migrant population by country of birth (2011)",
                                                         "Proportion of 16-18 year olds who are NEET (%) (2014)", "% working-age with a disability (2015)",
                                                        "Homes Owned outright, (2014) %", "Total carbon emissions (2013)",
                                                        "Household Waste Recycling Rate, 2014/15", "Happiness score 2011-14 (out of 10)",
                                                        "Childhood Obesity Prevalance (%) 2014/15", "Political control in council"]),
                                                        figsize = (85, 60))


# In[ ]:





# 
# 

# #### Average Age (2016 data)

# In[26]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Average Age, 2016",
                    color_continuous_scale = "Viridis_r",
                    #range_color = (30, 45),
                    hover_name = "area",
                    title = "Average age in the GLA",
                    mapbox_style = "carto-positron",
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "Average Age, 2016":"Average Age"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# #### Unemployment rate (2015)

# In[58]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Unemployment rate (2015)",
                    color_continuous_scale = "Viridis_r",
                    hover_name = "area",
                    title = "Unemployment rate in the GLA",
                    mapbox_style = "carto-positron",
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "Unemployment rate (2015)":"Unemployment rate"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# ### Youth Unemployment Rate

# In[57]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Youth Unemployment (claimant) rate 18-24 (Dec-14)",
                    color_continuous_scale = "Viridis_r",
                    hover_name = "area",
                    title = "Youth Unemployment (claimant) rate 18-24 in the GLA",
                    mapbox_style = "carto-positron",
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "Youth Unemployment (claimant) rate 18-24 (Dec-14)":"Youth Unemployment (claimant) rate 18-24"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 

# ### Happiness score (out of 10)

# In[29]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Happiness score 2011-14 (out of 10)",
                    color_continuous_scale = "Viridis",
                    hover_name = "area",
                    title = "Happiness score (out of 10) in the GLA",
                    mapbox_style = "carto-positron",
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "Happiness score 2011-14 (out of 10)":"Happiness score (out of 10)"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# In[ ]:





# 
# 

# #### Net internal migration

# In[30]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Net internal migration (2014)",
                    color_continuous_scale = "Viridis",
                    hover_name = "area",
                    title = "Net internal migration in the GLA",
                    mapbox_style = "carto-positron",
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "Net internal migration (2014)":"Net internal migration"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# #### Crime rates per thousand population 2014/15

# In[31]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Crime rates per thousand population 2014/15",
                    color_continuous_scale = "Viridis_r",
                    hover_name = "area",
                    title = "Crime rates per thousand population in the GLA",
                    mapbox_style = "carto-positron",
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "Crime rates per thousand population 2014/15":"Crime rate"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# ### Number of cars per household

# In[32]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Number of cars per household, (2011 Census)",
                    color_continuous_scale = "Viridis_r",
                    hover_name = "area",
                    title = "Crime rates per thousand population in the GLA",
                    mapbox_style = "carto-positron",
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "Number of cars per household, (2011 Census)":"Cars per household"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# ### Childhood Obesity

# In[33]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Childhood Obesity Prevalance (%) 2014/15",
                    color_continuous_scale = "Viridis_r",
                    hover_name = "area",
                    title = "Childhood Obesity Prevalance (%) in the GLA",
                    mapbox_style = "carto-positron",
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "Childhood Obesity Prevalance (%) 2014/15":"Childhood Obesity Prevalance (%)"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# ### % of pupils whose first language is not English (2015)

# In[34]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "% of pupils whose first language is not English (2015)",
                    color_continuous_scale = "Viridis",
                    hover_name = "area",
                    title = "% of pupils whose first language is not English in the GLA",
                    mapbox_style = "carto-positron",
                    #color_continuous_midpoint = 0,
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code",
                           "% of pupils whose first language is not English (2015)":"% of pupils whose first language is not English"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# ### Accessibility to public transport

# In[35]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Average Public Transport Accessibility score, 2014",
                    color_continuous_scale = "Viridis",
                    range_color = (2, 8),
                    hover_name = "area",
                    title = "Average Public Transport Accessibility Score in the GLA",
                    mapbox_style = "carto-positron",
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code",
                           "Average Public Transport Accessibility score, 2014":"Average Public Transport Accessibility Score"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# #### Politics

# In[36]:


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "Political control in council",
                    color_continuous_scale = "Viridis_r",
                    hover_name = "area",
                    title = "Political control in council in the GLA",
                    mapbox_style = "carto-positron",
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# 
# 

# #### Largest migrant population by country of birth (2011)

# In[71]:


london_data_5.columns.to_list()


# In[72]:


london_data_5.iloc[:, 15]


# In[37]:


# Alternatively, we can use INSERT
london_data_5.insert(16, "(New) Largest migrant population by country of birth (2011)", "Value")


# In[38]:


london_data_5.head(2)


# In[40]:


# Mapping
london_data_5["(New) Largest migrant population by country of birth (2011)"] = london_data_5["Largest migrant population by country of birth (2011)"].map({"United States":"United States", "France":"France",
"Ireland":"Ireland", "India":"India", "Poland":"Others", "Nigeria":"Nigeria",
"Turkey":"Others", "Sri Lanka":"Others", "Jamaica":"Others",
"Bangladesh":"Others", "Pakistan":"Others"})


# In[41]:


london_data_5


# In[51]:


color_map = {
    'United States': '#01e2f6',
    'India': '#e0b8c0',
    'Ireland': 'green',
    'France': '#bb0044',
    'Nigeria': '#fedd3e',
    'Others': '#d2e1f0'
}


fig = px.choropleth_mapbox(london_data_5,
                    geojson = london_map,
                    locations = 'code',
                    featureidkey = 'properties.code',
                    color = "(New) Largest migrant population by country of birth (2011)",
                    #color_continuous_scale = "Plasma",
                    color_discrete_map = color_map,
                    #range_color = (-10000, 10000),
                    hover_name = "area",
                    title = "Largest migrant population by country of birth in the GLA",
                    mapbox_style = "carto-positron",
                    #color_continuous_midpoint = 0,
                    opacity = 0.8,
                    center = {"lat": 51.49, "lon": -0.12765},
                    labels = {"code":"Code", "(New) Largest migrant population by country of birth":"(New) Largest migrant population by country of birth"},
                    zoom = 8.37)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin=dict(l=0, r=0, t=30, b=0), title_font=dict(size=20, family='Helvetica'))
fig.show()


# In[ ]:





# In[ ]:





# ### Scatterplots

# In[43]:


from sklearn.linear_model import LinearRegression

df1 = london_data_5[["median_salary", "Happiness score 2011-14 (out of 10)"]]
df1 = df1.dropna()
x = df1["median_salary"].values
y = df1["Happiness score 2011-14 (out of 10)"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x = x, y = y, mode = 'markers', marker = dict(color = 'blue', size=13),
                           text = london_data_5['area'], name = "", showlegend = False)
line_trace = go.Scatter(x = line_x, y = line_y, mode = 'lines', line = dict(color='red'),
                        name = f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data = [scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Median Salary and Happiness",
                  xaxis_title = 'Median Salary', 
                  yaxis_title = 'Happiness score')


# In[44]:


df2 = london_data_5[["Employment rate (%) (2015)", "Number of cars per household, (2011 Census)"]]
df2 = df2.dropna()
x = df2["Employment rate (%) (2015)"].values
y = df2["Number of cars per household, (2011 Census)"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x = x, y = y, mode = 'markers', marker = dict(color = 'blue', size = 13),
                           text = london_data_5['area'], name = "", showlegend = False)
line_trace = go.Scatter(x = line_x, y = line_y, mode = 'lines', line = dict(color='red'),
                        name = f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data = [scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Employment and Number of Cars",
                  xaxis_title = 'Employment rate', 
                  yaxis_title = 'Number of cars per household')


# In[71]:


df3 = london_data_5[["Youth Unemployment (claimant) rate 18-24 (Dec-14)", "Childhood Obesity Prevalance (%) 2014/15"]]
df3 = df3.dropna()
x = df3["Youth Unemployment (claimant) rate 18-24 (Dec-14)"].values
y = df3["Childhood Obesity Prevalance (%) 2014/15"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x = x, y = y, mode = 'markers', marker = dict(color='blue', size=13),
                           text = london_data_5['area'], name = "", showlegend = False)
line_trace = go.Scatter(x = line_x, y=line_y, mode='lines', line = dict(color='red'),
                        name = f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data = [scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Youth Unemployment and Childhood Obesity",
                  xaxis_title = 'Youth Unemployment (claimant) rate 18-24', 
                  yaxis_title = 'Childhood Obesity Prevalance (%)')

fig.show()


# In[52]:


df1 = london_data_5[["Average Public Transport Accessibility score, 2014", "Number of cars per household, (2011 Census)"]]
df1 = df1.dropna()
x=df1["Average Public Transport Accessibility score, 2014"].values
y=df1["Number of cars per household, (2011 Census)"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5['area'], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Transport and Number of Cars",
                  xaxis_title='Average Public Transport Accessibility Score', 
                  yaxis_title='Number of cars per household')

fig.show()


# In[53]:


df1 = london_data_5[["area", "% of resident population born abroad (2014)", "Crime rates per thousand population 2014/15"]]
df1 = df1.dropna()
x=df1["% of resident population born abroad (2014)"].values
y=df1["Crime rates per thousand population 2014/15"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x = x, y = y, mode = 'markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation of Immigrant Population and Crime Rate per borough",
                  xaxis_title='% of resident population born abroad', 
                  yaxis_title='Crime rates per thousand population')

fig.show()


# In[55]:


df1 = london_data_5[["area", "Unemployment rate (2015)", "Crime rates per thousand population 2014/15"]]
df1 = df1.dropna()
x = df1["Unemployment rate (2015)"].values
y = df1["Crime rates per thousand population 2014/15"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x = line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name = f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Unemployment Rate and Crime Rate per borough",
                  xaxis_title = 'Unemployment rate',
                  yaxis_title = 'Crime rates per thousand population')

fig.show()


# In[56]:


df1 = london_data_5[["area", "Remain", "Average Age, 2016"]]
df1 = df1.dropna()
x = df1["Average Age, 2016"].values
y = df1["Remain"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Age and Vote for Remain",
                  xaxis_title = 'Average Age', 
                  yaxis_title = 'Remain (%)')

fig.show()


# In[50]:


df1 = london_data_5[["area", "median_salary", "Crime rates per thousand population 2014/15"]]
df1 = df1.dropna()
x=df1["median_salary"].values
y=df1["Crime rates per thousand population 2014/15"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Salary and Crime",
                  xaxis_title = 'Median Salary', 
                  yaxis_title = 'Crime rates per thousand population')

fig.show()


# In[65]:


df1 = london_data_5[["area", "Remain", "median_salary"]]
df1 = df1.dropna()
x=df1["Remain"].values
y=df1["median_salary"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Remain and Median Salary",
                  xaxis_title = 'Remain', 
                  yaxis_title = 'Median Salary')

fig.show()


# In[84]:


df1 = london_data_5[["area", "Remain", "Net international migration (2014)"]]
df1 = df1.dropna()
x=df1["Remain"].values
y=df1["Net international migration (2014)"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Remain and Net international migration",
                  xaxis_title = 'Remain', 
                  yaxis_title = 'Net international migration')

fig.show()


# In[73]:


df10 = london_data_5[["area", "Remain", "Unemployment rate (2015)"]]
df10 = df10.dropna()
x=df10["Remain"].values
y=df10["Unemployment rate (2015)"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Remain and Unemployment rate",
                  xaxis_title = 'Remain',
                  yaxis_title = 'Unemployment rate (2015)')

fig.show()


# In[75]:


df10 = london_data_5[["area", "Remain", "Jobs Density, 2014"]]
df10 = df10.dropna()
x=df10["Remain"].values
y=df10["Jobs Density, 2014"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Remain and Jobs Density, 2014",
                  xaxis_title = 'Remain',
                  yaxis_title = 'Jobs Density, 2014')

fig.show()


# In[76]:


df10 = london_data_5[["area", "Remain", "Crime rates per thousand population 2014/15"]]
df10 = df10.dropna()
x=df10["Remain"].values
y=df10["Crime rates per thousand population 2014/15"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Remain and Crime rates per thousand population 2014/15",
                  xaxis_title = 'Remain',
                  yaxis_title = 'Crime rates per thousand population 2014/15')

fig.show()


# In[78]:


df10 = london_data_5[["area", "Remain", "Median House Price, 2014"]]
df10 = df10.dropna()
y=df10["Remain"].values
x=df10["Median House Price, 2014"].values
corr_coef = np.corrcoef(x, y)[0][1]

# Calculating the line equation using linear regression
regressor = LinearRegression()
regressor.fit(x.reshape(-1, 1), y.reshape(-1, 1))
line_x = np.array([min(x), max(x)])
line_y = regressor.predict(line_x.reshape(-1, 1)).flatten()

scatter_trace = go.Scatter(x=x, y=y, mode='markers', marker = dict(color='blue', size=13),
                           text = london_data_5["area"], name = "", showlegend = False)
line_trace = go.Scatter(x=line_x, y=line_y, mode='lines', line=dict(color='red'),
                        name=f'Correlation Line (r={corr_coef:.2f})', text = corr_coef, showlegend = False)
fig = go.Figure(data=[scatter_trace, line_trace])
fig.update_layout(title = "Correlation between Remain and Median House Price, 2014",
                  xaxis_title = 'Median House Price, 2014',
                  yaxis_title = 'Remain')


fig.show()


# In[ ]:





# In[ ]:





# In[ ]:




