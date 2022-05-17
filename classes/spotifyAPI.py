import requests
import urllib
import classes.logger as logger
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

	def sendRequest(self, session, urlValue=''):

		self.logger.debug("sendRequest")

		status_code=0
		waitTime=10
		tentativas=0

		#Verificando se o status eh 200 OK para prosseguir com codigo
		while(status_code!=200 and tentativas<3):

			try:
				response = requests.get(url=self.url+session+urlValue,headers=self.header )
				status_code=response.status_code
				if status_code!=200:
					self.logger.debug(" request fail:"+ str(response))
					print(response)
					if status_code == 429:
						print("Aguardando por: "+str(response.headers['retry-after']))
						sleep(int(response.headers['retry-after']))
					else:
						sleep(waitTime)
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
	def search(self, vType, searchValue,limit=20,index=0):

		self.logger.debug("search")

		session='search?'

		urlValue='q='+searchValue+'&type='+vType+'&limit='+str(limit)+'&offset='+str(index)

		self.logger.debug("urlValue: "+ str(urlValue))

		return self.sendRequest(session,urlValue)

	def trackSearch(self, trackName, artistName):

		self.logger.debug("trackSearch")

		trackName=urllib.parse.quote(trackName)
		artistName=urllib.parse.quote(artistName)

		searchValue='track:'+trackName+'%20artist:'+artistName

		self.logger.debug("searchValue: "+ str(searchValue))

		return self.search('track',searchValue)

	def get_audioFeatures(self, trackID):
		
		self.logger.debug("get_audioFeatures")

		session='audio-features/'

		return self.sendRequest(session,trackID)

	def get_track(self, trackID):

		self.logger.debug("get_audioFeatures")

		session='tracks/'

		return self.sendRequest(session,trackID)

	def get_releaseDate(self,trackID):

		self.logger.debug("get_releaseDate")

		response, respJson=self.get_track(trackID)

		return respJson['album']['release_date']

	def get_audioAnalysis(self,trackID):

		self.logger.debug("get_audioAnalysis")

		session='audio-analysis/'

		return self.sendRequest(session,trackID)

	def get_audioAnalysisResumed(self,trackID):

		self.logger.debug("get_audioAnalysisResumed")

		session='audio-analysis/'

		response, respJson=self.sendRequest(session,trackID)

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

	def get_artistInfo(self,artistID):

		self.logger.debug("get_artistInfo")

		session='artists/'

		return self.sendRequest(session,artistID)

	def get_genres(self,trackID):

		self.logger.debug("get_genres")

		response, respJson=self.get_track(trackID)

		genres=[]

		for artist in respJson['artists']:

			artistID=artist['id']
			response,artistInfoJson=self.get_artistInfo(artistID)

			for genre in artistInfoJson['genres']:

				genres.append(genre)

		return genres

	def get_type_by_year(self, _type='track',genre=None, index=1,year=2020,limit=10):

		self.logger.debug("get_tracks_by_year")

		year=urllib.parse.quote(str(year))

		if genre!=None:
			searchValue='genre:'+str(genre) + '+year:'+year
		else:
			searchValue='year:'+year

		self.logger.debug("searchValue: "+ str(searchValue))

		return self.search(_type,searchValue,limit=limit, index=index)

	def get_artist_top_tracks(self, artistID, market="BR"):

		self.logger.debug("artist_top_tracks")

		session='artists/'+str(artistID)+'/top-tracks?'

		urlValue='market='+str(market)

		return self.sendRequest(session,urlValue)

	def get_album_tracks(self, albumID, limit=10):

		self.logger.debug("get_album_tracks")

		session='albums/'+str(albumID)+'/tracks?'

		urlValue='limit='+str(limit)

		return self.sendRequest(session,urlValue)

