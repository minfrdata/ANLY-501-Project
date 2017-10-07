#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 21:29:30 2017

@author: chengzhong
"""
import pandas as pd
#open the categories list to read the colnames
with open ('categories.txt','r') as categories:
    #transform to dataframe
    cate = pd.read_csv(categories)['Top Lists'].tolist()

#read the first column
df  = pd.read_csv("track_full_"+cate[0]+".csv")
#append all information to one dataframe
for i in range(len(cate)-1):
    df = df.append(pd.read_csv("track_full_"+cate[i+1]+".csv"))
#write the dataframe to file
df.to_csv("track_full.csv")





