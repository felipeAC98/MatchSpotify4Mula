import requests
import urllib

class spotifyAPIConection():

	def __init__(self,clientID,clientSecret):

		self.url="https://api.spotify.com/v1/"

		self.clientID=clientID
		self.clientSecret=clientSecret

		self.access_token=self.getToken()
		
		self.header={
			'Authorization': 'Bearer {token}'.format(token=self.access_token)
		}

	#https://stmorse.github.io/journal/spotify-api.html
	def getToken(self):

		AUTH_URL = 'https://accounts.spotify.com/api/token'

		auth_response = requests.post(AUTH_URL, {
		    'grant_type': 'client_credentials',
		    'client_id': self.clientID,
		    'client_secret': self.clientSecret,
		})

		# convert the response to JSON
		auth_response_data = auth_response.json()

		# save the access token
		return auth_response_data['access_token']

	def updateHeader(self):
		self.header={
			'Authorization': 'Bearer {token}'.format(token=self.access_token)
		}

	def sendRequest(self, session, urlValue):

		response = requests.get(url=self.url+session+urlValue,headers=self.header )

		#Verificando se o status eh 200 OK para prosseguir com codigo
		if response.status_code!=200:
			print(response)
			self.getToken()
			self.updateHeader()

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