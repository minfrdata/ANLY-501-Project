#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 21:29:30 2017

@author: minxiaocn
"""

import json
import pandas as pd
import billboard
import numpy as np
class BillboardCharts():
	
	def __init__(self, start_date,end_date):
		self.start_date=start_date
		self.end_date=end_date	
		self.date_setting=None
		self.search_item=None
		
	
	def get_chart(self,search_item):
		#dont set the time interval too large, expensive in ROM when storing data
		self.search_item=search_item
		self.date_setting = pd.date_range(start=self.start_date, end=self.end_date, freq='W')
		""""this function is to get the ranking list from billboard 
		params:
		search_item
		date"""
		n=len(self.date_setting)
		charts_sets=["charts_"+str(i) for i in np.arange(n)]
	
		for i in np.arange(n):
			print(i)
			dt=str(self.date_setting[i].date())
			try:
				#using api to get data here: billboard.ChartData
				chart = pd.DataFrame(json.loads(billboard.ChartData(self.search_item,date=dt).json())['entries'])
				chart['Date'] = dt
				charts_sets[i]=chart
			except:
				"charts error"
			

		charts_full=pd.concat(charts_sets)
		charts_full.to_csv("charts_"+self.search_item+"from_"+self.start_date+"_to_"+self.end_date+".csv")
		del charts_sets



