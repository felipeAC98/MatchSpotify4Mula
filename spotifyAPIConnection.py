import requests
import urllib
import logger
from time import sleep as sleep
import traceback
import clientToken
import json

class spotifyAPIConnection():

	def __init__(self,clientID,clientSecret):

		self.url="https://api.spotify.com/v1/"

		self.clientID=clientID
		self.clientSecret=clientSecret

		self.access_token=self.getToken()
		
		self.header={
			'Authorization': 'Bearer {token}'.format(token=self.access_token)
		}

		self.logger=logger.setup_logger("spotifyAPI")

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

		self.logger.debug("sendRequest")

		status_code=0
		waitTime=4
		tentativas=0

		#Verificando se o status eh 200 OK para prosseguir com codigo
		while(status_code!=200 and tentativas<3):

			try:
				response = requests.get(url=self.url+session+urlValue,headers=self.header )
				status_code=response.status_code

				if status_code!=200:
					sleep(waitTime)
					self.logger.debug(" request fail:"+ str(response))
					print(response)
					self.access_token=self.getToken()
					self.updateHeader()

			except:
				self.logger.warning(' erro sendRequest: '+str(traceback.format_exc()))

				sleep(waitTime)

			waitTime=waitTime*2
			tentativas=tentativas+1

			#response = requests.get(url=self.url+session+str(urlValue),headers=self.header )

		self.logger.debug("response:"+ str(response))

		#self.logger.debug("response.json():"+ str(response.json()))

		return response, response.json()

	#Funcao responsavel por realizar buscas pelo banco do spotify
	#as buscas sao feitas a partir de um vType(artista, nome musica...) e o value a ser buscado 
	def search(self, vType, searchValue):

		self.logger.debug("search")

		session='search?'

		urlValue='q='+searchValue+'&type='+vType

		self.logger.debug("urlValue: "+ str(urlValue))

		return self.sendRequest(session,urlValue)

	def trackSearch(self, trackName, artistName):

		self.logger.debug("trackSearch")

		trackName=urllib.parse.quote(trackName)
		artistName=urllib.parse.quote(artistName)

		searchValue='track:'+trackName+'%20artist:'+artistName

		self.logger.debug("searchValue: "+ str(searchValue))

		return self.search('track',searchValue)

	def get_audioFeatures(self, ID):
		
		self.logger.debug("get_audioFeatures")

		session='audio-features/'

		return self.sendRequest(session,ID)

	def get_track(self, ID):

		self.logger.debug("get_audioFeatures")

		session='tracks/'

		return self.sendRequest(session,ID)

	def get_releaseDate(self,ID):

		self.logger.debug("get_releaseDate")

		response, respJson=self.get_track(ID)

		return respJson['album']['release_date']

	def get_audioAnalysis(self,ID):

		self.logger.debug("get_audioAnalysis")

		session='audio-analysis/'

		return self.sendRequest(session,ID)

	def get_audioAnalysisResumed(self,ID):

		self.logger.debug("get_audioAnalysisResumed")

		session='audio-analysis/'

		response, respJson=self.sendRequest(session,ID)

		tempo_confidence=respJson['track']['tempo_confidence']
		time_signature_confidence=respJson['track']['time_signature_confidence']
		key_confidence=respJson['track']['key_confidence']
		mode_confidence=respJson['track']['mode_confidence']

		bars=len(respJson['bars'])
		beats=len(respJson['beats'])
		sections=len(respJson['sections'])
		segments=len(respJson['segments'])
		tatums=len(respJson['tatums'])

		print(respJson['track']['tempo_confidence'])
		return respJson

	def get_artistInfo(self,ID):

		self.logger.debug("get_artistInfo")

		session='artists/'

		return self.sendRequest(session,ID)

	def get_genres(self,ID):

		self.logger.debug("get_genres")

		response, respJson=self.get_track(ID)

		genres=[]

		for artist in respJson['artists']:

			artistID=artist['id']
			response,artistInfoJson=self.get_artistInfo(artistID)

			for genre in artistInfoJson['genres']:

				genres.append(genre)

		return genres

class spotifyAPIConnectionTests():

	def __init__(self):
		self.spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)


	def test_genre(self):
		response, respJson=self.spotifyConnection.trackSearch("Starlight","Muse")
		trackID=respJson['tracks']['items'][0]['id']

		print("Generos obtidos: "+str(self.spotifyConnection.get_genres(trackID)))