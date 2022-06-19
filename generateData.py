from classes.spotifyAPI import spotifyData, spotifyAPIConnection
import sys
import clientToken
import csv
import traceback
import argparse
import json
from time import sleep as sleep

def main():

	#Obtencao dos parametros
	parser = argparse.ArgumentParser(description='args')
	parser.add_argument('--genre')						#caso queira se obter somente de um genero especifico
	parser.add_argument('--nItemsByYear')
	parser.add_argument('--startYear')
	parser.add_argument('--endYear')
	parser.add_argument('--overwrite')
	parser.add_argument('--filename')
	args = parser.parse_args()

	genre=None
	artDict={}
	nItemsByYear=500
	startYear=1985
	endYear=2023
	openFileType='a'
	index=0
	trackRequestLimit=50

	if args.filename != None:
		fileName=str(args.filename)
	else:
		fileName='spotifyDataset'

	if args.genre != None:
		genre=str(args.genre)

	if args.nItemsByYear != None:
		nItemsByYear=int(args.nItemsByYear)
		if trackRequestLimit>nItemsByYear:
			trackRequestLimit=nItemsByYear

	if args.startYear != None:
		startYear=int(args.startYear)

	if args.endYear != None:
		endYear=int(args.endYear)

	if args.overwrite != None and str(args.overwrite).lower() != "false" :
		openFileType='w'

	nTracksIncreasePercent=1

	_spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
	_spotifyData=spotifyData(_spotifyConnection=_spotifyConnection)

	with open(fileName+'.csv', openFileType) as csvFile:

		#Obtendo o nome dos parametros apartir de uma trackID exemplo
		fieldnames=_spotifyData.get_track_field_names()
		write = csv.DictWriter(csvFile, delimiter='|', lineterminator='\n',fieldnames=fieldnames)

		for year in range(startYear,endYear):

			#numberAlbumsByYear=int(nItemsByYear*nTracksIncreasePercent)
			#nTracksIncreasePercent+=0.025 #aumentando em 2.5% o numero de musicas por ano
			print("Year: "+str(year)+" nItemsByYear: "+str(nItemsByYear))

			while(index<nItemsByYear):
				if genre==None:
					write_tracks_by_year(_spotifyConnection,_spotifyData,write,year,trackRequestLimit,nItemsByYear,index,artDict)
				else: 
					write_tracks_by_genre(_spotifyConnection,_spotifyData,write,year,trackRequestLimit,nItemsByYear,index,genre)
				
				index+=trackRequestLimit

def write_tracks_by_year(_spotifyConnection,_spotifyData,write,year,trackRequestLimit,nItemsByYear,index,artDict):
	response, albunsJson=_spotifyConnection.get_type_by_year( _type='album',index=index,year=year,limit=trackRequestLimit)

	for album in albunsJson['albums']['items']:
		artistID=album['artists'][0]['id']
		albumID=album['id']

		if artistID in artDict.keys():
			artPopularity=artDict[artistID]['artPopularity']
		else:
			response, artistJson=_spotifyConnection.get_artistInfo(artistID)
			artPopularity=artistJson['popularity']
			totalFollowers=artistJson['followers']['total']
			artDict[artistID]={'artPopularity':artPopularity,'totalFollowers':totalFollowers}

		#Caso possua pouca popularidade nao sera utilizado
		if artPopularity<15:
			continue	
		response, albumJson=_spotifyConnection.get_album_tracks(albumID=albumID)
		try:
			write_tracks_from_json(write,_spotifyData,albumJson)
		except:
			print(' Erro obtendo track da resposta para o index: '+str(index)+ ' mensagem de erro: '+str(traceback.format_exc()))

		index+=trackRequestLimit	

def write_tracks_by_genre(_spotifyConnection,_spotifyData,write,year,trackRequestLimit,nItemsByYear,index,genre):
	response, respJson=_spotifyConnection.get_type_by_year(index=index,year=year,limit=trackRequestLimit,genre=genre)
	try:
		write_tracks_from_json(write,_spotifyData,respJson['tracks'],genre)

	except:
		print(' Erro obtendo track da resposta para o index: '+str(index)+ ' mensagem de erro: '+str(traceback.format_exc()))

def write_tracks_from_json(write,_spotifyData,json,genre=None):
	for track in json['items']:
		sleep(1)
		trackID=track['id']
		features=_spotifyData.get_track_features(trackID,genre=genre)
		write.writerow(features)

if __name__ == '__main__':
    sys.exit(main())
