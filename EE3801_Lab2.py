#!/usr/bin/env python
# coding: utf-8

# # Qn 1(a)

# In[466]:


import pandas as pd


# In[467]:


fao_df = pd.read_csv("FAO.csv", encoding="unicode_escape")


# In[468]:


fao_df.head() # see the dataset 


# In[469]:


# getting the names of areas, without duplicates
areas = list(fao_df["Area"].unique())


# In[470]:


# getting the names of all columns
columns = list(fao_df.columns)
# do a list slicing to get only the years and nothing else
years = columns[3:]


# In[471]:


# create an empty list (food_data_by_countries) to append all the dictionaries 
food_data_by_countries = []
for area in areas:
    location = {}
    for year in years:
        filt = (fao_df["Area"] == area)
        total_production = fao_df.loc[filt][year].sum()
        location[year] = [total_production]
    food_data_by_countries.append(location)

# create an empty dataframe to append all the other dataframes 
totalProductionByEachCountryEachYear = pd.DataFrame()

# start appending the dataframes!
for country_dict in food_data_by_countries:
    individual_df = pd.DataFrame(country_dict)
    totalProductionByEachCountryEachYear = totalProductionByEachCountryEachYear.append(individual_df)

# naming the rows by countries
totalProductionByEachCountryEachYear.index = areas
print("Qn 1(a):")
print("\n")
totalProductionByEachCountryEachYear


# In[472]:


# saving the newly created dataframe as a new csv file 
totalProductionByEachCountryEachYear.to_csv("total_production_by_country_each_year.csv")


# # Q1(b)

# In[473]:


# getting a list of the total productions by country
overall_production = []
for area in areas:
    total_production = totalProductionByEachCountryEachYear.loc[area].sum()
    overall_production.append([total_production])


# In[474]:


# creating a dictionary to transform it into a dataframe 
overall_production_dict = dict(zip(areas, overall_production))


# In[475]:


# converting the dictionay into a dataframe 
overall_production_df = pd.DataFrame(overall_production_dict)
overall_production_df = overall_production_df.transpose()

# give the columns a nice name
overall_production_df = overall_production_df.rename(columns={0: "OPC"})
overall_production_df.index.name = "Countries"
print("Qn1(b):")
print("\n")
overall_production_df


# # Q1(c)

# In[476]:


# APPYPC = Overall production by a specific country / total number of years
total_number_of_years = len(years)


# In[477]:


average_production_by_year = []
for area in areas:
    average = (overall_production_df.loc[area]["OPC"]/total_number_of_years)
    average_production_by_year.append([average])


# In[478]:


# creating a dictionary to transform it into a dataframe 
APPYPC_dict = dict(zip(areas, average_production_by_year))


# In[479]:


# converting the dictionay into a dataframe 
APPYPC_df = pd.DataFrame(APPYPC_dict)
APPYPC_df = APPYPC_df.transpose()

# give the columns a nice name
APPYPC_df = APPYPC_df.rename(columns={0: "APPYPC"})
APPYPC_df.index.name = "Countries"
print("Qn1(c):")
print("\n")
APPYPC_df


# # 1(d)

# In[480]:


# GAPPC = Overall production by a specific country / Overall production by all the countries
overall_production_by_all_countries = overall_production_df["OPC"].sum()


# In[481]:


# getting a list of GAPPC by country
global_average_production = []
for area in areas:
    global_average = (overall_production_df.loc[area]["OPC"] / overall_production_by_all_countries)
    global_average_production.append([global_average])


# In[482]:


# creating a dictionary to transform it into a dataframe 
GAPPC_dict = dict(zip(areas, global_average_production))


# In[483]:


# converting the dictionay into a dataframe 
GAPPC_df = pd.DataFrame(GAPPC_dict)
GAPPC_df = GAPPC_df.transpose()

# give the columns a nice name
GAPPC_df = GAPPC_df.rename(columns={0: "GAPPC"})
GAPPC_df.index.name = "Countries"
print("Qn1(d):")
print("\n")
GAPPC_df


# # For Part (b) to (d), store your result as a DF and display only the top 3 and bottom 3 results from this new DF

# In[484]:


countries_food_data = overall_production_df
countries_food_data["APPYPC"] = APPYPC_df["APPYPC"]
countries_food_data["GAPPC"] = GAPPC_df["GAPPC"]


# In[485]:


