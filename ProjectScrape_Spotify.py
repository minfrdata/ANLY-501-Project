# -*- coding: utf-8 -*-
"""
Created on Sun Oct  1 13:26:42 2017

@author: minxiaocn
"""


import pandas as pd
import spotipy
import numpy as np
import spotipy.util as util

class spotifyDataCenter():
	def __init__(self,token,no_offset=1):
		self.token=token
		self.search_item=None
		self.playlist_user=None
		self.playlist_id=None
		self.track=None
		self.no_offset=no_offset
	'''get playlist by searching in spotify'''
	def get_playlist(self,search_item):
		self.search_item=search_item
         # will produce 10 csv file for each search item
		playlist_sets=["playlist_"+self.search_item+str(i) for i in np.arange(10)]
		frames=[]
		print(playlist_sets)
		try:
			for ofst in np.arange(self.no_offset):
		
				#use API search and download playlist datasets
				sp = spotipy.Spotify(auth=self.token).search(self.search_item, limit=50, offset=50*ofst, type='playlist', market=None)
				#- offset - the index of the first item to return
				df = pd.DataFrame(sp)
				playlist_sets[ofst]= pd.DataFrame(df.loc['items','playlists'])
				frames.append(playlist_sets[ofst])			  
			#combine all the datasets and save the dataset into local file			
			playlist_full=pd.concat(frames)
			playlist_full.to_csv("full_playlist"+self.search_item+".csv",index=False)
		except:
			print('Seaching error')
			
			
			
			
	"""get lists by users_playlist using uers_id and playlist id, it will return tracks info
	in the playlist. basically, we will use the track_id to find track audio features in the future"""
	def tracks_in_playlists(self,user_list,playlist_id_list):
		self.playlist_id_list=playlist_id_list
		self.user_list=user_list
		track_sets=["track_"+i for i in self.playlist_id_list]
		
		for i in np.arange(len(self.user_list)):
			
			try:
			
				usr=self.user_list[i]
				pid=self.playlist_id_list[i]
				#api parts
				sp2 = spotipy.Spotify(auth=self.token).user_playlist(user=usr,playlist_id=pid)
			
				df= pd.DataFrame(sp2['tracks']['items'])
				track_info= pd.DataFrame(df['track'].tolist())
				#add two label rows for the parent playlist
				track_info["parentPlaylist"]=pid
				track_info["parentCat"]=self.search_item
#			
				track_sets[i]=track_info
			except:
				print("user_playlist error")
				track_sets[i]=pd.DataFrame([0])
		tracks=pd.concat(track_sets)
		tracks.to_csv("tracks_"+self.search_item+".csv",index=False)
			
			
	"""get audio features using track_id from last step, it will return audio features
	     in the playlist. logics is the same as above"""	
	def audio_info(self,track_id_list):
		self.track_id=track_id_list
		sound_sets=["sound_feature_"+ str(i) for i in np.arange(len(self.track_id))]
		for i in np.arange(len(self.track_id)):
			tid=[self.track_id[i]]
			try:
				#use the api the get audio feature here, parameter is the track_id
				sp3 = spotipy.Spotify(auth=self.token).audio_features(tid)
				sound_sets[i]= pd.DataFrame(sp3)	
			except:
				print("audio features error")
				sound_sets[i]=pd.DataFrame([0])
		
		sound_features=pd.concat(sound_sets)
		sound_features["track_id"]=self.track_id.values
		sound_features.to_csv("sound_features_"+self.search_item+".csv",index=False)
		
	

	
