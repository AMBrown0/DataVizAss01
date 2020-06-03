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
        print("%s:%s[%s]=NAN" % (cell['country_code'],cell['date_value'],key))
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


#'https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/date-range/{YYYY-MM-DD}/{YYYY-MM-DD}''
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

        

#for contry, new_df in confirmedcases_df.groupby(level=0):
#for contry, new_df in confirmedcases_df.groupby(level=0):
#    print(new_df)

#for ind in confirmedcases_df.index:
#    print(ind)
#for date, new_df in confirmedcases_df.groupby(level=0):
#confirmeddeaths=get_subset_by_key(data_df,'deaths')
#stringencyindex_legacy=get_subset_by_key(data_df,'stringency')
# with open('file.txt', 'w') as file:
#      file.write(json.dumps(data_dict)) 

# # open a request to read the data
# data = urllib.request.urlopen("https://covidtrackerapi.bsg.ox.ac.uk/api/v2/stringency/actions/AND/2020-03-03").read()
# # load the data (will be saved as dictionary in output)
# output = json.loads(data)

# # let's see what is inside "stringencyData"
# sd=output["stringencyData"]
# for x in sd:
#     key=x
#     value=sd[key]
#     print("%s=%s" % (x,value))




# # show all columns in the console
# pd.set_option('display.max_columns', None)

# # download file 'athlete_events.csv' from Moodle on Kaggle 
# # read the dataset as a pandas DataFrame
# olympics = pd.read_csv('./data/athlete_events.csv')

# #1)
    
# olympics_win = olympics.dropna(subset=['Medal'])

# win_UK =olympics_win.query('NOC=="GBR"').Year.value_counts().sort_index()

# plt.plot(win_UK.index, win_UK.values, marker='o', markerfacecolor='darkgreen')

# plt.title("number of medals won by the UK team between 1896 and 2016")
# plt.xlabel('Year'); plt.ylabel('number of medals');

# # if you want to add  y values as labels to the points
# for x,y in zip(win_UK.index,win_UK.values):
#     lab = "{}".format(y)
#     plt.annotate(lab, (x,y),xytext=(x+2,y+10))
    

# # 2)
# #a)

# win_UK_medals=olympics_win.query('NOC=="GBR"').groupby(['Medal','Year'])['Medal'].count().rename("counts").reset_index()

# win_UK_medals.sort_values('Year',inplace=True)


# plt.plot(win_UK_medals.query('Medal=="Gold"').Year, win_UK_medals.query('Medal=="Gold"').counts, marker='o', markerfacecolor='Gold', color='Gold', linewidth=2, label="Gold")

# plt.plot(win_UK_medals.query('Medal=="Silver"').Year, win_UK_medals.query('Medal=="Silver"').counts, marker='*', markerfacecolor='Grey', color='Grey', linewidth=2, label="Silver")

# plt.plot(win_UK_medals.query('Medal=="Bronze"').Year, win_UK_medals.query('Medal=="Bronze"').counts, marker='D', markerfacecolor='black', color='black', linewidth=2, label="Bronze")

# plt.title("number of medals (Gold,Silver,Bronze) won by the UK team between 1896 and 2016")
# plt.xlabel('Year'); plt.ylabel('number of medals');
# plt.legend()



# #b)

# win_UK_F= olympics_win.query('NOC=="GBR" & Sex=="F"').Year.value_counts().reset_index()
# win_UK_F.rename(columns={"index":"Year","Year":"F_count"},inplace=True)

# win_UK_M= olympics_win.query('NOC=="GBR" & Sex=="M"').Year.value_counts().reset_index()
# win_UK_M.rename(columns={"index":"Year","Year":"M_count"},inplace=True)


# win_UK_all=win_UK_F.merge(win_UK_M,how='outer', on='Year').sort_values(by='Year')

# win_UK_all.replace(np.nan,0, inplace=True)

# plt.plot(win_UK_all.Year, win_UK_all.F_count, marker='o', markerfacecolor='red', color='red', linewidth=2, label="Female")

# plt.plot(win_UK_all.Year, win_UK_all.M_count, marker='*', markerfacecolor='blue', color='blue', linewidth=2, label="Male")

# plt.title("number of medals (Females, Males) won by the UK team between 1896 and 2016")
# plt.xlabel('Year'); plt.ylabel('number of medals');
# plt.legend()


# # =============================================================================
# # Undirected graph
# # =============================================================================

# # libraries
# import pandas as pd
# import numpy as np
# import networkx as nx
# import matplotlib.pyplot as plt
 
# # Build a dataframe with your connections
# friends = pd.DataFrame({ 'from':['Adam', 'Borris', 'Chloe','Adam','Ezzy','Fiona','Ezzy','Harry','Harry','Diana','Fiona'],
#                          'to':['Diana', 'Adam', 'Ezzy','Chloe','Adam','Fiona','Harry','Diana','Borris','Harry','Chloe'],
#                       })
 
# # Build your graph
# G=nx.from_pandas_edgelist(friends, 'from', 'to')
 
# # plot with different layouts

# # Circular
# nx.draw(G, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.circular_layout(G))
# plt.title("circular")
 

# # =============================================================================
# # directed graph
# # =============================================================================
 
# # Build your graph
# G=nx.from_pandas_edgelist(friends, 'from', 'to', create_using=nx.DiGraph())
 
# # plot with different layouts
# # spring
# nx.draw(G, arrows=True,arrowsize=20, with_labels=True, node_size=1500, node_color="skyblue", pos=nx.spring_layout(G))
# plt.title("spring")


 
# # =============================================================================
# # weighted graph
# # =============================================================================

# # Build a dataframe with your connections
# friends = pd.DataFrame({ 'from':['Adam', 'Borris', 'Chloe','Adam','Ezzy','Fiona','Ezzy','Harry','Harry','Diana','Fiona'],
#                          'to':['Diana', 'Adam', 'Ezzy','Chloe','Adam','Ezzy','Harry','Diana','Borris','Harry','Chloe'],
#                          'weight':['5', '3', '6','4','2','7','5','4','8','6','2']})
 
# # Build your graph
# G=nx.from_pandas_edgelist(friends, 'from', 'to', edge_attr=True)
 
# # plot with Fruchterman Reingold layouts
# pos1=nx.fruchterman_reingold_layout(G)
# nx.draw(G, with_labels=True, node_size=1000, pos=pos1)

# labels = nx.get_edge_attributes(G,'weight')
# nx.draw_networkx_edge_labels(G, edge_labels=labels, pos=pos1)
# plt.title("fruchterman_reingold")

 