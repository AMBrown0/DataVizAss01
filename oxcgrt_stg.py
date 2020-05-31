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



#==============================Part 2 - Question 1 =================================

#country_list=['China','South Korea','United States','France','United Kingdom','Italy']
#country_list=['United Kingdom']
country_list=['Italy']
stringencyindex_legacy_df=stringencyindex_legacy_df[stringencyindex_legacy_df['CountryName'].isin(country_list)]
confirmedcases_df=confirmedcases_df[confirmedcases_df['CountryName'].isin(country_list)]
country=confirmedcases_df.iloc[:,0].iloc[0]

s_t_df=stringencyindex_legacy_df.transpose()
c_t_df=confirmedcases_df.transpose()
X=c_t_f_df=c_t_df.iloc[2:,:]
X.set_axis(['confirmedcases'],axis=1,inplace=True)
Y=s_t_df.iloc[2:,:]
Y.set_axis(['stringency'],axis=1,inplace=True)
Y.rename(index={0:"stringency"})
result=pd.concat([X,Y], axis=1)
result.set_index("confirmedcases",inplace=True) 
result.sort_index(inplace=True)
# X=confirmedcases_df[confirmedcases_df['CountryName'] == 'China']

# print("Country=%s" % country)
# #Remove the country name and code columns
# #X=X.iloc[:,2:]
# X=X.iloc[:,-5:]


# Y=stringencyindex_legacy_df[stringencyindex_legacy_df['CountryName'] == 'China']
# #Y=Y.iloc[:,2:]
# Y=Y.iloc[:,-5:]

plt.title('Comparison of stringency of COVID-19 repsonse in six countries') 
#X=[3,5,6]
#Y=[1,2,3]
plt.plot(result,label=country)
plt.xscale("log")
plt.ylim(0, 100)
plt.xlim(1, 1000000)
#plt.scatter(X, Y, label='China')
plt.legend()
plt.show()

#X=confirmedcases_df=confirmedcases_df.iloc[1,:]


# plt.plot(r1, sports_M, color='blue', width=barWidth, edgecolor='white', label='Male')
# plt.bar(r2, sports_F, color='red', width=barWidth, edgecolor='white', label='Female')

# plt.title('# of females against males winners for the Winter games from 1972 to 2014') 
# plt.xlabel('Year', fontweight='bold')
# plt.xticks([r + barWidth/2 for r in range(len(sports_M))], sports_M.index,rotation=90, fontsize=8)

# # xl = pd.ExcelFile(dataFile)
# # xl.sheet_names  # see all sheet names



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

 