class spotifyAPIConnectionTests():

	def __init__(self):
		self.spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)


	def test_genre(self):
		response, respJson=self.spotifyConnection.trackSearch("Starlight","Muse")
		trackID=respJson['tracks']['items'][0]['id']

		print("Response: "+str(response))
		print("Generos obtidos: "+str(self.spotifyConnection.get_genres(trackID)))

	def test_get_type_by_year(self,year=2010,limit=1):
		response, respJson=self.spotifyConnection.get_type_by_year(_type='track',index=2,year=year,limit=limit)

		print("Response: "+str(response))
		print("test_get_type_by_year: "+str(json.dumps(respJson, indent=4, sort_keys=True)))

	def test_get_artist_top_tracks(self,artistID="0TnOYISbd1XYRBk9myaseg"):
		response, respJson=self.spotifyConnection.get_artist_top_tracks(artistID=artistID)

		print("Response: "+str(response))
		print("test_get_album_tracks: "+str(json.dumps(respJson, indent=4, sort_keys=True)))


	def test_get_album_tracks(self,albumID="4aawyAB9vmqN3uQ7FjRGTy"):
		response, respJson=self.spotifyConnection.get_album_tracks(albumID=albumID)

		print("Response: "+str(response))
		print("test_get_album_tracks: "+str(json.dumps(respJson, indent=4, sort_keys=True)))

class spotifyData():

	def __init__(self,_spotifyConnection=None):

		if _spotifyConnection==None:
			self.spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
		else:
			self.spotifyConnection=_spotifyConnection

		self.logger=logger.setup_logger("spotifyData")

	def get_field_names(self):
		fieldnames=[]

		#Obtendo o nome dos parametros apartir de uma trackID exemplo
		for key in  self.get_track_features("4REjaHRPmVb7btssqChJSy"):
			fieldnames.append(key)

		return fieldnames

	def get_track_features(self,trackID,genre=None,artDict=None):

		self.logger.debug("get_track_features: trackID: "+str(trackID))

		features={}

		response, respJson=self.spotifyConnection.get_track(trackID)

		#features["spotifyAlbum_id"]=respJson['album']["id"]
		features["release_date"]=respJson['album']["release_date"]
		features["popularity"]=respJson['popularity']
		
		self.logger.debug("release_date: "+str(features["release_date"]))
		
		artistID=respJson['artists'][0]["id"]

		if artDict==None:
			#Obtendo total de seguidores do spotify
			response, respJson=self.spotifyConnection.get_artistInfo(artistID)
			features['totalFollowers']=respJson['followers']['total']
		else:
			features['totalFollowers']=artDict['totalFollowers']

		#Obtendo informacoes relacionadas com o audio de alto nivel da múusica
		_spotifyBasicAudioFeature=['danceability','energy','key','mode','speechiness','loudness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature']
	
		response, respJson=self.spotifyConnection.get_audioFeatures(trackID)

		for key in respJson:
			if key in _spotifyBasicAudioFeature:
				features[key]=respJson[key]

		#Obtendo informacoes de audio de baixo nivel simplificadas da musica
		'''_spotifyAudioAnalysisTrack=['num_samples','tempo_confidence','time_signature_confidence','key_confidence','mode_confidence']
		_spotifyAudioAnalysis=['bars','beats','sections','segments','tatums']

		response, respJson=self.spotifyConnection.get_audioAnalysis(trackID)

		for key in respJson['track']:
			if key in _spotifyAudioAnalysisTrack:
				features[key]=respJson['track'][key]

		for key in respJson:
			if key in _spotifyAudioAnalysis:
				features[key]=len(respJson[key])'''

		#Obtendo o genero da musica
		if genre==None:
			features['genres']=self.spotifyConnection.get_genres(trackID)
		else:
			features['genres']=genre

		return features

class spotifyDataTests():

	def __init__(self):
		self.spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
		self.spotifyData=spotifyData(self.spotifyConnection)

	def test_get_track_features(self):
		response, respJson=self.spotifyConnection.trackSearch("Starlight","Muse")
		trackID=respJson['tracks']['items'][0]['id']

		features= self.spotifyData.get_track_features(trackID)

		print("Features: "+str(features))
