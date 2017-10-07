# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 22:45:30 2017

@author: minxiaocn
"""


import pandas as pd
import sys
import numpy as np
import spotipy
import numpy as np
import spotipy.util as util
from ProjectScrape_Spotify import spotifyDataCenter
from ProjectScrape_Billboard import BillboardCharts

def main(argv):
	# please setting here
	scope = 'user-library-read'
	token = util.prompt_for_user_token("21hp6bjdej4iw3p7r7ku6k3hy", scope,
	                                   client_id="daee6dac49104695af13009e3c4d028c",
	                                   client_secret ="9242b89b091a42bb94f5d0bc23524b5e",
	                                   redirect_uri = "http://127.0.0.1:8000/")
	search_item="rock"# since the datafile is large,we manually replace the keyword and scrape
	
	# create instance of spotifyDatacenter
	mysearch=spotifyDataCenter(token)	
    
	#===== STEP 1 	#get playlist by serch
	print("step 1 starts")
	
	mysearch.get_playlist(search_item)
	## generate 30 csv (500 records each) for all search_items
	
	
	
	#===== STEP 2 get user_playlist use username and playlist_id
	print("step 2 starts")
	# only use the data with 
	#prepare params
	##get playlist id and user id
	myplaylist=pd.read_csv("full_playlist"+mysearch.search_item+".csv")
	user_list=[eval(i).get("id" ) for i in myplaylist["owner"]]
	playlist_id_list=myplaylist["id"]
	#run function
	mysearch.tracks_in_playlists(user_list,playlist_id_list)
	#combind all the track_in_playlist_id to one csv? yes, can save individual dataset too,but need modify in the methods
	
	
#	
#	#========STEP 3  get track  audio features and combine with user_playlist in step 2
	print("step 3 starts")
	tracks=pd.read_csv("tracks_"+ mysearch.search_item+".csv")
	track_id_list=tracks["id"]
	mysearch.audio_info(track_id_list)
	sound_features=pd.read_csv("sound_features_"+mysearch.search_item+".csv")
	track_full=pd.concat([tracks,sound_features],axis=1)
	track_full.to_csv("track_full_"+mysearch.search_item+".csv",index=False)
	
	#======= STEP 4 sraping billboard website
	#execuation:
	myRanking=BillboardCharts("2016-09-30","2017-09-30")
	with open('genre.txt', 'r') as f:
		genrename = f.readline().split(',')
	for gr in genrename:
		search_item=gr
		myRanking.get_chart(search_item)


if __name__=="__main__":
	main(sys.argv)   
