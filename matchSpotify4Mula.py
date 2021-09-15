import csv
import logger
import traceback

#carregando dados 4mula
import pandas as pd
df = pd.read_parquet('4mula_metadata.parquet')

for col in df.columns:
	print(col)

#removando algumas features grandes e desnecessarias
#df.drop(['melspectrogram'], axis=1,inplace=True)
df.drop(['music_lyrics'], axis=1,inplace=True)

#conectando as API
import vagalumeAPIConnection
import spotifyAPIConnection
import clientToken

vagalumeConnection=vagalumeAPIConnection.vagalumeAPIConnection(clientToken.VAGALUME_KEY)

spotifyConnection=spotifyAPIConnection.spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)

logging=logger.setup_logger("matchSpotify4Mula")

_4mulaFeatureNames=['music_id', 'music_name', 'music_lang', 'art_id','art_name', 'art_rank', 'main_genre', 'related_genre','musicnn_tags']
_spotifyFeatureNames=['danceability','energy','key','mode','speechiness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature']

fieldnames=_4mulaFeatureNames+_spotifyFeatureNames+['period']+['position']+['mus_rank']

totalDeFalhas=0
tMusicasNLocalizadasSpotify=0
ultMusID='3ade68b8g76dbb0b3'	#somente para caso o processo pare no meio da execucao, este valor sera a ultima musica obtida no csv

with open('matchSpotify4Mula-large.csv', 'a') as arquivo_csv:
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

			ID=item['id']

			response, respJson=spotifyConnection.get_audioFeatures(ID)

			#obtendo atributos da musica do spotify
			for key in respJson:
				if key in _spotifyFeatureNames:
					features[key]=respJson[key]

			#obtendo rank da musica
			try:
				rank,position,period=vagalumeConnection.getSpecificRank(artID, musID, period='monthly', limit=2)
			except:
				totalDeFalhas=totalDeFalhas+1
				logging.warning(' erro ao obter rank: '+str(traceback.format_exc()))
				break

			#features.append(rank)
			features['period']=period
			features['position']=position
			features['mus_rank']=rank

			logging.debug(' salvando amostra')
			#salvando dados do spotify + 4mula
			write.writerow(features)

			#assim que localizar um match saira da iteracao
			break

logging.warning(' totalDeFalhas ao obter rank vagalume: '+str(totalDeFalhas))
logging.warning(' total musicas nao localizadas spotify: '+str(tMusicasNLocalizadasSpotify))