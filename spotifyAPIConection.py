import requests
import urllib

class spotifyAPIConection():

	def __init__(self,access_token):

		self.url="https://api.spotify.com/v1/"

		self.access_token=access_token
		
		self.header={
			'Authorization': 'Bearer {token}'.format(token=access_token)
		}

	def sendRequest(self, session, urlValue):
		response = requests.get(url=self.url+session+urlValue,headers=self.header )

		return response, response.json()

	#Funcao responsavel por realizar buscas pelo banco do spotify
	#as buscas sao feitas a partir de um vType(artista, nome musica...) e o value a ser buscado 
	def search(self, vType, searchValue):

		session='search?'

		urlValue='q='+searchValue+'&type='+vType

		return self.sendRequest(session,urlValue)

	def trackSearch(self, trackName, artistName):

		trackName=urllib.parse.quote(trackName)
		artistName=urllib.parse.quote(artistName)

		searchValue='track:'+trackName+'%20artist:'+artistName

		return self.search('track',searchValue)