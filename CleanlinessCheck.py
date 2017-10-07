# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 23:48:34 2017

@author: minxiaocn
"""
import pandas as pd
import numpy as np
import ast

class cleanCheck():
	
	def __init__(self,col_names,rawdata,colname_selection,logical_test=False,specialcol=False):
		self.col_names=col_names
		self.rawdata=rawdata
		self.colname_selection=colname_selection
		self.dataset=None
		self.dataset_dim=None
		self.description=None
		self.col_outrange=None
		self.col_missingCell=None
		self.logical_test=logical_test
		self.specialcol=specialcol
		
		
	def loadingData(self):
		'''this is an executive function should not be in a class
		data loading
		remove useless columns'''
			#reading raw data and only remove useless columns
		dataset=pd.read_csv(self.rawdata)
		dataset=dataset[self.colname_selection]
		#rename columns to make it clear
		dataset.columns=self.col_names
		self.dataset=dataset
		
	def specialCol(self):
		"""function to deal with columns where each cell contains a list or dictionary
		in spotify data set, it will be album and artists"""
		
		#get the album name from the album column which is originally a dictionary
		try:
			self.dataset["album"]=self.dataset["album"].apply(lambda x: ast.literal_eval(x)["name"])
			self.dataset["artists"]=self.dataset["artists"].apply(lambda x: ast.literal_eval(x)[0]["name"])
		except:
			print("error when fetching data from list or dictionary column")
		#get the artisit name from the artist colum which is originally a list
		
		
	def basicDescription(self):
		'''get a basic sense of a dataset'''
		self.dataset_dim=self.dataset.shape
		#for each column, check data decription
		self.description=self.dataset.describe(include='all')
		
		
	def duplicated_rows(self):
		''' this function checks duplicated row records,
		index will be returned
		'''
#		self.duplicated_rows=dataset.loc[dataset.duplicated(keep='first'),:]
		self.duplicated_index=self.dataset.index[self.dataset.duplicated(keep='first')]
		
		
	def blank_rows(self):
		''' this function checks blank row records,
		index will be returned
		'''
		#4. missing values checking, first rows and then columns
		#blank row
		self.blank_index=self.dataset.index[self.dataset.isnull().all(1)]
#		self.blank_row=dataset.iloc[blank_index]
#		self.no_blank_row=len(blank_row)
		
		
	def Missing_cell_rows(self):
		# problem: include both blank_rows and rows with part mising
		#no. of missing cells 
		"""this function checks row records with missing cell records,
		missing values in the blank row will also be recored here.
		a list of index for each column will be returned
		"""
		self.col_missingCell = ["rows_missingValue_"+i for i in self.col_names]
		for i in np.arange(len(self.col_names)):
			  target_col=self.dataset[self.col_names[i]]
			  self.col_missingCell[i]=self.dataset.index[target_col.isnull()]
#			
#		self.row_withMissing_cell_index = self.dataset.index[self.dataset.isnull().any(axis=1)]
#		row_withMissing_cell=dataset.iloc[row_withMissing_cell_index]
#		no_row_withMissing_cell=len(row_withMissing_cell)
#		
		#missing dalei
		#need to identify empty dictionarys and empty list in several colss and fetch the required the data
		#		if to be done
		
		
	

	
	def out_range(self,mymin,mymax,col_categorical,category_range):
		          #need specify categorical cols among numerical cols
		"""function to check data out of range for each numerical cols  and check wrong type for str cols.
		so before using this method,cols in the data frame should be cleaned to be numerical and str cols only, 
		for example,values storing list or dictionary should be fetched out.
		
			
		
		parameter for this funtin:
		mymin: a list of minimum value of each col
		mymax: a list of maximum value of each col
		col_categorical: a list contains the column name of categorical columns
		category_range:: a list contains the categories for each cols, for example: mode:[0,1] is an element 
		this list
		
		
		return: self.col_outrange
		this function return a list of the index of outrange item for each column,
		they will be stored in a list """
	
		
		self.col_outrange=["outrange_index_col_"+i for i in self.col_names]
		no_col=len(self.col_names)
		
		for i in np.arange(no_col):
			target_col=self.dataset[self.col_names[i]]
			print(i)
			try:
				if pd.api.types.is_numeric_dtype(target_col):
					
					if self.col_names[i] in col_categorical:
						outrange_index=self.dataset.index[target_col.notnull().apply(lambda x: x not in category_range[self.col_names[i]])]
							
					else:
						outrange_index=self.dataset.index[(target_col<mymin[i])|(target_col>mymax[i])]
#						outrange_rows=self.dataset.iloc(outrange_index)
				else:
					correct_index=target_col.apply(type).eq(str).index.values.tolist()
					outrange_index=list(set(self.dataset.index.tolist())-set(correct_index))
				self.col_outrange[i]=outrange_index
			
			except:
				print("out of range error in column"+self.col_names[i])
				
	def logicCheck(self,column1,column2):
		"""function to check the logic is correct between columns.
		in our data, we will see if element in one column is larger than the correspoing element in another colum
		when it should be less
		
		parameters:column1
	                column2
		out: self.dataset.index
		
		"""
		#get the index for rows which doesn't satisfy column 1 < column2
		self.logicindex=self.dataset.index[self.dataset[column1]<self.dataset[column2]]
				


	
	
	
	def QualityControl(self,mymin,mymax,col_categorical,category_range,column1=None,column2=None):
		
		"""function to summarize all cleaning test scores for each colums and overall dataset"""
		
		self.loadingData()
		if self.specialcol:
			self.specialCol()
		#diagnosis for whole dataet
		self.duplicated_rows()
		self.blank_rows()
		#diagnosis for each column
		self.basicDescription()
		self.Missing_cell_rows()
		self.out_range(mymin, mymax, col_categorical, category_range)
		if self.logical_test:
			self.logicCheck(column1,column2)
			
		
		# write the result to the local file:
		with open("CleanlinessCheck_"+self.rawdata+".csv", "w") as f:
			f.write("Summary of the whole dataset \n")
			f.write("data dim:"+str(self.dataset_dim)+"\n")
			f.write("Proportion of duplicated rows is "+str(len(np.unique(self.duplicated_index.tolist()))/(self.dataset_dim[0]))+"\n")
			f.write("Proportion of blank rows is "+str(len(np.unique(self.blank_index.tolist()))/(self.dataset_dim[0]))+"\n")
#		column_summary=self.basicDescription
		column_cleanliness=pd.DataFrame([[len(i.tolist())/self.dataset_dim[0] for i in self.col_missingCell],[len(i)/self.dataset_dim[0]  for i in self.col_outrange]],columns=self.col_names)
          #add the logial result if there is one
		if self.logical_test:		
			column_cleanliness=column_cleanliness.T
			column_cleanliness["logical_test"]=np.zeros(len(self.col_names))
			column_cleanliness=column_cleanliness.T
			
			column_cleanliness.loc["logical_test",column1]=len(self.logicindex.tolist())/self.dataset_dim[0]
			column_cleanliness.loc["logical_test",column2]=len(self.logicindex.tolist())/self.dataset_dim[0]
			
			
		column_cleanliness.to_csv("CleanlinessCheck_"+self.rawdata+".csv",mode="a")
		
#	def dataClean(self):
#		#remove the blank rows
#		if self.blank_index!=[]:
#			self.dataset=self.dataset.drop(self.blank_index)
#		#remove the duplicated rows
#		self.drop_duplicates(keep="first")
#		#
#		for col in 
#		
#			
#		
#			
			
			
		
		
		

	
#	
#colname_selection=['album', 'artists', 'available_markets', 'duration_ms', 'id', 'name',
#       'popularity',  
#       'parentPlaylist', 'parentCat', 'acousticness', 
#       'danceability', 'energy', 'instrumentalness',
#       'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
#       'time_signature', 'valence'
#       ]
#
#col_names=['album', 'artists', 'available_markets', 'duration_ms', 'track_id', 'track_name',
#       'popularity',    
#       'parentPlaylist', 'parentCat', 'acousticness', 
#       'danceability', 'energy', 'instrumentalness',
#       'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
#       'time_signature', 'valence'
#       ]								
#col_categorical=["mode"]
#category_range={"mode":[0,1]}
#mymin=[np.nan, np.nan, np.nan, 0.01,np.nan,np.nan,0, np.nan, np.nan, 0, 0, 0, 0,0, 0, -60, np.nan, 0, 0.01,0.01, 0]
#mymax=[np.nan, np.nan, np.nan, 99999999,np.nan,np.nan,99999999, np.nan, np.nan, 1, 1, 1, 1,11, 1, 0, np.nan, 1, 999999999,999999999, 1]
#FileName="track_full_chill.csv"	
#myClean=cleanCheck(col_names,FileName,colname_selection)	
#myClean.QualityControl()
#     
#			


#colname_selection=["Date","Genre","artist","lastPos","peakPos","rank","title","weeks"]
#col_names=["Date","Genre","artist","lastPos","peakPos","rank","title","weeks"]
#mymin=[np.nan,np.nan,np.nan,0,1,0,np.nan,1]
#mymax=[np.nan,np.nan,np.nan,50,50,50,np.nan,99999999]
#FileName="charts_christian-songsfrom_2016-09-30_to_2017-09-30.csv"
#myBillboard=cleanCheck(col_names,FileName,colname_selection,logical_test=True)
#myBillboard.QualityControl("lastPos","peakPos")
#






	


	
	