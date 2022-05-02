from classes.spotifyAPI import spotifyData, spotifyAPIConnection
import sys
import clientToken
import csv
import traceback

trackRequestLimit=50
fileName='spotifyDataset'

def main():

	defaultNumberTracksByYear=1000
	nTracksIncreasePercent=1

	_spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
	_spotifyData=spotifyData(_spotifyConnection=_spotifyConnection)

	with open(fileName+'.csv', 'w') as csvFile:

		#Obtendo o nome dos parametros apartir de uma trackID exemplo
		fieldnames=_spotifyData.get_field_names()

		write = csv.DictWriter(csvFile, delimiter=',', lineterminator='\n',fieldnames=fieldnames)

		for year in range(1970,2023):

			numberTracksByYear=int(defaultNumberTracksByYear*nTracksIncreasePercent)
			#nTracksIncreasePercent+=0.025 #aumentando em 2.5% o numero de musicas por ano
			index=0

			print("Year: "+str(year)+" numberTracksByYear: "+str(numberTracksByYear))

			while(index<numberTracksByYear):

				response, respJson=_spotifyConnection.get_type_by_year(index=index,year=year,limit=trackRequestLimit)

				try:

					for track in respJson['tracks']['items']:

						trackID=track['id']

						features=_spotifyData.get_track_features(trackID)

						write.writerow(features)

				except:
					print(' Erro obtendo track da resposta para o index: '+str(index)+ ' mensagem de erro: '+str(traceback.format_exc()))
					break

				index+=trackRequestLimit

if __name__ == '__main__':
    sys.exit(main())