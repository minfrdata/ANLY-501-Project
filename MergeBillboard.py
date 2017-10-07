#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 02:08:43 2017

@author: chengzhong
"""
import pandas as pd

#Choose the genre col names
bbgenre = ['pop-songs','country-songs','rock-songs','r-b-hip-hop-songs',
           'dance-electronic-songs','latin-songs','christian-songs','hot-holiday-songs',
           'youtube','greatest-hot-100-singles','hot-100']

#read the first file we scraped from billboard as a dataframe
dfb = pd.read_csv("charts_"+bbgenre[0]+"from_2016-09-30_to_2017-09-30.csv")
dfb['Genre'] = bbgenre[0]

#merge all the data to one file
for i in range(len(bbgenre)-1):
    df2 = pd.read_csv("charts_"+bbgenre[i+1]+"from_2016-09-30_to_2017-09-30.csv")
    df2['Genre'] = bbgenre[i+1]
    dfb = dfb.append(df2)
#choose valid columns
dfb = dfb[['Date','Genre','artist','lastPos','peakPos','rank','title','weeks']]
#write the dataframe to csv
dfb.to_csv('billboardranking.csv',index = False)
