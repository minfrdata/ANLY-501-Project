# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 18:33:50 2017

@author: minxiaocn
"""
import pandas as pd
import numpy as np
import ast as ast
from CleanlinessCheck import cleanCheck
import sys

#exective function



def main(argv):
	"""we will check the cleanliness of two datasets in this part.
	two datasets:
	track_full.csv
	billboardranking.csv
 
	the cleanliness check result will be save into 2 csv, so you can have a look at the summary and scores 
	for the data.
	
	After this we will clean datasets using the index of those wrong records from the cleanliness check 
	phase.
	"""
	#1.cleanliness for the spotify dataset
	#set the parameters
	colname_selection=['album', 'artists', 'available_markets', 'duration_ms', 'id', 'name',
	       'popularity',  
	       'parentPlaylist', 'parentCat', 'acousticness', 
	       'danceability', 'energy', 'instrumentalness',
	       'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
	       'time_signature', 'valence'
	       ]
	
	col_names=['album', 'artists', 'available_markets', 'duration_ms', 'track_id', 'track_name',
	       'popularity',    
	       'parentPlaylist', 'parentCat', 'acousticness', 
	       'danceability', 'energy', 'instrumentalness',
	       'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
	       'time_signature', 'valence'
	       ]								
	col_categorical=["mode"]
	category_range={"mode":[0,1]}
	mymin=[np.nan, np.nan, np.nan, 0.01,np.nan,np.nan,0, np.nan, np.nan, 0, 0, 0, 0,0, 0, -60, np.nan, 0, 0.01,0.01, 0]
	mymax=[np.nan, np.nan, np.nan, 99999999,np.nan,np.nan,99999999, np.nan, np.nan, 1, 1, 1, 1,11, 1, 0, np.nan, 1, 999999999,999999999, 1]
	FileName="track_full.csv"	
	mySpotify=cleanCheck(col_names,FileName,colname_selection)	
	mySpotify.QualityControl(mymin,mymax,col_categorical,category_range)
	     
					
		
	#	#==================================================================================================================
	      #2.cleanliness for billboard dataset
	colname_selection=["Date","Genre","artist","lastPos","peakPos","rank","title","weeks"]
	col_names=["Date","Genre","artist","lastPos","peakPos","rank","title","weeks"]
	mymin=[np.nan,np.nan,np.nan,0,1,0,np.nan,1]
	mymax=[np.nan,np.nan,np.nan,50,50,50,np.nan,99999999]
	FileName="billboardranking.csv"
	myBillboard=cleanCheck(col_names,FileName,colname_selection,logical_test=True)
	myBillboard.QualityControl(mymin,mymax,col_categorical,category_range,"lastPos","peakPos")
	#	
		
		#=================================================================================================================
		#%%%%%%%%after cleanliness check, we will clean the dataset using record indexes 
		#3.clean the spotify dataset
	#	#remove blank_rows
	mySpotify.dataset=mySpotify.dataset.drop(mySpotify.blank_index)
	#remove the duplicated rows
	mySpotify.dataset=mySpotify.dataset.drop_duplicates(keep="first")
	#correct the missing cells:
	
	str_col=['album', 'artists', 'available_markets', 'duration_ms', 'track_id', 'track_name','parentPlaylist', 'parentCat']
	num_col=['popularity','acousticness', 'danceability', 'energy', 'instrumentalness','liveness', 'loudness',  'speechiness', 'tempo','time_signature', 'valence']	
	int_col=['key',"mode"]
	for i in np.arange(len(mySpotify.col_names)):
		
		col=mySpotify.col_names[i]
		# remove the str columns with missingcells
		# remove the str columns with outrange cells
		mySpotify.Missing_cell_rows()
		if col in str_col:
			mySpotify.dataset=mySpotify.dataset.drop(mySpotify.col_missingCell[i])
			
			mySpotify.dataset=mySpotify.dataset.drop(mySpotify.col_outrange[i])
	    # replace the numeric missing cells with mean:
		# replace out of range values in numeric columns with mean:
		if col in num_col:
			mySpotify.dataset.loc[mySpotify.col_missingCell[i].tolist(),col]=np.mean(mySpotify.dataset[col][~np.isnan(mySpotify.dataset[col])]) 
			mySpotify.dataset.loc[mySpotify.col_outrange[i].tolist(),col]=np.mean(mySpotify.dataset[col][~np.isnan(mySpotify.dataset[col])])  
		
		if col in int_col:	
		# replace the int mising cells with median:
		# replace the out of range cell that in int columns with median:
			mySpotify.dataset.loc[mySpotify.col_missingCell[i].tolist(),col]=np.median(mySpotify.dataset[col][~np.isnan(mySpotify.dataset[col])]) 
			mySpotify.dataset.loc[mySpotify.col_outrange[i].tolist(),col]=np.median(mySpotify.dataset[col][~np.isnan(mySpotify.dataset[col])]) 
		
	
			#4.clean the billboard data
		
	#remove blank_rows
	myBillboard.dataset=myBillboard.dataset.drop(myBillboard.blank_index)
	#remove the duplicated rows
	myBillboard.dataset=myBillboard.dataset.drop_duplicates(keep="first")
	#correct the missing cells:
	
	str_col=["Genre","artist","title"]
	num_col=["lastPos","peakPos","rank","weeks"]	
	int_col=[]
	for i in np.arange(len(myBillboard.col_names)):
		col=myBillboard.col_names[i]
		# remove the str columns with missingcells
		# remove the str columns with outrange cells
		mySpotify.Missing_cell_rows()
		if col in str_col:
			myBillboard.dataset=myBillboard.dataset.drop(myBillboard.col_missingCell[i])
			
			myBillboard.dataset=myBillboard.dataset.drop(myBillboard.col_outrange[i])
	    # replace the numeric missing cells with mean:
		# replace out of range values in numeric columns with mean:
		if col in num_col:
			myBillboard.dataset.loc[myBillboard.col_missingCell[i].tolist(),col]=np.mean(myBillboard.dataset[col][~np.isnan(myBillboard.dataset[col])]) 
			myBillboard.dataset.loc[myBillboard.col_outrange[i].tolist(),col]=np.mean(myBillboard.dataset[col][~np.isnan(myBillboard.dataset[col])])  
		
		if col in int_col:	
		# replace the int mising cells with median:
		# replace the out of range cell that in int columns with median:
			myBillboard.dataset.loc[myBillboard.col_missingCell[i].tolist(),col]=np.median(myBillboard.dataset[col][~np.isnan(myBillboard.dataset[col])]) 
			myBillboard.dataset.loc[myBillboard.col_outrange[i].tolist(),col]=np.median(myBillboard.dataset[col][~np.isnan(myBillboard.dataset[col])]) 
		
	#======================After cleaning, we check the cleanliness of data
	"""this part just repeats the first two steps, and you can check the report csv for the clean data"""
	myBillboard.dataset.to_csv("myBillboard.csv",index=False)
	mySpotify.dataset.to_csv("mySpotify.csv",index=False)
	#4.1cleanliness for the spotify dataset
	#set the parameters
	
	col_names=['album', 'artists', 'available_markets', 'duration_ms', 'track_id', 'track_name',
	       'popularity',    
	       'parentPlaylist', 'parentCat', 'acousticness', 
	       'danceability', 'energy', 'instrumentalness',
	       'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo',
	       'time_signature', 'valence'
	       ]								
	col_categorical=["mode"]
	category_range={"mode":[0,1]}
	mymin=[np.nan, np.nan, np.nan, 0.01,np.nan,np.nan,0, np.nan, np.nan, 0, 0, 0, 0,0, 0, -60, np.nan, 0, 0.01,0.01, 0]
	mymax=[np.nan, np.nan, np.nan, 99999999,np.nan,np.nan,99999999, np.nan, np.nan, 1, 1, 1, 1,11, 1, 0, np.nan, 1, 999999999,999999999, 1]
	FileName="mySpotify.csv"	
	mySpotify=cleanCheck(col_names,FileName,col_names)	
	mySpotify.QualityControl(mymin,mymax,col_categorical,category_range)
	
	#4.2.cleanliness for billboard dataset
	colname_selection=["Date","Genre","artist","lastPos","peakPos","rank","title","weeks"]
	col_names=["Date","Genre","artist","lastPos","peakPos","rank","title","weeks"]
	mymin=[np.nan,np.nan,np.nan,0,1,0,np.nan,1]
	mymax=[np.nan,np.nan,np.nan,50,50,50,np.nan,99999999]
	FileName="myBillboard.csv"
	myBillboard=cleanCheck(col_names,FileName,colname_selection,logical_test=True)
	myBillboard.QualityControl(mymin,mymax,col_categorical,category_range,"lastPos","peakPos")
	
if __name__=="__main__":
	main(sys.argv)   

			

	
