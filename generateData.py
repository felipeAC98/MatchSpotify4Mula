from classes.spotifyAPI import spotifyData, spotifyAPIConnection
import sys
import clientToken
import csv
import traceback
import argparse

trackRequestLimit=50
fileName='spotifyDataset'

def main():

	#Obtencao dos parametros
	parser = argparse.ArgumentParser(description='args')
	parser.add_argument('--genre')						#caso queira se obter somente de um genero especifico
	parser.add_argument('--nMusicsByYear')
	parser.add_argument('--startYear')
	parser.add_argument('--endYear')
	parser.add_argument('--overwrite')
	args = parser.parse_args()

	genre=None
	nMusicsByYear=1000
	startYear=1970
	endYear=2023
	openFileType='a'

	if args.genre != None:
		genre=str(args.genre)

	if args.nMusicsByYear != None:
		nMusicsByYear=int(args.nMusicsByYear)

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

			numberTracksByYear=int(nMusicsByYear*nTracksIncreasePercent)
			#nTracksIncreasePercent+=0.025 #aumentando em 2.5% o numero de musicas por ano
			index=0

			print("Year: "+str(year)+" numberTracksByYear: "+str(numberTracksByYear))

			while(index<numberTracksByYear):

				response, respJson=_spotifyConnection.get_type_by_year(index=index,year=year,limit=trackRequestLimit,genre=genre)

				try:

					for track in respJson['tracks']['items']:

						trackID=track['id']

						features=_spotifyData.get_track_features(trackID,genre=genre)

						write.writerow(features)

				except:
					print(' Erro obtendo track da resposta para o index: '+str(index)+ ' mensagem de erro: '+str(traceback.format_exc()))
					break

				index+=trackRequestLimit

if __name__ == '__main__':
    sys.exit(main())