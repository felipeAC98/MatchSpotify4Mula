from classes.spotifyAPI import spotifyData, spotifyAPIConnection
import sys
import clientToken
import csv
import traceback
import argparse
import json

fileName='spotifyDataset'

def main():

	#Obtencao dos parametros
	parser = argparse.ArgumentParser(description='args')
	parser.add_argument('--genre')						#caso queira se obter somente de um genero especifico
	parser.add_argument('--nAlbumsByYear')
	parser.add_argument('--startYear')
	parser.add_argument('--endYear')
	parser.add_argument('--overwrite')
	args = parser.parse_args()

	genre=None
	nAlbumsByYear=500
	startYear=1985
	endYear=2023
	openFileType='a'
	artDict={}
	trackRequestLimit=50

	if args.genre != None:
		genre=str(args.genre)

	if args.nAlbumsByYear != None:
		nAlbumsByYear=int(args.nAlbumsByYear)
		if trackRequestLimit>nAlbumsByYear:
			trackRequestLimit=nAlbumsByYear

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
		fieldnames=_spotifyData.get_field_names()

		write = csv.DictWriter(csvFile, delimiter=',', lineterminator='\n',fieldnames=fieldnames)

		for year in range(startYear,endYear):

			#numberAlbumsByYear=int(nAlbumsByYear*nTracksIncreasePercent)
			#nTracksIncreasePercent+=0.025 #aumentando em 2.5% o numero de musicas por ano
			index=0

			print("Year: "+str(year)+" nAlbumsByYear: "+str(nAlbumsByYear))

			while(index<nAlbumsByYear):

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
					if artPopularity<20:
						continue

					response, albumJson=_spotifyConnection.get_album_tracks(albumID=albumID)

					try:
						for track in albumJson['items']:
							trackID=track['id']
							features=_spotifyData.get_track_features(trackID,artDict=artDict[artistID])
							write.writerow(features)

					except:
						print(' Erro obtendo track da resposta para o index: '+str(index)+ ' mensagem de erro: '+str(traceback.format_exc()))
						break

				index+=trackRequestLimit
			
if __name__ == '__main__':
    sys.exit(main())