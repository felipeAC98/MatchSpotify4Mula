import csv
import logger
import traceback
import threading
#conectando as API
import vagalumeAPIConnection
import spotifyAPIConnection
import clientToken

def spotifyFeatures():

	#carregando dados 4mula
	import pandas as pd
	arquivoBase='spotifyOnlyFeatures'

	logging=logger.setup_logger("spotifyFeatures")

	spotifyConnection=spotifyAPIConnection.spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)

	_4mulaFeatureNames=['music_id', 'music_name', 'music_lang', 'art_id','art_name', 'art_rank4Mula', 'main_genre', 'related_genre','musicnn_tags']

	_spotifyBasicAudioFeature=['danceability','energy','key','mode','speechiness','loudness','acousticness','instrumentalness','liveness','valence','tempo','duration_ms','time_signature']
	_spotifyAudioAnalysisTrack=['num_samples','tempo_confidence','time_signature_confidence','key_confidence','mode_confidence']
	_spotifyAudioAnalysis=['bars','beats','sections','segments','tatums']

	fieldnames=_4mulaFeatureNames+['spotify_trackID']+_spotifyBasicAudioFeature+['spotifyAlbum_id']+['release_date'] +['popularity']+['spotifyArt_id']+_spotifyAudioAnalysisTrack+_spotifyAudioAnalysis+['period']+['position']+['mus_rank']+['art_rank']

	df = pd.read_csv('4mula_metadata_generated.csv', sep=',', names = fieldnames)
	for col in df.columns:
		print(col)

	totalDeFalhas=0
	tMusicasNLocalizadasSpotify=0
	ultMusID=0	#somente para caso o processo pare no meio da execucao, este valor sera a ultima musica obtida no csv
	totMus=0

	spotifyFeatures=['spotify_trackID','spotify_artID','totalFollowers','artPopularity']

	with open(arquivoBase+'.csv', 'a') as arquivo_csv:

		write = csv.DictWriter(arquivo_csv, delimiter=',', lineterminator='\n',fieldnames = spotifyFeatures)

		#percorrendo todas linhas do df
		for index, row in df.iterrows():
			logging.debug(' \n')

			spotify_trackID=row['spotify_trackID']
			spotify_artID=row['spotifyArt_id']

			#logging.debug(' 4Mula artistName: '+str(artistName)+ ' 4Mula trackName: '+str(trackName)+' artID: '+str(artID)+' musID: '+str(musID))

			features={}

			features['spotify_trackID']=spotify_trackID
			features['spotify_artID']=spotify_artID

			#obtendo atributos basicos da musica do spotify ==== _spotifyTrackInfoAlbum e relacionados
			response, respJson=spotifyConnection.get_artistInfo(features['spotify_artID'])
			
			if(response.status_code!=200):
				totalDeFalhas=totalDeFalhas+1
				logging.warning(' erro ao obter informacoes do spotify')
				continue
			
			features['totalFollowers']=respJson['followers']['total']
			features['artPopularity']=respJson['popularity']

			logging.debug(' salvando amostra')
			#salvando dados do spotify + 4mula
			write.writerow(features)

			print("Total de musicas: "+str(totMus))
			totMus+=1

	logging.warning(' totalDeFalhas ao obter rank vagalume: '+str(totalDeFalhas))
	logging.warning(' total musicas nao localizadas spotify: '+str(tMusicasNLocalizadasSpotify))

spotifyFeatures()