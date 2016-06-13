import requests, json, re
# import flask and twilio
from flask import Flask, request
from twilio.rest import TwilioRestClient 

# Environment Variables
DEBUG = True

STOCK_DETAILS = { 
	"change" : 			 {	"showUser" : False,	"displayName": "Change"			},
	"chg_percent" : 	 {	"showUser" : True, "displayName": ""				},
	"day_high" : 		 {	"showUser" : True, "displayName": "High"			},
	"day_low" : 		 {	"showUser" : False,	"displayName": "Low"			},
	"issuer_name" : 	 {	"showUser" : False,	"displayName": ""				},
	"issuer_name_lang" : {	"showUser" : False,	"displayName": ""				},
	"name" : 			 {	"showUser" : False,	"displayName": "Name"			},
	"price" : 			 {	"showUser" : False,	"displayName": "Price"			},
	"symbol" : 			 {	"showUser" : False,	"displayName": "Symbol"			},
	"ts" : 				 {	"showUser" : False,	"displayName": "Recent as of"	},
	"type" : 			 {	"showUser" : False,	"displayName": "Type"			},
	"utctime" : 		 {	"showUser" : False,	"displayName": ""				},
	"volume" : 			 {	"showUser" : False,	"displayName": "Volume"			},
	"year_high" : 		 {	"showUser" : True,	"displayName": "Year High"		},
	"year_low" : 		 {	"showUser" : False,	"displayName": "Year Low"		}
}

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
		tickerSymbol = message.upper().strip()



		# get rid of any characters not a letter or digit
		tickerSymbol = re.sub(r'[\W_]+', '', tickerSymbol)

		#check for the detail option and set the flag if present
		if tickerSymbol == 'DETAIL':
			moreInfo = True
			continue
		# otherwise add the ticker symbol to the list
		tickerSymbolList.append(tickerSymbol)
	
	# hit yfinance to get stock info
	stockInfo = getStockInfo(tickerSymbolList, moreInfo)


	# parse the data from yfinance
	parsedStockInfo = parseStockInfo(stockInfo, moreInfo)

	# create the text message and send it
	outputText = parseOutput(parsedStockInfo, moreInfo)
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
def getStockInfo(tickerSymbols, moreInfo):
	#build a string for the URL query of all the ticker symbols
	PARAMS = ""
	for symbol in tickerSymbols:
		PARAMS += symbol + ','
	#trim the last comma
	PARAMS = PARAMS[:-1]

	YFinanceURL = 'http://finance.yahoo.com/webservice/v1/symbols/' + PARAMS + '/quote?format=json'

	# add parameter for detailed view
	if moreInfo:
		YFinanceURL += '&view=detail'


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
def parseStockInfo(stockInfo, moreInfo):
	output = []

	# loop through all the stocks in the response and extract relevant data
	for stock in stockInfo:
		stock = stock[unicode("resource")][unicode("fields")]

		# grab name and price, format price
		name = stock[unicode("symbol")]
		price = stock[unicode("price")]
		price = float(price)
		# format to currency
		price = formatCurrency(price)
		stockInfo = {'symbol': name, 'price': price} 


		# If more info requested, include other details about stock
		if moreInfo:
			for detail in STOCK_DETAILS:
				displayName = STOCK_DETAILS[detail]['displayName']
				if STOCK_DETAILS[detail]['showUser']:
					stockInfo[displayName] = stock[unicode(detail)]


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
def parseOutput(output, moreInfo):
	text = ""
	for company in output:
		text += company["symbol"] + " " + company["price"]

		if moreInfo:
			for detail in company:
				if detail == "symbol" or detail == "price":
					continue
				text += detail + ": " + company[detail] + ","
		text += "; "

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


def formatCurrency(inString):
	return '${:,.2f}'.format(inString)




if __name__ == "__main__":
	app.run(debug=DEBUG, host='0.0.0.0', port=5001)