# getting the top 3 and bottom 3 data
top3Data = countries_food_data.head(3)
bottom3Data = countries_food_data.tail(3)
topThreeAndBottomThreeData = pd.concat([top3Data, bottom3Data])
print("Qn 1(b)-(d): The top 3 and bottom 3 results are ")
print("\n")
topThreeAndBottomThreeData


# # Q2

# In[486]:


from matplotlib import pyplot as plt
import numpy as np


# In[487]:


fig =  plt.figure(figsize=(45, 4))
ax = fig.add_subplot(111)
APPYPC_df = APPYPC_df.sort_values("APPYPC", ascending=False)
ax.bar(APPYPC_df.index, APPYPC_df["APPYPC"])
ax.set_xticklabels(APPYPC_df.index, rotation=60, horizontalalignment="right", fontsize="12")

ax.set_title("Average Production Per Year by Country", fontsize=24)
ax.set_ylabel("Average Production", fontsize=22)
ax.set_xlabel("Countries", fontsize=22)

print("Qn2(a):")
print("\n")
plt.show

# From the barchart, we can observe that the countries with the highest and lowest productions are
# China, mainland and Saint Kitts and Nevis respectively. 


# # Q3

# In[488]:


# For this particular problem, I categorize countries whose GAPPC values are less than 1% into "Others"

import itertools
plt.style.use('ggplot')

t = GAPPC_df.sort_values(by=['GAPPC'],ascending=False)
temp = GAPPC_df.to_dict('dict')

newdic={}
for key, group in itertools.groupby(temp['GAPPC'], lambda k: 'Others' if (temp['GAPPC'][k]<.01) else k):
     newdic[key] = sum([temp['GAPPC'][k] for k in list(group)])   

labels = newdic.keys()
sizes = newdic.values()

tot = 0.0
for i in sizes:
    tot += i
newdic['Others'] = 1.02 - tot

fig, ax = plt.subplots(figsize=(12, 10))
ax.pie(sizes, labels=labels, autopct='%1.2f%%', explode=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0), startangle=90)
ax.axis('equal')
plt.tight_layout()

print("Qn3:")
print("\n")
plt.show()


# # Q4

# In[489]:


# set the filter to get countries whose avergae production is more than 5%
filt = (countries_food_data["GAPPC"] > 0.05)


# In[490]:


GAPPC_column = countries_food_data["GAPPC"]


# In[491]:


# get the countries whose average production is more than 5%
countries_averageProduction_more_than_fivePercent = list(GAPPC_column.loc[filt].index)


# In[492]:


# get the respective percentages of these countries
percentages_of_countries_averageProduction_more_than_fivePercent = list(GAPPC_column.loc[filt])


# In[493]:


# find the percentage of "others"
total_percent_of_countries_more_than_5percent = 0
for i in range(len(percentages_of_countries_averageProduction_more_than_fivePercent)):
    total_percent_of_countries_more_than_5percent += percentages_of_countries_averageProduction_more_than_fivePercent[i]
percent_of_others = 1 - total_percent_of_countries_more_than_5percent


# In[494]:


# create a list of all percentages with all countries
percentages_of_countries_averageProduction_more_than_fivePercent.append(percent_of_others)


# In[495]:


# finally, plotting the pie chart...

labels = "China, mainland", "India", "United States of America", "Others"
sizes = list(map(lambda n: n*100, percentages_of_countries_averageProduction_more_than_fivePercent))
explode = (0.1, 0.1, 0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct="%1.1f%%", shadow=True, startangle=90)
ax1.axis("equal")
plt.title("GAPPC whose average production is more than 5%")
print("Qn4:")
print("\n")
plt.show()


# # Q5(a)

# In[496]:


# setting the filter to get ONLY honey from fao_df
filt = (fao_df["Item"] == "Honey")

# getting honey_only_df
honey_only_df = fao_df.loc[filt]

# construct a total column which computes the total honey production from 2010 to 2013
honey_only_df["Total"] = honey_only_df["Y2010"] + honey_only_df["Y2011"] + honey_only_df["Y2012"] + honey_only_df["Y2013"]

# if the honey production for a particular country is zero, drop it!
honey_df = honey_only_df.drop(honey_only_df[(honey_only_df["Total"] == 0)].index)

# construct a new dataframe call honey_df which consists of the area, Y2010 - Y2013
honey_df = honey_df[["Area", "Y2010", "Y2011", "Y2012", "Y2013"]]


# In[497]:


