#!/usr/bin/env python
# coding: utf-8

# ### Web scraping for the Brexit Referendum elections
# 
# Here we used the **BeautifulSoup library** to scrape information from the page "https://www.londoncouncils.gov.uk/node/29459"

# In[103]:


import os

os.chdir(r"C:\Università\Luiss\2nd semester\Data Visualization\Project work\FINAL\2")


# In[104]:


import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.londoncouncils.gov.uk/node/29459'
response = requests.get(url)

# Parsing the HTML content using BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')

# Findinf the table element containing the data
table = soup.find('table')

# Extracting the table rows
rows = []
for tr in table.find_all('tr'):
    row = [td.text.strip() for td in tr.find_all('td')]
    if row:
        rows.append(row)

# Extracting the required columns from the rows
data = []
for row in rows:
    borough = row
    votes_cast = row[1]
    turnout = row[2]
    leave = row[3]
    remain = row[4]
    data.append([borough, votes_cast, turnout, leave, remain])

# Writing the data to a CSV file
with open('brexit_referendum_2016.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Borough', 'Votes Cast', 'Turnout', 'Leave', 'Remain'])
    writer.writerows(data)


# 
# 

# ### Cleaning the data scraped

# In[105]:


import pandas as pd
import numpy as np


# In[106]:


brexit = pd.read_csv("brexit_referendum_2016.csv")
brexit.head()


# In[107]:


brexit.drop(labels = 0, inplace = True)


# In[108]:


# Reset the index starting from 0
brexit = brexit.reset_index(drop=True)


# In[109]:


# Clean all the needless characters 

brexit.Borough = brexit.Borough.str.replace('\[\]', '').str.replace('\d+', '').str.replace(',', '').str.replace("'", '')
brexit.Borough = brexit.Borough.str.replace('[', '').str.replace(']', '').str.replace('.', '').str.replace('%', '')
brexit["Votes Cast"] = brexit["Votes Cast"].str.replace(',', '')
brexit.Turnout = brexit.Turnout.str.replace('%', '').str.replace('&', '')
brexit.Remain = brexit.Remain.str.replace(',', '')
brexit.Leave = brexit.Leave.str.replace(',', '')

brexit["Votes Cast"] = brexit["Votes Cast"].astype("int")
brexit.Remain = brexit.Remain.astype("int")
brexit.Turnout = brexit.Turnout.astype("float")
brexit.Leave = brexit.Leave.astype("int")


# In[110]:


brexit.info()


# In[111]:


brexit.head(7)


# In[112]:


brexit_2 = brexit.copy()


# In[113]:


# Since in the other dataset we have "City of london" as first row and "Barking and Dagenham" ad second,
# here we just fixed the order
brexit_2.loc[[0, 1, 2, 3, 4, 5, 6]] = brexit_2.loc[[6, 0, 1, 2, 3, 4, 5]].values


# In[114]:


brexit_2.head(7)


# 
# 

# ### Concatenate this dataset with our first one (london_boroughs.csv) - LONDON_DATA_2 

# In[115]:


london_data = pd.read_csv("london_boroughs.csv")
london_data.area = london_data.area.str.capitalize()
london_data_2 = pd.concat([london_data, brexit_2], axis=1) 


# In[116]:


london_data_2.head(8)


# In[117]:


# Making the 'Remain' attribute a percentage, as well as 'Leave'
london_data_2.Remain = london_data_2.Remain / london_data_2["Votes Cast"]


# In[118]:


london_data_2.Leave = london_data_2.Leave / london_data_2["Votes Cast"]


# In[119]:


london_data_2.Leave = london_data_2.Leave*100
london_data_2.Remain = london_data_2.Remain*100


# In[120]:


london_data_2.head()


# In[121]:


# Dropping the 'Borough' column, as it has the same values of 'area'
london_data_2 = london_data_2.drop(columns = "Borough")


# In[122]:


# Export the clean dataset to a csv file
london_data_2.to_csv('london_data_2.csv', index=False)


# 
# 

# ### LONDON_DATA_3 (concatenating other data)

# In[124]:


pd.set_option('display.max_columns', 120)

new_london = pd.read_csv("london-borough-profiles-2016 Data set.csv")
new_london.drop(labels = 0, inplace = True)
new_london = new_london.reset_index(drop=True)

# Merging 'london_data_2' and this you data ('new_london')
london_data_3 = pd.concat([london_data_2, new_london], axis = 1)


# In[125]:


london_data_3.head(3)


# In[126]:


len(london_data_3.columns)


# In[127]:


london_data_3.drop(columns = london_data_3.loc[:, "% of second largest migrant population (2011)":"Third largest migrant population arrived during 2014/15"],
                   inplace = True)


# In[128]:


london_data_3.drop(columns = london_data_3.loc[:, "Code":"Population density (per hectare) 2016"],
                   inplace = True)


# In[129]:


london_data_3.drop(columns = london_data_3.loc[:, "Proportion of population aged 0-15, 2016":"Proportion of population aged 65 and over, 2016"],
                   inplace = True)


# In[130]:


london_data_3.drop(columns = ["Net natural change (2014)", "% of largest migrant population (2011)"], inplace = True)


# In[131]:


london_data_3.drop(columns = ["Male employment rate (2015)", "Female employment rate (2015)",
                             "Proportion of the working-age population who claim out-of-work benefits (%) (Aug-2015)"],
                              inplace = True)


# In[132]:


