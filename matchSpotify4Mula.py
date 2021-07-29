import csv

#carregando dados 4mula
import pandas as pd
df = pd.read_parquet('4mula_metadata.parquet')
#removendo letra da musica
df.drop(['music_lyrics'], axis=1,inplace=True)

#conectando as API
import vagalumeAPIConnection
import spotifyAPIConnection
import clientToken

vagalumeConnection=vagalumeAPIConnection.vagalumeAPIConnection(clientToken.VAGALUME_KEY)

spotifyConnection=spotifyAPIConnection.spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)

with open('matchSpotify4Mula.csv', 'w') as arquivo_csv:
	write = csv.writer(arquivo_csv, delimiter=',', lineterminator='\n')

	#percorrendo todas linhas do df
	for index, row in df.iterrows():
		trackName=row['music_name']
		artistName=row['art_name']

		musID=row['music_id']
		artID=row['art_id']

		atributos=[]

		#obtendo atributos da musica do 4mula
		for atributo in row:
			atributos.append(atributo)

		response, respJson=spotifyConnection.trackSearch(trackName,artistName)

		for item in respJson['tracks']['items'] :
			if item['name']!=trackName:
				print('nome diferente do esperado')
				print(trackName)
				print(artistName)
				print(item['name'])
				input("Press Enter to continue...")

			ID=item['id']

			response, respJson=spotifyConnection.get_audioFeatures(ID)

			#obtendo atributos da musica do spotify
			for chave in respJson:
				atributos.append(respJson[chave])

			#obtendo rank da musica
			rank=vagalumeConnection.getSpecificRank(artID, musID, period='monthly', limit=1)

			atributos.append(rank)

			#salvando dados do spotify + 4mula
			write.writerow(atributos)