# getting the top three items from honey_df
topThreeItems = honey_df.head(3)


# In[498]:


# getting the bottom three items from honey_df
bottomThreeItems = honey_df.tail(3)


# In[499]:


# merge the two dataframes above into one and display it 
topThreeAndBottomThreeDf = topThreeItems.append(bottomThreeItems)
print("Qn5(a):")
print("\n")
topThreeAndBottomThreeDf


# # 5(b)

# In[500]:


# total_honey_production_between_2010and2013 = 
honey_df["Total"] = honey_df["Y2010"] + honey_df["Y2011"] + honey_df["Y2012"] + honey_df["Y2013"]


# In[501]:


# construct a new_df which consists of only the "area" and "total" columns
total_honey_production_between_2010and2013_df = honey_df[["Area", "Total"]]


# In[502]:


# getting and printing the overall honey production (global production)
overall_honey_production_globally = total_honey_production_between_2010and2013_df["Total"].sum()
print("Qn5(b), part 1:")
print(f'The overall honey production globally is {overall_honey_production_globally}')
# overall_honey_production_globally


# In[503]:


# appending the total_honey_production_between_2010and2013_df with the honey dataframe and saving it as a csv file
# the appended version of the dataframe is already done above, hence, we only left with converting in into a csv file
honey_df.to_csv("honey_production_from_year_2010_to_2013.csv", index=False)


# In[504]:


# printing the top three and bottom three daatsetsfrom the honey_df
topThreeHoneyData = honey_df.head(3)
bottomThreeHoneyData = honey_df.tail(3)
topThreeAndBottomThreeDataFromHoneyDF = topThreeHoneyData.append(bottomThreeHoneyData)
print("Qn5(b):")
print("\n")
topThreeAndBottomThreeDataFromHoneyDF


# # 5(c)

# In[561]:


# get the honey production of all countries from 2010 to 2013
honey_from_all_countries_from_2010_to_2013 = honey_only_df[["Area", "Y2010", "Y2011", "Y2012", "Y2013"]]


# In[562]:


# getting the average honey production for each country
honey_from_all_countries_from_2010_to_2013["average"] = (honey_from_all_countries_from_2010_to_2013["Y2010"] + honey_from_all_countries_from_2010_to_2013["Y2011"] + honey_from_all_countries_from_2010_to_2013["Y2012"] + honey_from_all_countries_from_2010_to_2013["Y2013"]) / 4


# In[563]:


total_average = honey_from_all_countries_from_2010_to_2013["average"].sum()


# In[564]:


five_percent_of_total_average = 0.05 * total_average


# In[568]:


filt = (honey_from_all_countries_from_2010_to_2013["average"] > five_percent_of_total_average)
more_than_five_percent = honey_from_all_countries_from_2010_to_2013.loc[filt]


# In[583]:


# plotting the pie chart
labels = 'China, mainland', 'Germany', 'Turkey', 'United States of America', "others"
sizes = list(more_than_five_percent["average"])
sizes = list(map(lambda x: (x/total_average)*100, sizes))

# get the percenatge for "others"
total = 0
for i in range(len(sizes)):
    total += sizes[i]
left = 100 - total

sizes.append(left)

