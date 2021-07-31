import csv
import logger

#carregando dados 4mula
import pandas as pd
df = pd.read_parquet('4mula_metadata.parquet')
#removando algumas features grandes e desnecessarias
df.drop(['melspectrogram'], axis=1,inplace=True)
df.drop(['music_lyrics'], axis=1,inplace=True)

#conectando as API
import vagalumeAPIConnection
import spotifyAPIConnection
import clientToken

vagalumeConnection=vagalumeAPIConnection.vagalumeAPIConnection(clientToken.VAGALUME_KEY)

spotifyConnection=spotifyAPIConnection.spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)

logging=logger.setup_logger("matchSpotify4Mula")

with open('matchSpotify4Mula.csv', 'w') as arquivo_csv:
	write = csv.writer(arquivo_csv, delimiter=',', lineterminator='\n')

	#percorrendo todas linhas do df
	for index, row in df.iterrows():
		trackName=row['music_name']
		artistName=row['art_name']

		musID=row['music_id']
		artID=row['art_id']


		logging.debug(' artistName: '+str(artistName)+ ' trackName: '+str(trackName)+' artID: '+str(artID)+' musID: '+str(musID))

		features=[]
		_4mulaFeatureNames=['music_id', 'music_name', 'music_lang', 'art_id','art_name', 'art_rank', 'main_genre', 'related_genre','musicnn_tags']
		_spotifyFeatureNames=['danceability','energy','key','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature']
		
		#obtendo atributos da musica do 4mula
		for feature in _4mulaFeatureNames:
			try:
				logging.debug(' feature: '+str(row[feature]))
				features.append(row[feature])
			except:
				logging.debug(' feature nao encontrada: '+str(feature))
		#Fazendo o match no spotify
		response, respJson=spotifyConnection.trackSearch(trackName,artistName)

		for item in respJson['tracks']['items'] :
			if item['name']!=trackName:
				logging.debug('nome diferente do esperado')
		
				print('nome diferente do esperado')
				print(trackName)
				print(artistName)
				print(item['name'])
				input("Press Enter to continue...")

			ID=item['id']

			response, respJson=spotifyConnection.get_audioFeatures(ID)

			#obtendo atributos da musica do spotify
			for key in respJson:
				if key in _spotifyFeatureNames:
					features.append(respJson[key])

			#obtendo rank da musica
			rank=vagalumeConnection.getSpecificRank(artID, musID, period='monthly', limit=1)

			features.append(rank)

			#salvando dados do spotify + 4mula
			write.writerow(features)