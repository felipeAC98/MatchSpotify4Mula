import requests
import json
import logger

class vagalumeAPIConnection():

	def __init__(self,APIKEY):

		self.url="https://api.vagalume.com.br/"

		self.APIKEY=str(APIKEY)

		self.logger=logger.setup_logger("vagalumeAPI")

	def sendRequest(self, session, urlAttribute):

		self.logger.debug("sendRequest")

		key='&apikey={'+self.APIKEY+'}'

		urlAttribute=urlAttribute+key

		url=self.url+session+str(urlAttribute)

		response = requests.get(url=url)

		self.logger.debug("url:"+ str(url))

		self.logger.debug("response: " + str(response))

		self.logger.debug("response.json(): " + str(response.json()))

		return response, response.json()

	def getGeneralRank(self, rankType=None, period=None, periodVal=None, scope=None, limit=10):

		self.logger.debug("getGeneralRank")

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

		return self.sendRequest(session, urlAttribute)

	def getSpecificRank(self, artID, musID, period='monthly', limit=10, periodStart=None, periodEnd=None):

		self.logger.debug("getSpecificRank")

		session='rankArtist.php?'

		urlAttribute='artID='+str(artID)

		urlAttribute=urlAttribute+'&musID='+str(musID)

		urlAttribute=urlAttribute+'&period='+str(period)

		if  periodStart!=None and periodEnd!=None:

			urlAttribute=urlAttribute+'&periodStart='+str(periodStart)

			urlAttribute=urlAttribute+'&periodEnd='+str(periodEnd)

		urlAttribute=urlAttribute+'&limit='+str(limit)

		response, respJson= self.sendRequest(session, urlAttribute)
		#print(json.dumps(respJson, indent=4, sort_keys=True))

		period=period[:-2]

		musicLen=len(respJson['music'][period][musID])

		rank=respJson['music'][period][musID][musicLen-1]['rank']		#Contém a pontuação da música baseado na quantidade de acessos.
		periodR=respJson['music'][period][musID][musicLen-1]['period']
		position=respJson['music'][period][musID][musicLen-1]['pos'] 	#Contém a posição da música no rank de top músicas do Vagalume.

		#self.logger.debug("getSpecificRank: period: "+str(periodR))	

		return rank, position, periodR

def test_SpecificRank():

	#conectando a API
	import clientToken
	import json

	APIKEY=clientToken.VAGALUME_KEY

	vagalumeConnection=vagalumeAPIConnection(APIKEY)

	#response, respJson=vagalumeConnection.getGeneralRank(rankType='mus', period='month', periodVal='202106', scope='all', limit=2)

	#print(json.dumps(respJson, indent=4, sort_keys=True))

	artID='3ade68b7g6b960ea3'
	musicID='3ade68b8g42c34fa3'

	rank=vagalumeConnection.getSpecificRank(artID,musicID, period='monthly',limit=1,  periodStart='2020-01', periodEnd='2020-02')

	print(rank)

	return None