from classes.spotifyAPI import spotifyData, spotifyAPIConnection
import sys
import clientToken

trackRequestLimit=50

def main():

	defaultNumberTracksByYear=1000
	nTracksIncreasePercent=1

	_spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
	_spotifyData=spotifyData(_spotifyConnection=_spotifyConnection)

	for year in range(1990,1992):

		numberTracksByYear=defaultNumberTracksByYear*nTracksIncreasePercent
		nTracksIncreasePercent=nTracksIncreasePercent+0.05 #aumentando em 5% o numero de musicas por ano
		index=0

		while(index<numberTracksByYear):

			index+=trackRequestLimit

			response, respJson=_spotifyConnection.get_type_by_year(index=index,year=year,limit=trackRequestLimit)

			for track in respJson['tracks']['items']:

				trackID=track['id']

				features=_spotifyData.get_track_features(trackID)

				print(features)
if __name__ == '__main__':
    sys.exit(main())