explode = (0.1, 0.1, 0.1, 0.1, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.title("Countries whose average production is > 5% of global production from 2010 to 2013")
print("Qn5(c):")
print("\n")
plt.show()


# # Q6(a)

# In[445]:


import re
# getting all the Malaysia datasets from fao_df
filt = fao_df["Area"] == "Malaysia"
malaysia_df = fao_df.loc[filt]


# In[446]:


# filter out the sugar items for Food element
filt_food = (fao_df["Element"] == "Food") & (fao_df["Item"].str.contains("Sugar", flags=re.IGNORECASE))
malaysia_sugar_Food = malaysia_df.loc[filt_food]

# getting only for years between 2010 and 2013
malaysia_sugar_Food_between_2010And2013 = malaysia_sugar_Food[["Area", "Element", "Y2010", "Y2011", "Y2012", "Y2013"]]
malaysia_sugar_Food_between_2010And2013

# getting the total sugar production per year for malaysia (Food)
malaysia_sugar_Food_2010 = malaysia_sugar_Food_between_2010And2013["Y2010"].sum()
malaysia_sugar_Food_2011 = malaysia_sugar_Food_between_2010And2013["Y2011"].sum()
malaysia_sugar_Food_2012 = malaysia_sugar_Food_between_2010And2013["Y2012"].sum()
malaysia_sugar_Food_2013 = malaysia_sugar_Food_between_2010And2013["Y2013"].sum()


# In[447]:


# filter out the sugar items for Feed element
filt_feed = (fao_df["Element"] == "Feed") & (fao_df["Item"].str.contains("Sugar", flags=re.IGNORECASE))
malaysia_sugar_Feed = malaysia_df.loc[filt_feed]

# getting only for years between 2010 and 2013
malaysia_sugar_Feed_between_2010And2013 = malaysia_sugar_Feed[["Area", "Element", "Y2010", "Y2011", "Y2012", "Y2013"]]
malaysia_sugar_Feed_between_2010And2013

# getting the total sugar production per year for malaysia (Feed)
malaysia_sugar_Feed_2010 = malaysia_sugar_Feed_between_2010And2013["Y2010"].sum()
malaysia_sugar_Feed_2011 = malaysia_sugar_Feed_between_2010And2013["Y2011"].sum()
malaysia_sugar_Feed_2012 = malaysia_sugar_Feed_between_2010And2013["Y2012"].sum()
malaysia_sugar_Feed_2013 = malaysia_sugar_Feed_between_2010And2013["Y2013"].sum()


# In[448]:


# creating a dictionary to convert it to dataframe
malaysia_sugar = {"Country": ["Malaysia", "Malaysia"], "Food Type": ["Food", "Feed"], "2010": [malaysia_sugar_Food_2010, malaysia_sugar_Feed_2010], "2011": [malaysia_sugar_Food_2011, malaysia_sugar_Feed_2011], "2012": [malaysia_sugar_Food_2012, malaysia_sugar_Feed_2012], "2013": [malaysia_sugar_Food_2013, malaysia_sugar_Feed_2013]}


# In[449]:


# getting the dataframe for malaysia sugar production
malaysia_sugar_df = pd.DataFrame(malaysia_sugar)
print("Q6(a), Malayisa sugar production:")
print("\n")
malaysia_sugar_df


# In[450]:


# getting all the France datasets from fao_df
filt = fao_df["Area"] == "France"
france_df = fao_df.loc[filt]


# In[451]:


# filter out the sugar items for Food element
filt_food = (fao_df["Element"] == "Food") & (fao_df["Item"].str.contains("Sugar", flags=re.IGNORECASE))
france_sugar_Food = france_df.loc[filt_food]

# getting only for years between 2010 and 2013
france_sugar_Food_between_2010And2013 = france_sugar_Food[["Area", "Element", "Y2010", "Y2011", "Y2012", "Y2013"]]
france_sugar_Food_between_2010And2013

# getting the total sugar production per year for malaysia (Food)
france_sugar_Food_2010 = france_sugar_Food_between_2010And2013["Y2010"].sum()
france_sugar_Food_2011 = france_sugar_Food_between_2010And2013["Y2011"].sum()
france_sugar_Food_2012 = france_sugar_Food_between_2010And2013["Y2012"].sum()
france_sugar_Food_2013 = france_sugar_Food_between_2010And2013["Y2013"].sum()


# In[452]:


# filter out the sugar items for Feed element
filt_feed = (fao_df["Element"] == "Feed") & (fao_df["Item"].str.contains("Sugar", flags=re.IGNORECASE))
france_sugar_Feed = france_df.loc[filt_feed]

# getting only for years between 2010 and 2013
france_sugar_Feed_between_2010And2013 = france_sugar_Feed[["Area", "Element", "Y2010", "Y2011", "Y2012", "Y2013"]]
france_sugar_Feed_between_2010And2013

# getting the total sugar production per year for malaysia (Feed)
france_sugar_Feed_2010 = france_sugar_Feed_between_2010And2013["Y2010"].sum()
france_sugar_Feed_2011 = france_sugar_Feed_between_2010And2013["Y2011"].sum()
france_sugar_Feed_2012 = france_sugar_Feed_between_2010And2013["Y2012"].sum()
france_sugar_Feed_2013 = france_sugar_Feed_between_2010And2013["Y2013"].sum()


# In[453]:


# creating a dictionary to convert it to dataframe
france_sugar = {"Country": ["France", "France"], "Food Type": ["Food", "Feed"], "2010": [france_sugar_Food_2010, france_sugar_Feed_2010], "2011": [france_sugar_Food_2011, france_sugar_Feed_2011], "2012": [france_sugar_Food_2012, france_sugar_Feed_2012], "2013": [france_sugar_Food_2013, france_sugar_Feed_2013]}


# In[454]:


# getting the dataframe for france sugar production
france_sugar_df = pd.DataFrame(france_sugar)
print("Qn6(a), France sugar production:")
print("\n")
france_sugar_df


# # 6(b)

# In[455]:


# mergeing the two dataframes into one and display it
sugar_production_by_MalaysiaAndFrance_between_2010And2013 = malaysia_sugar_df.append(france_sugar_df)
print("Qn6b:")
print("\n")
sugar_production_by_MalaysiaAndFrance_between_2010And2013.reset_index(drop=True)


# # 6(c)

# In[456]:


# constant x-axis for both plots - represents years from 2010 to 2013
x_axis = ["2010", "2011", '2012',"2013"]

# total sugar production (sugar + allied sugar products) in the respective years for Malaysia
malaysia_total_sugar_yaxis = [2424, 2459, 2573, 2615]
# plotting the line plot out
plt.plot(x_axis, malaysia_total_sugar_yaxis, label="Malaysia", marker="o")

# total sugar production (sugar + allied sugar products) in the respective years for France
france_total_sugar_yaxis = [4663, 4678, 4745, 4960]
# plotting the line plot out
plt.plot(x_axis, france_total_sugar_yaxis, label="France", marker="o")

# labeeling of the axes, and giving the plot a title 
plt.xlabel("Years", fontsize=12)
plt.ylabel("Sugar Production from 2010 t0 2013", fontsize=12)
plt.title("Trends over the years on the total sugarand allied sugar products produced.")
plt.legend()
plt.grid(True)
print("Qn6b:")
print("\n")
plt.show()


# # 6(d)

# In[457]:


import numpy as np
fig = plt.figure(figsize=(16, 14))

pltMalaysiaFood = fig.add_subplot(221)
pltMalaysiaFeed = fig.add_subplot(223)
pltFranceFood = fig.add_subplot(222)
pltFranceFeed = fig.add_subplot(224)

x = ["2010", "2011", "2012", "2013"]
y1 = [2362, 2411, 2541, 2587] # malaysia food
y2 = [62, 48, 32, 28] # malaysia feed
y3 = [4583, 4601, 4668, 4882] # france food
y4 = [80, 77, 77, 78] # france feed

# plotting for Malaysia (food)
pltMalaysiaFood.bar(x, y1, color="#e58e38", width=0.5)
pltMalaysiaFood.set_xlabel("Years", fontsize="15")
pltMalaysiaFood.set_ylabel("Sugar Production", fontsize="15")
pltMalaysiaFood.set_title("Msia's sugar products(Food) from 2010 - 2013", fontsize="18")

# plotting for ,Malaysia (feed)
pltMalaysiaFeed.bar(x, y2, color="#008fd5", width=0.5)
pltMalaysiaFeed.set_xlabel("Years", fontsize="15")
pltMalaysiaFeed.set_ylabel("Sugar Production", fontsize="15")
pltMalaysiaFeed.set_title("Msia's sugar product(Feed) from 2010 - 2013", fontsize="18")

# plotting for France (food)
pltFranceFood.bar(x, y3, color="#444444", width=0.5)
pltFranceFood.set_xlabel("Years", fontsize="15")
pltFranceFood.set_ylabel("Sugar Production", fontsize="15")
pltFranceFood.set_title("France's sugar product (Food) from 2010 - 2013", fontsize="18")

# plotting for France (feed)
pltFranceFeed.bar(x, y4, color="#007f67", width=0.5)
pltFranceFeed.set_xlabel("Years", fontsize="15")
pltFranceFeed.set_ylabel("Sugar Production", fontsize="15")
pltFranceFeed.set_title("France's sugar product(Feed) from 2010 - 2013", fontsize="18")

print("Qn6(d):")
print("\n")
plt.show()


# # 6(f)

# In[458]:


average_between_two_countries_in_2010 = ((2541 + 32) + (4668 + 77)) / 2
difference_between_two_countries_in_2010 = abs((2541 + 32) - (4668 + 77))
percentage_difference_between_the_two_countries_in_2012 = (difference_between_two_countries_in_2010 / average_between_two_countries_in_2010) * 100

print(f'Qn6(f): The percentage difference between Malaysia and France in 2010 is {percentage_difference_between_the_two_countries_in_2012}%')


# In[ ]:




