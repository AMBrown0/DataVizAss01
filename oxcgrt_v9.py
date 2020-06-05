# -*- coding: utf-8 -*-
"""
Created on Mon May 11 00:59:29 2020

@author: Meso
"""

# =============================================================================
# 1. Create a plot that shows the number of medals won by the UK team between 1896 and 2016.
# 2. Repeat Q1 but consider the following:
# a) showing the numbers of different type of medals (Gold, Silver, and Bronze)
# b) Showing the number of medals won by Males and Females separately.
# =============================================================================
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from numpy import median, mean
import json, urllib.request
import sys
from pathlib import Path
from datetime import datetime

def get_data_from_cell(cell,key):

    try:
        data=cell[key]
        #print("Data OK=%s")
        #print("Data OK=%s" %data)
            
        if data is None:
            print("%s:%s[%s]=None" % (cell['country_code'],cell['date_value'],key))
            return np.nan
        else:
            print("%s:%s[%s]=%s" % (cell['country_code'],cell,cell['date_value'],key))
    except:    
        #print("%s:%s[%s]=NAN" % (cell['country_code'],cell['date_value'],key))
        return np.nan
    #print("<%s>=<%s>=%s" % (cell,key,data))
    return data
    
def get_subset_by_key(data_df,key):
    #print("data_df=%s" % data_df)
    #print("key=%s" % key)
    #update_df=data_df.applymap(get_data_from_cell,args=(key))
    updated_df=data_df.applymap(lambda x: get_data_from_cell(x,key))
    #update_df=data_df.apply(lambda column: )
    return updated_df
    
#%matplotlib inline

dataFolder=Path(r'.')
filename="OxCGRT_summary_updated.xlsx"
dataFile= dataFolder / filename


start_date="2020-01-01"
end_date="2020-05-10"

#==============================Part 1 - Question 1 & 2=================================
url='https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/' + start_date + '/' + end_date
print(url)
data = urllib.request.urlopen(url).read()

# load the data (will be saved as dictionary in output)
output = json.loads(data)
#print(output)

#Read in the data portion of the json information 

data_dict=output["data"]
data_df=pd.DataFrame(data_dict)
data_frame_sorted=data_df.sort_index(axis=0)


writer = pd.ExcelWriter(filename, engine='xlsxwriter')

confirmedcases_df=get_subset_by_key(data_frame_sorted,'confirmed')
#Liner interolate missing values and fill in remaining NaN with Zero
confirmedcases_df=confirmedcases_df.interpolate(method='linear', limit_direction='forward', axis=1)
confirmedcases_df.columns=pd.to_datetime(confirmedcases_df.columns).strftime("%d%b%Y")
confirmedcases_df=confirmedcases_df.fillna(0)
confirmedcases_df.to_excel(writer, sheet_name='confirmedcases')


confirmeddeaths_df=get_subset_by_key(data_frame_sorted,'deaths')
#Liner interolate missing values and fill in remaining NaN with Zero
confirmeddeaths_df=confirmeddeaths_df.interpolate(method='linear', limit_direction='forward', axis=1)
confirmeddeaths_df=confirmeddeaths_df.fillna(0)
confirmeddeaths_df.columns=pd.to_datetime(confirmeddeaths_df.columns).strftime("%d%b%Y")
confirmeddeaths_df.to_excel(writer, sheet_name='confirmeddeaths')



stringencyindex_legacy_df=get_subset_by_key(data_frame_sorted,'stringency_legacy')
#stringencyindex_legacy_df=stringencyindex_legacy_df.interpolate(method='linear', limit_direction='forward', axis=1)
#backup=stringencyindex_legacy_df
#stringencyindex_legacy_df=stringencyindex_legacy_df.fillna(0)
stringencyindex_legacy_df.columns=pd.to_datetime(stringencyindex_legacy_df.columns).strftime("%d%b%Y")
stringencyindex_legacy_df.to_excel(writer, sheet_name='stringencyindex_legacy')

writer.save()

        
