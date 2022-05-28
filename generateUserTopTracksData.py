from classes.spotifyAPI import spotifyData, spotifyAPIConnection
import sys
import clientToken
import csv
import traceback
import argparse
import json
from time import sleep as sleep

fileName='userTopItemsDataset'

def main():

	#Obtencao dos parametros
	parser = argparse.ArgumentParser(description='args')
	parser.add_argument('--overwrite')
	args = parser.parse_args()

	openFileType='a'
	artDict={}
	trackRequestLimit=1
	position=0

	if args.overwrite != None and str(args.overwrite).lower() != "false" :
		openFileType='w'

	nTracksIncreasePercent=1

	_spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
	_spotifyData=spotifyData(_spotifyConnection=_spotifyConnection)

	with open(fileName+'.csv', openFileType) as csvFile:

		#Obtendo o nome dos parametros apartir de uma trackID exemplo
		fieldnames=_spotifyData.get_track_field_names()
		fieldnames.append('mus_name')
		fieldnames.append('art_name')
		fieldnames.append('position')

		write = csv.DictWriter(csvFile, delimiter='|', lineterminator='\n',fieldnames=fieldnames)

		for index in range(0,50):

			response, json=_spotifyConnection.get_user_top_items(_type="tracks",limit=trackRequestLimit,index=index)

			for track in json['items']:
				trackID=track['id']
				print(track['name'])
				features=_spotifyData.get_track_features(trackID)
				features['mus_name']=track['name']
				features['art_name']=track['artists'][0]['name']
				features['position']=position
				position+=1
				write.writerow(features)

if __name__ == '__main__':
    sys.exit(main())
