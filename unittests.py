from classes.spotifyAPI import spotifyAPIConnection
import unittest
import clientToken
import json

class testsSpotifyAPIConnection(unittest.TestCase):

	def test_genre(self):
		spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
		response, respJson=spotifyConnection.trackSearch("Starlight","Muse")
		self.assertEqual(response.status_code, 200)
		
		trackID=respJson['tracks']['items'][0]['id']
		genres=spotifyConnection.get_genres(trackID)
		print("Generos obtidos: "+str(genres))

		expectGenres=['modern rock', 'permanent wave', 'rock']
		self.assertEqual(genres, expectGenres)

	def test_get_type_by_year(self):
		year=2010
		limit=1
		spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
		response, respJson=spotifyConnection.get_type_by_year(_type='track',index=2,year=year,limit=limit)
		print("test_get_type_by_year: "+str(json.dumps(respJson, indent=4, sort_keys=True)))
		self.assertEqual(response.status_code, 200)

	def test_get_artist_top_tracks(self,artistID="0TnOYISbd1XYRBk9myaseg"):
		spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
		response, respJson=spotifyConnection.get_artist_top_tracks(artistID=artistID)
		print("test_get_album_tracks: "+str(json.dumps(respJson, indent=4, sort_keys=True)))
		self.assertEqual(response.status_code, 200)

	def test_get_album_tracks(self,albumID="4aawyAB9vmqN3uQ7FjRGTy"):
		spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
		response, respJson=spotifyConnection.get_album_tracks(albumID=albumID)
		print("test_get_album_tracks: "+str(json.dumps(respJson, indent=4, sort_keys=True)))
		self.assertEqual(response.status_code, 200)

	'''def test_get_user_top_items(self,_type="tracks"):
		spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
		response, respJson=spotifyConnection.get_user_top_items(_type=_type,limit=1)
		print("test_get_user_top_items: "+str(json.dumps(respJson, indent=4, sort_keys=True)))
		self.assertEqual(response.status_code, 200)'''

if __name__ == '__main__':
    unittest.main()