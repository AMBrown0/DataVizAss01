# -*- coding: utf-8 -*-
"""
Created on Mon May 11 00:59:29 2020

@author: 
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from numpy import median, mean
import json, urllib.request
import sys
from pathlib import Path
from datetime import datetime
import matplotlib.dates as mdate
import plotly.graph_objects as go


#%matplotlib inline

# # open a request to read the data
# data = urllib.request.urlopen("https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/actions/GBR/2020-04-06").read()
# # load the data (will be saved as dictionary in output)
# output = json.loads(data)


#==============================Part 1 - Question 1b =================================
dataFolder=Path(r'.')
filename="OxCGRT_summary.xlsx"
dataFile= dataFolder / filename
#sheetname='stringencyindex_legacy'
stringencyindex_legacy_df = pd.read_excel (dataFile,sheet_name='stringencyindex_legacy')
confirmedcases_df = pd.read_excel (dataFile,sheet_name='confirmedcases')
confirmeddeaths_df = pd.read_excel (dataFile,sheet_name='confirmeddeaths')
#null_rows=data_df[data_df.isnull().any(axis=1)]
# Fill stringency data with teh last known values 
stringencyindex_legacy_df=stringencyindex_legacy_df.ffill(axis=1)



#==============================Part 2 - Question 3 =================================

country_list=['China','South Korea','United States','France','United Kingdom','Italy']
#country_list=['United Kingdom']
#country_list=['South Korea']

#fig = plt.figure(figsize=(18,10), dpi=1600)
for country in country_list:
    stringencyindex_legacy_c_df=stringencyindex_legacy_df[stringencyindex_legacy_df['CountryName'] == country]
    confirmedcases_c_df=confirmedcases_df[confirmedcases_df['CountryName'] == country]
    #country=confirmedcases_df.iloc[:,0].iloc[0]
    s_t_df=stringencyindex_legacy_c_df.transpose()
    c_t_df=confirmedcases_c_df.transpose()
    X=c_t_f_df=c_t_df.iloc[2:,:]
    X.set_axis(['confirmedcases'],axis=1,inplace=True)
    Y=s_t_df.iloc[2:,:]
    Y.set_axis(['stringency'],axis=1,inplace=True)
    Y.rename(index={0:"stringency"})
    result=pd.concat([X,Y], axis=1)
    result.set_index("confirmedcases",inplace=True) 
    result.sort_index(inplace=True)
    plt.title('Comparison of stringency of COVID-19 repsonse in six countries') 
    plt.xlabel("Reported number of cases of COVID-19")
    plt.ylabel("Stringency index")
    plt.plot(result,label=country)
    plt.xscale("log")
    
    plt.ylim(0, 100)
    plt.xlim(1, 1000000)


plt.legend()
plt.show()

#Convert index to date  time for grouping


#tart_date='2020-03-02'
#tart_date='2020-05-10'


#==============================Part 2 - Question 4 =================================
#X=confirmedcases_df.transpose()
cc_df=confirmedcases_df.transpose()
country_list=confirmedcases_df['CountryName']
cc_df=cc_df.iloc[2:,]


#Calcaulte the increase from the previous day select date and average per week
cc_df.index = pd.to_datetime(cc_df.index)
cc_df=cc_df.diff(axis=0)
avg_df=cc_df.loc['2020-03-02':'2020-05-10']
gr = avg_df.groupby(pd.Grouper(level=0,freq='W'))
gr_mean =pd.DataFrame([ g.mean() for i,g in gr ])

#Create a list of the countries with largest values
largest_ten=gr_mean.max().nlargest(10)
largest_ten_country_list=country_list[largest_ten.index]

#Generate the data to plot
values_of_largest_ten=gr_mean[largest_ten_country_list.index]
values_of_largest_ten=values_of_largest_ten.transpose()
values_of_largest_ten.index=largest_ten_country_list
column_names=(pd.date_range(start='2020-03-02', periods=10, freq='W-MON')).date
values_of_largest_ten.columns=column_names
values_of_largest_ten.index.name="Country Name"
fig = plt.figure(figsize=(18,10), dpi=1600)
ax = plt.axes()
ax.set_title('Average new weekly confirmed cases ')
sns.heatmap(values_of_largest_ten)
plt.show()
#==============================Part 2 - Question 5 =================================
cc_may1_df=confirmedcases_df[['CountryName','01may2020']]
cc_may1_us=cc_may1_df[cc_may1_df['CountryName'] == 'United States']['01may2020']
cc_may1_rest=float(cc_may1_df.sum()) - float(cc_may1_us)
cc_plt=[cc_may1_us,cc_may1_rest]

cd_may1_df=confirmeddeaths_df[['CountryName','01may2020']]
cd_may1_us=cd_may1_df[cd_may1_df['CountryName'] == 'United States']['01may2020']
cd_may1_rest=float(cd_may1_df.sum()) - float(cd_may1_us)
cd_plt=[cd_may1_us,cd_may1_rest]
pop_us=328000000
pop_world=7800000000


#fig = plt.figure(figsize=(18,7), dpi=1200)
fig.suptitle("US COVID-19 vs Rest of World", fontsize=16)
ax1 = plt.subplot(131)
ax2 = plt.subplot(132)
ax3 = plt.subplot(133)

percentage = [pop_us,pop_world]
labels= ['United States','Other']


ax1 = plt.subplot2grid((1,3),(0,0))
plt.title('Population')
explodes = (0.1, 0)
plt.pie(percentage, explode=explodes, labels=labels, autopct='%1.0f%%',startangle=90,counterclock=False)

ax1 = plt.subplot2grid((1,3),(0,1))
plt.title('Confirmed Cases')
explodes = (0.1, 0)
plt.pie(cc_plt, explode=explodes, labels=labels, autopct='%1.0f%%',startangle=90,counterclock=False)

ax1 = plt.subplot2grid((1,3),(0,2))
plt.title('Deaths')
explodes = (0.1, 0)
plt.pie(cd_plt, explode=explodes, labels=labels, autopct='%1.0f%%',startangle=90,counterclock=False)

plt.show()


# to explode the 4th slice

# autopct: control the labels inside the wedges
#plt.pie(percentage, explode=explodes, labels=labels, autopct='%1.0f%%')
#==============================Part 2 - Question 6 =================================
c_uk_df=confirmeddeaths_df[confirmeddeaths_df['CountryName'] == 'United Kingdom']
cc_uk_df=c_uk_df.transpose()
cc_uk_df=cc_uk_df.iloc[2:,]
start_date='2020-03-07'
end_date='2020-05-10'
#x_axis=(pd.date_range(start=start_date, end=end_date, freq='W-SUN')).date

#Calcaulte the increase from the previous day select date and average per week
cc_uk_df.index = pd.to_datetime(cc_uk_df.index)
#cc_uk_df=cc_uk_df.diff(axis=0)
ax=plt.plot(cc_uk_df)
#ax.yaxis.set_major_formatter(mticker.ScalarFormatter())
#ax.get_xaxis().get_major_formatter().set_scientific(False)
#locator = mdate.YearLocator()
locator = mdate.DayLocator(interval=14)
plt.gca().xaxis.set_major_locator(locator)
plt.gcf().autofmt_xdate()
plt.yscale('log')
plt.xticks(rotation=90)
    
plt.title('Confirmed deaths UK betweek 7th March and 10th May 2020') 
plt.xlabel("Date")
plt.ylabel("Confirmed Deaths")
#plt.ticklabel_format(style='plain')
plt.show()


#==============================Part 2 - Question 7 =================================
country_list=['United Kingdom','Spain','Italy','France','United States']
#country_list=['United Kingdom']
#country_list=['South Korea']

#fig = plt.figure(figsize=(18,10), dpi=1600)
#ndc_df=confirmedcases_df[confirmedcases_df['CountryName'] in country_list]
ndc_df=confirmedcases_df[confirmedcases_df['CountryName'].isin(country_list)]
ndc_df=ndc_df.transpose()
ndc_df.columns=ndc_df.loc['CountryName']
ndc_df=ndc_df.iloc[2:,]
start_date='2020-03-01'
end_date='2020-05-01'
ndc_df.index = pd.to_datetime(ndc_df.index)
ndc_df=ndc_df.loc[start_date:end_date]
ndc_df=ndc_df.diff(axis=0)
ndc_df.dropna(inplace=True)

#ax=plt.plot(ndc_df)
#plt.xticks(rotation=90)

fig, ax = plt.subplots()
X=ndc_df.index
Y_all = pd.DataFrame([ ndc_df[c] for c in country_list ])
#Y_all=ndc_df.transpose()
# Y1=list(ndc_df['Spain'])
# Y2=list(ndc_df['Italy'])
# Y3=list(ndc_df['United Kingdom'])
#A=pd.DataFrame([Y1,Y2,Y3])
#A=list(ndc_df[country_list])
ax.stackplot(X,Y_all)
ax.legend(Y_all.index,loc='upper left')
plt.xticks(rotation=90)
plt.show()

# ndc_df=confirmedcases_df[confirmedcases_df['CountryName'].isin(country_list)]
# ndc_df=ndc_df.set_index('CountryName')
# ndc_df=ndc_df.iloc[:,1:]

# plt.fill_between(X, Y1,
#                  color="skyblue", alpha=0.4)
# plt.fill_between(X, Y2,
#                  color="slateblue", alpha=0.4)

# fig = go.Figure()
# fig.add_trace(go.Scatter(x=X, y=Y1, fill='tozeroy')) # fill down to xaxis
# fig.add_trace(go.Scatter(x=X, y=Y2, fill='tonexty')) # fill to trace0 y

# fig.show()
# plt.show()
# #for country in country_list:
#     stringencyindex_legacy_c_df=stringencyindex_legacy_df[stringencyindex_legacy_df['CountryName'] == country]
#     confirmedcases_c_df=confirmedcases_df[confirmedcases_df['CountryName'] == country]
#     #country=confirmedcases_df.iloc[:,0].iloc[0]
#     s_t_df=stringencyindex_legacy_c_df.transpose()
#     c_t_df=confirmedcases_c_df.transpose()
#     X=c_t_f_df=c_t_df.iloc[2:,:]
#     X.set_axis(['confirmedcases'],axis=1,inplace=True)
#     Y=s_t_df.iloc[2:,:]
#     Y.set_axis(['stringency'],axis=1,inplace=True)
#     Y.rename(index={0:"stringency"})
#     result=pd.concat([X,Y], axis=1)
#     result.set_index("confirmedcases",inplace=True) 
#     result.sort_index(inplace=True)
#     plt.title('Comparison of stringency of COVID-19 repsonse in six countries') 
#     plt.xlabel("Reported number of cases of COVID-19")
#     plt.ylabel("Stringency index")
#     plt.plot(result,label=country)
#     plt.xscale("log")
    
#     plt.ylim(0, 100)
#     plt.xlim(1, 1000000)


# plt.legend()
# plt.show()