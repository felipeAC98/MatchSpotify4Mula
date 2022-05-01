from classes.spotifyAPI import spotifyData, spotifyAPIConnection
import sys
import clientToken

def main():

	_spotifyConnection=spotifyAPIConnection(clientToken.CLIENT_ID, clientToken.CLIENT_SECRET)
	_spotifyData=spotifyData(_spotifyConnection=_spotifyConnection)

	for year in range(1990,1995):

		response, respJson=_spotifyConnection.get_type_by_year(year=year,limit=1)

		for track in respJson['tracks']['items']:

			trackID=track['id']

			features=_spotifyData.get_track_features(trackID)

			print(features)
if __name__ == '__main__':
    sys.exit(main())