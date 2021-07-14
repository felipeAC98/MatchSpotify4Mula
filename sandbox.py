import requests

url="https://api.spotify.com/v1/audio-features/"
access_token='BQBTuBansNMF8sitjnFsCf_zYhMiToX9Aq0rNKwHA0UfQ4SPQlLAL4vKH5PA8ypH9wbwLbP75yv2-slJpH_Hjoo5pdbNuWNnxx9SuZqcCG_0DVisJqGcT_nscUmCgc-a_VYhUUk0Drr6cIBc8coJORroJxI'
header={
	'Authorization': 'Bearer {token}'.format(token=access_token)
}
id='4JpKVNYnVcJ8tuMKjAj50A'

response = requests.get(url=url+id,headers=header )

print(response)

respJson=response.json()

print(respJson)

for item in respJson:
	print(respJson[item])