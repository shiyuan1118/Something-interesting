#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 11:34:47 2021

@author: baoshiyuan
"""

import requests
import json
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.font_manager as font_manager
from matplotlib import rcParams
import jieba.analyse

##########################################################################
######Extract Information about Justin Trudeau and clean Data#############
##########################################################################


#set query operators, from date and API key to construct the url
url='https://content.guardianapis.com/search?from-date=2018-01-01&q=Justin%20AND%20Trudeau&api-key=c73f3b88-1799-4fad-a095-9ce570fd7570'

#explore the first page data and standarize
data=requests.get(url)
content_json=json.loads(data.content)
df=pd.DataFrame(content_json['response']['results'])
num_results=int(content_json['response']['total'])

#get the number of pages
required_pages=int(content_json['response']['pages'])

#explore the data of all pages and standarize
for page in range(2,required_pages+1):
    
    payload={'page':page}
    data_1=requests.get(url=url,params=payload)
    content_json1=json.loads(data_1.content)
    df_p=pd.DataFrame(content_json1['response']['results'])
    df=df.append(df_p)

#save all row data in Excel
writer=pd.ExcelWriter('Data.xlsx')    

df.to_excel(writer,sheet_name='RowData',index=False)

#filter all items that types are article
df=df[df['type']=='article']    

#standarize the webPublicationDate 
df['date']=pd.to_datetime(df['webPublicationDate'],infer_datetime_format=True).dt.date

df = df.drop(['webPublicationDate'], axis=1)

#sort all data by date
df.sort_values(by='date',ascending=True,inplace=True)

#insert index of data
df.insert(0,'index',range(len(df)),allow_duplicates=False)

df.to_excel(writer,sheet_name='FilteredData',index=False)



##########################################################################
##################Count the number of Articles############################
##########################################################################


#Count the number of articles
df_1=(pd.to_datetime(df['date'],infer_datetime_format=True)
       .dt.floor('d')
       .value_counts()
       .rename_axis('date')
       .reset_index(name='count'))

#standarise the date
df_1['date']=pd.to_datetime(df_1['date'],infer_datetime_format=True).dt.date

#generate a time series
df_2=pd.date_range(start="20180101",end=datetime.date.today(),freq='D').date

#reindex in the whole time series
df_1=(df_1.set_index('date').reindex(df_2))

#When there are no articles mentioned, we count as 0
df_1=df_1.fillna(0)

#get the describe statistics information
describe=df_1['count'].describe()

#save the count of number of articles
df_1.to_excel(writer,sheet_name='Data_Count',index=True)

#calculate the number of articles in every section 
m_section=df['sectionId'].value_counts()

#save the frequence of every section in Excel
m_section.to_excel(writer,sheet_name='Data_Frequency',index=True)


##########################################################################
#########################Data Visualisation###############################
##########################################################################


#Set font and picture format
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Avenir Next']

fig = plt.figure(figsize=(15,9), dpi=244)
ax = fig.add_subplot(111)

#set x axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y%m$d'))
plt.xticks(pd.date_range(start="20180101",end=datetime.date.today(),freq='Q'), rotation=45)

#set y axis
my_y_ticks = np.arange(0, 20, 2)
plt.yticks(my_y_ticks)

#drawing the line chart over time
table = pd.DataFrame([i for i in range(len(df_1))],columns=['value'],index=pd.date_range(start="20180101",end=datetime.date.today(),freq='D'))
ax.plot(table.index,df_1['count'],color='lightgrey', label='No. of articles',linewidth='0.8')

#set labels and title
plt.xlabel('Date', fontsize=18)
plt.ylabel('Count', fontsize=18)
ax.legend()  
plt.title('Number of Articles about Justin Trudeau which has been posted since 01.01.2018 until today', fontsize=15, color='black', pad=20)          
plt.gcf().autofmt_xdate()

#drawing Auxiliary line with mean value
sup_line = [round(df_1['count'].mean(),2) for i in range(len(df_1))]
ax.plot(table.index, sup_line, color='black', linestyle='--', linewidth='1.5', label='Mean Value')
ax.legend()  

plt.show()

##########################################################################
######################Find the unusual Events#############################
##########################################################################
unusual=df_1[df_1['count']>=df_1['count'].quantile(0.999)]
unusual=unusual.index.values.tolist()

for i in range(len(unusual)):
    print(unusual[i])
    print(df[df['date']==unusual[i]]['webTitle'])
    print('\n')
    

#analyse the keywords of web Titel in the five most published days with weight


dates=df['date'].value_counts().head(5).index.values

for d in dates:
    sub=df.query('date==@d')
    
    key_words=jieba.analyse.extract_tags(sub['webTitle'].sum(),topK=5,withWeight=True)

    print(d)
    print(key_words)
    print('\n')

writer.save()


   
    
    