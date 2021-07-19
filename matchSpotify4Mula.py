#carregando dados 4mula
import pandas as pd
df = pd.read_parquet('4mula_metadata.parquet')

#conectando a API
import spotifyAPIConection

access_token='BQCELmVlfPoBgVn5cgT8tOOJzR3uznWawKrY8Oi5qNqdng1NWGzVPYP56njzdkwu34PHWxIYZAE-HooTDHzsBHvVNwoO0KjYvb4DPcw3YZ8QgmQAgCz3fDx_b1XGGWW6qmoVIrVuP_0sqIaR9v494XC_Sq8'
conexaoSpotify=spotifyAPIConection.spotifyAPIConection(access_token)

#percorrendo todas linhas do df
for index, row in df.iterrows():
	trackName=row['music_name']
	artistName=row['art_name']

	response, respJson=conexaoSpotify.trackSearch(trackName,artistName)
	print('Nome buscado: '+ trackName)

	for item in respJson['tracks']['items'] :
		print('Nome no spotify: '+ item['name'])
		#print(item['id'])

		if item['name']!=trackName:
			print('nome diferente do esperado')

		input("Press Enter to continue...")
	
	print('\n')