london_data_3.drop(columns = london_data_3.loc[:, "Gross Annual Pay, (2015)":"% of employment that is in public sector (2014)"],
                   inplace = True)


# In[133]:


london_data_3.drop(columns = ["Number of active businesses, 2014", "Two-year business survival rates (started in 2012)",
                             "Fires per thousand population (2014)", "Ambulance incidents per hundred population (2014)",
                             "Average Band D Council Tax charge (£), 2015/16", "New Homes (net) 2014/15 (provisional)",
                             "Being bought with mortgage or loan, (2014) %", "Rented from Local Authority or Housing Association, (2014) %",
                             "Rented from Private landlord, (2014) %", "% of area that is Greenspace, 2005",
                             "Number of cars, (2011 Census)", "% of adults who cycle at least once per month, 2013/14",
                             "Achievement of 5 or more A*- C grades at GCSE or equivalent including English and Maths, 2013/14",
                             "Rates of Children Looked After (2015)"],
                              inplace = True)


# In[134]:


london_data_3.drop(columns = london_data_3.loc[:, "Male life expectancy, (2012-14)":"Worthwhileness score 2011-14 (out of 10)"],
                   inplace = True)


# In[135]:


london_data_3.drop(columns = ["People aged 17+ with diabetes (%)", "Mortality rate from causes considered preventable 2012/14",
                             "% children living in out-of-work households (2014)"],
                              inplace = True)


# In[136]:


london_data_3.drop(columns = london_data_3.loc[:, "Proportion of seats won by Conservatives in 2014 election":"Turnout at 2014 local elections"],
                   inplace = True)


# In[137]:


london_data_3.head(3)


# In[138]:


len(london_data_3)


# In[139]:


# Export the clean dataset to a csv file
london_data_3.to_csv('london_data_3.csv', index=False)


# 
# 

# ### LONDON_DATA_4 (concatenating other data)

# In[140]:


london_data_4 = london_data_3.copy()


# In[141]:


london_data_4.head(3)


# In[142]:


# Subsistuting the dots ('.') with NaN
london_data_4.replace(to_replace = ".", value = np.nan, inplace = True)


# In[143]:


london_data_4.head(3)


# In[144]:


# Deleting rows regarding summary London's data
london_data_4.drop(index = range(33, 39), inplace = True)


# In[145]:


london_data_4


# In[146]:


london_data_4.isnull().sum()


# In[147]:


# Select rows with at least one NaN value
london_data_4[london_data_4.isna().any(axis=1)]


# In[148]:


london_data_4.info()


# In[149]:


# Adjusting types
london_data_4["Net internal migration (2014)"] = london_data_4["Net internal migration (2014)"].astype(int)

london_data_4["Net international migration (2014)"] = london_data_4["Net international migration (2014)"].astype(int)

london_data_4["% of resident population born abroad (2014)"] = london_data_4["% of resident population born abroad (2014)"].astype(float)

london_data_4["Unemployment rate (2015)"] = london_data_4["Unemployment rate (2015)"].astype(float)

london_data_4["Youth Unemployment (claimant) rate 18-24 (Dec-14)"] = london_data_4["Youth Unemployment (claimant) rate 18-24 (Dec-14)"].astype(float)

london_data_4["Proportion of 16-18 year olds who are NEET (%) (2014)"] = london_data_4["Proportion of 16-18 year olds who are NEET (%) (2014)"].astype(float)

london_data_4["% working-age with a disability (2015)"] = london_data_4["% working-age with a disability (2015)"].astype(float)

london_data_4["Proportion of working age people with no qualifications (%) 2015"] = london_data_4["Proportion of working age people with no qualifications (%) 2015"].astype(float)

london_data_4["Proportion of working age with degree or equivalent and above (%) 2015"] = london_data_4["Proportion of working age with degree or equivalent and above (%) 2015"].astype(float)

london_data_4["Crime rates per thousand population 2014/15"] = london_data_4["Crime rates per thousand population 2014/15"].astype(float)

london_data_4["Homes Owned outright, (2014) %"] = london_data_4["Homes Owned outright, (2014) %"].astype(float)


# In[150]:


london_data_4["Median House Price, 2014"] = london_data_4["Median House Price, 2014"].str.replace(',', '')

london_data_4["Median House Price, 2014"] = london_data_4["Median House Price, 2014"].astype(int)


# In[151]:


london_data_4["Total carbon emissions (2013)"] = london_data_4["Total carbon emissions (2013)"].str.replace(',', '')

london_data_4["Total carbon emissions (2013)"] = london_data_4["Total carbon emissions (2013)"].astype(float)
london_data_4["Household Waste Recycling Rate, 2014/15"] = london_data_4["Household Waste Recycling Rate, 2014/15"].astype(float)
london_data_4["Average Public Transport Accessibility score, 2014"] = london_data_4["Average Public Transport Accessibility score, 2014"].astype(float)
london_data_4["% of pupils whose first language is not English (2015)"] = london_data_4["% of pupils whose first language is not English (2015)"].astype(float)
london_data_4["Childhood Obesity Prevalance (%) 2014/15"] = london_data_4["Childhood Obesity Prevalance (%) 2014/15"].astype(float)
london_data_4["Political control in council"] = london_data_4["Political control in council"].astype("category")


# In[152]:


london_data_4.info()


# In[153]:


# Export the clean dataset to a csv file
london_data_4.to_csv('london_data_4.csv', index=False)


# In[ ]:




