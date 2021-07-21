import csv

#carregando dados 4mula
import pandas as pd
df = pd.read_parquet('4mula_metadata.parquet')
#removendo letra da musica
df.drop(['music_lyrics'], axis=1,inplace=True)

#conectando a API
import spotifyAPIConection
import clientToken

spotifyConnection=spotifyAPIConection.spotifyAPIConection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)

with open('matchSpotify4Mula.csv', 'w') as arquivo_csv:
	write = csv.writer(arquivo_csv, delimiter=',', lineterminator='\n')

	#percorrendo todas linhas do df
	for index, row in df.iterrows():
		trackName=row['music_name']
		artistName=row['art_name']

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

			#salvar dados do spotify + 4mula aqui dentro

			write.writerow(atributos)