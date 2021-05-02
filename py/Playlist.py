#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random as rand
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

class playlistGen:

    redirect = 'http://localhost:8080'
    scope = 'user-top-read playlist-modify-public playlist-modify-private'
    cid = '61f3c3cc2b9e4ff8991a2cae3e8ee7e4'
    secret = 'bf04d10991b243aea72b34f35a479f16'
    default = ['happy','sad','r-n-b','pop','hip-hop']
    err_msg = "Something went wrong, please retry after logging in again"
    
    #initialize playlist generator; "genres" takes a list of up to 5 genres; personal is boolean 
    def __init__(self, genres=default, personal = True):
        #initialize general purpose client credential spotify API
        self.__client_credentials_manager = SpotifyClientCredentials(client_id=self.cid, client_secret=self.secret)
        self.sp = spotipy.Spotify(client_credentials_manager=self.__client_credentials_manager)
        
        #set personalization
        self.__personal = personal
    
        #Login with spotify user auth API and get their user id
        try:
            self.__oauth_manager = SpotifyOAuth(client_id=self.cid, client_secret=self.secret, redirect_uri=self.redirect, scope=self.scope)
            self.__token = self.__oauth_manager.get_cached_token()
            self.sp2 = spotipy.Spotify(oauth_manager=self.__oauth_manager)
            self.__uid = self.sp2.current_user()['id']
        except:
            #no token or uid if login fails
            self.__token = None
            self.__uid = None
        
        #set user's genres or default
        self.__genres = genres
   
    #check if there is a valid auth token
    def check_auth(self):
        return self.__oauth_manager.validate_token(self.__token)
    
    #return list of genres used to make recommendations
    def get_genres(self):
        return self.__genres

    #generate a spotify track list object, "vals" takes list in format [valence, energy]
    def gen_recs(self, vals):

        #check if user wants personalized results
        if self.__personal:
            auth = self.check_auth()
        else:
            auth = False
            
        genres = self.get_genres()

        if not self.sp2.current_user_top_tracks(limit=1)['items']:
            auth = False

        if auth:
            #reccomend tracks based on user's top spotify artists and tracks
            try:
                fav_artists = self.sp2.current_user_top_artists(limit=3)
                fav_tracks = self.sp2.current_user_top_tracks(limit=5)

                artist_uris = [artist['uri'] for artist in fav_artists['items']]
                track_uris = [track['uri'] for track in fav_tracks['items']]
                results = self.sp.recommendations(seed_artists=artist_uris, seed_tracks=track_uris[:5-len(artist_uris)],
                                             target_valence=vals[0], target_energy=vals[1], max_speechiness=0.3,
                                             max_liveness=0.8)
                return results['tracks']
            except:
                print(self.err_msg)

        elif genres:
            #recommend tracks based on chosen genres
            results = self.sp.recommendations(seed_genres=genres, target_valence=vals[0], target_energy=vals[1],
                                         max_speechiness=0.3, max_liveness=0.8)
            return results['tracks']

        else:
            #recommend tracks from random genres if none selected
            genres = rand.sample(self.sp.recommendation_genre_seeds()['genres'],k=5)
            results = self.sp.recommendations(seed_genres=genres, target_valence=vals[0], target_energy=vals[1],
                                         max_speechiness=0.3, max_liveness=0.8)
            return results['tracks']
      
    #makes a list of lists containing [track title, artist name]; "tracklist" takes tracklist object from gen_recs()
    def gen_playlist(self, tracklist):
        return [[track['name'],track['artists'][0]['name']]for track in tracklist]
    
    #outputs human readable playlist; "playlist" takes list from gen_playlist()
    def str_playlist(slef, playlist):
        return "\n".join([i[0] + ' -- ' + i[1] for i in playlist])
    
    #sets the genre list; "genres" takes list of up to 5 genres
    def set_genres(self, genres):
        self.__genres = genres
        
    #sets the genre list back to the default
    def restore_genre_default(self):
        self.__genres = self.default
        
    #returns value of personal
    def get_personal(self):
        return self.__personal
    
    #toggles personalization setting
    def toggle_personal(self):
        if self.__personal:
            self.__personal = False
        else:
            self.__personal = True
            
    #returns spotify user id of current user
    def get_uid(self):
        return self.__uid
    
    #saves the generated playlist to the user's spotify account; "tracklist" takes tracklist object from gen_recs()
    def save_playlist(self, tracklist):
        #check if the user is logged in
        if self.check_auth():
            try:
                #create empty playlist and return its id
                pl = self.sp2.user_playlist_create(self.get_uid(),'My Mood Playlist', public = False)['uri']
                #get uris for the recommended songs
                uris = [track['uri'] for track in tracklist]
                #add the songs to the new playlist
                self.sp2.user_playlist_add_tracks(self.get_uid(),pl,uris)
                print("Playlist saved successfully!")
            except:
                #warns user if API breaks
                print(self.err_msg)
        else:
            #tell user to login if they haven't
            print("You must log in to Spotify first")
    
    #brings up the spotify login page so user may login if not already, or switch accounts
    def force_login(self):
        try:
            #Forces the spotify login/app-authorization-page to pop up
            self.__oauth_manager = SpotifyOAuth(client_id=self.cid, client_secret=self.secret, redirect_uri=self.redirect,
                                          scope=self.scope, show_dialog=True)
            self.__oauth_manager.get_access_token(as_dict=False,check_cache=False)
            self.__oauth_manager = SpotifyOAuth(client_id=self.cid, client_secret=self.secret, redirect_uri=self.redirect,
                                          scope=self.scope, show_dialog=False)
            #sets user API and uid
            self.sp2 = spotipy.Spotify(oauth_manager=self.__oauth_manager)
            self.__uid = self.sp2.current_user()['id']
            self.__token = self.__oauth_manager.get_cached_token()
        except:
            #blanks token and uid on failed login/authorization
            self.__token = None
            self.__uid = None
            print(self.err_msg)
            
    #prints list of all valid spotify genres for reference
    def genre_list(self):
        print(self.sp.recommendation_genre_seeds()['genres'])
        print(len(self.sp.recommendation_genre_seeds()['genres']))