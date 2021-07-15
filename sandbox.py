import spotifyAPIConection

access_token='BQBmJm6yFq-uWfSkBHQmgcEhM-GQkdmaeGL29lyBOo143QPVWW9OW8sSK7md0BXxH7CtUdYEYkpw1R2Zda-01CFb4OHFGSfWtPCQobVLHmrDjVNAwtgfLJrY7yieCZUyAXVUfkcE4623OFb1D405wTu4HSg'
conexaoSpotify=spotifyAPIConection.spotifyAPIConection(access_token)

session="audio-features/"
id='4JpKVNYnVcJ8tuMKjAj50A'

artistName='Nicki Minaj'
trackName='Good Form'

response, respJson=conexaoSpotify.trackSearch(trackName,artistName)

for item in respJson['tracks']['items'] :
	print(item['name'])
	print(item['id'])

	print('\n')