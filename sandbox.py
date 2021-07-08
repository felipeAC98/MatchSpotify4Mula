import requests

url="https://api.spotify.com/v1/audio-features/"
access_token='BQC0Hjc2MR1HzX5h-fMzyeh5FJGofHi4I2ek7w_K4UfLDBDl9a6lD1U9PjX16qA18HbbS1GuLCBq_lrCc2fz14QxFgPmylPiLFhYcTY8hgBXYOUnViTMx1HNWIvxoQKOrBd5KvIdG49ypaxntXW6ud8pGcM'
header={
	'Authorization': 'Bearer {token}'.format(token=access_token)
}
id='6i0V12jOa3mr6uu4WYhUBr'

response = requests.get(url=url+id,headers=header )

print(response)

respJson=response.json()

print(respJson)

for item in respJson:
	print(respJson[item])