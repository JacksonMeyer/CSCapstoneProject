import Playlist

#make playlist generator object
plGen = Playlist.playlistGen()

#generate and print a playlist
#tracks = plGen.gen_recs([0.1,0.4]) #substitute any values for [valence, energy]; will come from jackson's code
#pl = plGen.gen_playlist(tracks)
#print(plGen.str_playlist(pl))
#plGen.genre_list()
plGen.force_login()



#to save a playlist to user's spotify account
#plGen.save_playlist(tracks)