import requests, json, re
# import flask and twilio
from flask import Flask, request
from twilio.rest import TwilioRestClient 

# Environment Variables
DEBUG = True

# setup twilio login and client for outgoing messages
ACCOUNT_SID = "AC47dfcf040faf1fd544217eb5791310aa" 
AUTH_TOKEN = "08de93e91162fe799b6f8a7ec157b8b5" 

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

app = Flask(__name__)

# for line in data: # files are iterable
#     print line



@app.route("/", methods=['POST'])
def parseText():

	# get the number to text back
	from_number = request.values.get("From", None)
	text_contents = request.values.get('Body', None).split(",")

	output = []
	tickerSymbolList = []
	moreInfo = False

	for message in text_contents:
		# capitolize ticker symbol
		tickerSymbol = message.upper()

		# get rid of any characters not a letter or digit
		allSymbols = re.sub(r'[\W_]+', '', tickerSymbol)

		#check for the detail option and set the flag if present
		if tickerSymbol == 'DETAIL':
			moreInfo = True
			continue
			
		tickerSymbolList.append(tickerSymbol)
	# hit yfinance to get stock info
	stockInfo = getStockInfo(tickerSymbolList)


	# parse the data from yfinance
	parsedStockInfo = parseStockInfo(stockInfo)

	# create the text message and send it
	outputText = parseOutput(parsedStockInfo)
	sendText(outputText)

	# # text the response back
	return json.dumps(output)



#########################################################################################
# Function:			getStockInfo(tickerSymbol)											#
#																						#
# Description:		Hit the finance API once, requesting all companies' stock info		#
#																						#
# Input:	(List)	Contains all the stock ticker symbols								#
# Output:	(Dict)	Contains requested stock information for all companies				#
#########################################################################################
def getStockInfo(tickerSymbols):
	#build a string for the URL query of all the ticker symbols
	PARAMS = ""
	print tickerSymbols
	for symbol in tickerSymbols:
		PARAMS += symbol + ','
	#trim the last comma
	PARAMS = PARAMS[:-1]

	YFinanceURL = 'http://finance.yahoo.com/webservice/v1/symbols/' + PARAMS + '/quote?format=json&view=detail'
	response = requests.get(YFinanceURL)

	# get the response JSON 
	response = response.json()

	# step down to the array of different companies,
	# filtering any useless higher level information
	response = response[unicode("list")][unicode("resources")]

	return response



#########################################################################################
# Function:			parseStockInfo(stockInfo)											#
#																						#
# Description:		Create a string representation of the stock information				#
#					to send as text 													#
#																						#
# Input:	(Dict)	Contains data from the finance API									#
# Output:	(Dict)	Contains only requested stock information 							#
#########################################################################################
def parseStockInfo(stockInfo):
	output = []

	# loop through all the stocks in the response and extract relevant data
	for stock in stockInfo:
		stock = stock[unicode("resource")][unicode("fields")]

		# change = stock["change"]
		price = stock[unicode("price")]
		price = float(price)

		# format to currency
		price = '${:,.2f}'.format(price)


		name = stock[unicode("symbol")]

		# if statements for options (subscribe, more info, etc)

		stockInfo = {'symbol': name, 'price': price} 
		output.append(stockInfo)
	
	return output

#########################################################################################
# Function:				parseOutput(output)												#
#																						#
# Description:			Create a string representation of the stock information			#
#						to send as text 												#
#																						#
# Input:	(Dict)		Contains company names and their stock information				#
# Output:	(String)	A String representation to send to text 						#
#########################################################################################
def parseOutput(output):
	text = ""
	for company in output:
		text += company["symbol"] + " " + company["price"] + ";  "

	# trim off the trailing spaces and semicolon
	text = text.strip()
	text = text[:-1]
	return text


#########################################################################################
# Function:					sendText(output)											#
#																						#
# Description:				Make a call to the twilio API to reply via SMS with the 	#
#							requested stock information									#
#																						#
# Input:	(String)		Dictionary containing company names and their stock 		#
#							information 												#
# Output:	(None)																		#
#########################################################################################
def sendText(output):
	message = client.messages.create(
	    to="+19149076903", 
	    from_="+19142144724", 
	    body=output,
	   	sid=ACCOUNT_SID,

    )




if __name__ == "__main__":
	app.run(debug=DEBUG)