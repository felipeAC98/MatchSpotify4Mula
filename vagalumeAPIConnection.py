import requests

class vagalumeAPIConnection():

	def __init__(self,APIKEY):

		self.url="https://api.vagalume.com.br/"

		self.APIKEY=str(APIKEY)

	def sendRequest(self, session, urlAttribute):
		
		url=self.url+session+str(urlAttribute)

		print(url)
		response = requests.get(url=url)

		return response, response.json()

	def getGeneralRank(self, rankType=None, period=None, periodVal=None, scope=None, limit=10):

		session='rank.php?'

		urlAttribute=''

		if rankType!=None:
			urlAttribute=urlAttribute+'type='+str(rankType)

		if period!=None:
			urlAttribute=urlAttribute+'&period='+str(period)
	
		if periodVal!=None:
			urlAttribute=urlAttribute+'&periodVal='+str(periodVal)
	
		if scope!=None:
			urlAttribute=urlAttribute+'&scope='+str(scope)

		urlAttribute=urlAttribute+'&limit='+str(limit)

		key='apikey={'+self.APIKEY+'}'

		urlAttribute=urlAttribute+key

		return self.sendRequest(session, urlAttribute)

	def getSpecificRank(self, artID, musID, period='monthly', limit=10, periodStart=None, periodEnd=None):

		session='rankArtist.php?'

		urlAttribute='artID='+str(artID)

		urlAttribute=urlAttribute+'&musID='+str(musID)

		urlAttribute=urlAttribute+'&period='+str(period)

		urlAttribute=urlAttribute+'&limit='+str(limit)

		if periodStart!=None and periodEnd!=None:

			urlAttribute=urlAttribute+'&periodStart='+str(periodStart)

			urlAttribute=urlAttribute+'&periodEnd='+str(periodEnd)

		return self.sendRequest(session, urlAttribute)

def test_SpecificRank():

	#conectando a API
	import clientToken
	import json

	APIKEY=clientToken.VAGALUME_KEY

	vagalumeConnection=vagalumeAPIConnection(APIKEY)

	#response, respJson=vagalumeConnection.getGeneralRank(rankType='mus', period='month', periodVal='202106', scope='all', limit=10)

	#print(json.dumps(respJson, indent=4, sort_keys=True))

	artID='3ade68b6g2480fda3'
	musicID='3ade68b8g9410afa3'

	response, respJson=vagalumeConnection.getSpecificRank(artID,musicID, period='monthly', limit=10, periodStart='2021-05', periodEnd='2021-07')

	print(response)
	print(json.dumps(respJson, indent=4, sort_keys=True))

	return None