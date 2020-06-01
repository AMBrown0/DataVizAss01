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
#null_rows=data_df[data_df.isnull().any(axis=1)]
# Fill stringency data with teh last known values 
stringencyindex_legacy_df=stringencyindex_legacy_df.ffill(axis=1)



#==============================Part 2 - Question 3 =================================

country_list=['China','South Korea','United States','France','United Kingdom','Italy']
#country_list=['United Kingdom']
#country_list=['South Korea']


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
ax = plt.axes()
ax.set_title('Average new weekly confirmed cases ')
sns.heatmap(values_of_largest_ten)

#==============================Part 2 - Question 4 =================================