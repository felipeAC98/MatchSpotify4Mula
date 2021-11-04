import csv
import logger
import traceback
import threading
#conectando as API
import vagalumeAPIConnection
import spotifyAPIConnection
import clientToken

def matchSpotify4Mula():

	#carregando dados 4mula
	import pandas as pd
	arquivoBase='4mula_metadata'
	df = pd.read_parquet('4mula_metadata.parquet')

	for col in df.columns:
		print(col)

	logging=logger.setup_logger("matchSpotify4Mula")

	#removando algumas features grandes e desnecessarias
	try:
		df.drop(['melspectrogram'], axis=1,inplace=True)
	except:
		logging.warning(' feature melspectrogram nao encontrada para dropar: '+str(traceback.format_exc()))

	df.drop(['music_lyrics'], axis=1,inplace=True)

	vagalumeConnection=vagalumeAPIConnection.vagalumeAPIConnection(clientToken.VAGALUME_KEY)

	spotifyConnection=spotifyAPIConnection.spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)

	_4mulaFeatureNames=['music_id', 'music_name', 'music_lang', 'art_id','art_name', 'art_rank4Mula', 'main_genre', 'related_genre','musicnn_tags']

	_spotifyBasicAudioFeature=['danceability','energy','key','mode','speechiness','loudness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature']
	_spotifyAudioAnalysisTrack=['num_samples','tempo_confidence','time_signature_confidence','key_confidence','mode_confidence']
	_spotifyAudioAnalysis=['bars','beats','sections','segments','tatums']

	fieldnames=_4mulaFeatureNames+['spotify_trackID']+_spotifyBasicAudioFeature+['spotifyAlbum_id']+['release_date'] +['popularity']+['spotifyArt_id']+_spotifyAudioAnalysisTrack+_spotifyAudioAnalysis+['period']+['position']+['mus_rank']+['art_rank']

	totalDeFalhas=0
	tMusicasNLocalizadasSpotify=0
	ultMusID=0	#somente para caso o processo pare no meio da execucao, este valor sera a ultima musica obtida no csv
	totMus=0

	with open(arquivoBase+'.csv', 'a') as arquivo_csv:

		write = csv.DictWriter(arquivo_csv, delimiter=',', lineterminator='\n',fieldnames = fieldnames)

		#percorrendo todas linhas do df
		for index, row in df.iterrows():
			logging.debug(' \n')

			trackName=row['music_name']
			artistName=row['art_name']

			musID=row['music_id']
			artID=row['art_id']


			logging.debug(' 4Mula artistName: '+str(artistName)+ ' 4Mula trackName: '+str(trackName)+' artID: '+str(artID)+' musID: '+str(musID))

			features={}

			#obtendo atributos da musica do 4mula
			for feature in _4mulaFeatureNames:
				try:
					logging.debug(' feature: '+str(row[feature]))
					features[feature]=row[feature]
				except:
					logging.debug(' feature nao encontrada: '+str(feature))
			
			if ultMusID!=0 and features['music_id'] != ultMusID:
				logging.debug(' musica ja presente: '+str(features['music_name']))
				continue

			else:
				ultMusID=0

			#Inicializando thread para obter os valores obtidos da API do vagalume
			vagalumeFeatures={'mus_rank':0,'art_rank':0,'position':0,'period':0}
			prevPosition=vagalumeFeatures['position']
			vagalumeThread = threading.Thread(target=vagalumeConnection.getNSetSpecificRank,args=(vagalumeFeatures,artID, musID,'monthly', 2,))
			vagalumeThread.start()

			#Fazendo o match no spotify
			response, respJson=spotifyConnection.trackSearch(trackName,artistName)

			if len(respJson['tracks']['items'])<1:
				tMusicasNLocalizadasSpotify=tMusicasNLocalizadasSpotify+1
				logging.debug(' musica nao localizada no spotify')

			for item in respJson['tracks']['items'] :
				
				logging.debug(' musica Spotify localizada: '+str(item['name']))

				#Somente matchs exatamente iguais serao considerados - nao considerando caps lock ou assentuacao
				if len(item['name']) > len(trackName)+6 or len(item['name']) < len(trackName)-6:
					logging.debug(' nome diferente, descartando musica Spotify')
					continue

				features['spotify_trackID']=item['id']

				#obtendo atributos basicos da musica do spotify ==== _spotifyBasicAudioFeature
				response, respJson=spotifyConnection.get_audioFeatures(features['spotify_trackID'])

				for key in respJson:
					if key in _spotifyBasicAudioFeature:
						features[key]=respJson[key]

				#obtendo atributos basicos da musica do spotify ==== _spotifyTrackInfoAlbum e relacionados
				response, respJson=spotifyConnection.get_track(features['spotify_trackID'])

				features["spotifyAlbum_id"]=respJson['album']["id"]
				features["release_date"]=respJson['album']["release_date"]
				features["popularity"]=respJson['popularity']
				features["spotifyArt_id"]=respJson['artists'][0]["id"]

				#obtendo atributos basicos da musica do spotify ==== _spotifyAudioAnalysisTrack
				response, respJson=spotifyConnection.get_audioAnalysis(features['spotify_trackID'])

				for key in respJson['track']:
					if key in _spotifyAudioAnalysisTrack:
						features[key]=respJson['track'][key]

				#obtendo atributos basicos da musica do spotify ==== _spotifyAudioAnalysis
				for key in respJson:
					if key in _spotifyAudioAnalysis:
						features[key]=len(respJson[key])

				#obtendo rank da musica == VAGALUME
				try:
					#musRank,artRank,position,period=vagalumeConnection.getSpecificRank(artID, musID, period='monthly', limit=2)
					vagalumeThread.join()

				except:
					totalDeFalhas=totalDeFalhas+1
					logging.warning(' erro ao obter rank: '+str(traceback.format_exc()))
					break

				if(prevPosition==vagalumeFeatures['position']):
					totalDeFalhas=totalDeFalhas+1
					logging.warning(' erro ao obter rank vagalume')
					break

				#features.append(rank)
				features['period']=vagalumeFeatures['period']
				features['position']=vagalumeFeatures['position']
				features['mus_rank']=vagalumeFeatures['mus_rank']
				features['art_rank']=vagalumeFeatures['art_rank']

				logging.debug(' salvando amostra')
				#salvando dados do spotify + 4mula
				write.writerow(features)

				print("Total de musicas: "+str(totMus))
				totMus+=1
				#assim que localizar um match saira da iteracao
				break

	logging.warning(' totalDeFalhas ao obter rank vagalume: '+str(totalDeFalhas))
	logging.warning(' total musicas nao localizadas spotify: '+str(tMusicasNLocalizadasSpotify))

matchSpotify4Mula()