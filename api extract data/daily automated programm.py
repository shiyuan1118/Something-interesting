#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 00:55:56 2021

@author: baoshiyuan
"""
import requests
import time
import json
import pandas as pd
import datetime
from dateutil.parser import parse

def daily_update():
    while True:
        #update the data from a new day
        if datetime.now().hour == 24:
            try:
                days=[str(d.date()) for d in pd.date_range('2018-1-1',str(datetime.now().date()))][:5]
                #get the data with URL
                data=[]
                for day in days:
                    url='https://content.guardianapis.com/search?from-date=2018-01-01&q=Justin%20AND%20Trudeau&api-key=c73f3b88-1799-4fad-a095-9ce570fd7570'
                    data=requests.get(url)
                    content_json=json.loads(data.content)
                    
                    try:
                        df=pd.DataFrame(content_json['response']['results'])
                        df['date']=df['webPublicationDate'].map(parse).dt.date
                        data.append(df)
                    except:
                        pass
                    time.sleep(0.1)
                daily_data=pd.concat(data)
                
                sta=daily_data['date'].value.counts().sort_index().reset_index()
                #count the number of articles
                sta.columns=['date','count']
                #draw pictire for the evolution
                fig=sta.set_index('date').iplot(kind='bar',theme='white',xTitle='date',yTitle='count',title='Number of Articles about Justin Trudeau which has been posted since 01.01.2018 until today',asFigure=True)
                fig.write_html(r'num_of_articles_over_time.thml')
                print('Successfully!')
                break
            except:
                print('Something is wrong')
                                 
