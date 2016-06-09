# import flask and twilio
from flask import Flask, request
import requests, json, re


# used to send messages
from twilio.rest import TwilioRestClient 

# import urllib2  # the lib that handles the url stuff

#
DEBUG = True

# setup twilio login and client for outgoing messages
ACCOUNT_SID = "AC47dfcf040faf1fd544217eb5791310aa" 
AUTH_TOKEN = "08de93e91162fe799b6f8a7ec157b8b5" 

client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN) 

app = Flask(__name__)

# data = urllib2.urlopen('http://download.finance.yahoo.com/d/quotes.csv?s=AAPL+GOOG+MSFT') # it's a file like object and works just like a file
# for line in data: # files are iterable
#     print line



@app.route("/", methods=['POST'])
def parseText():

	# get the number to text back
	from_number = request.values.get("From", None)
	text_contents = request.values.get('Body', None).split(",")

	output = []

	for message in text_contents:
		print(message)
		# capitolize ticker symbol
		tickerSymbol = message.upper()
		# get rid of any characters not a letter or digit
		tickerSymbol = re.sub(r'[\W_]+', '', tickerSymbol)
		
		# hit yfinance to get stock info
		stockInfo = getStockInfo(tickerSymbol)

		# parse the data from yfinance
		stockInfo = parseStockInfo(stockInfo)
		
		# add the parsed data into the output list
		output.append(stockInfo)

	# create the text message and send it
	outputText = parseOutput(output)
	sendText(outputText)

	# text the response back
	return json.dumps(output)

def getStockInfo(tickerSymbol):
	YFinanceURL = 'http://finance.yahoo.com/webservice/v1/symbols/' + tickerSymbol + '/quote?format=json&view=detail'
	response = requests.get(YFinanceURL)

	# get the response JSON 
	response = response.json()
	# print(response)
	# step down to the array of different companies,
	# filtering any useless higher level information
	response = response[unicode("list")][unicode("resources")]

	return response

def parseStockInfo(stockInfo):
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
		# return the parsed data
		return stockInfo

#***
# Function:			parseOutput(output)
#
# Description:		Create a string representation of the stock information
#					to send as text
#
# Input:	(Dict)		Dictionary containing company names and their stock information
# Output:	(String)	A String representation to send to text
def parseOutput(output):
	text = ""
	for company in output:
		text += company["symbol"] + " " + company["price"] + ";  "

	# trim off the trailing spaces and semicolon
	text = text.strip()
	text = text[:-1]
	return text

def sendText(output):
	message = client.messages.create(
	    to="+19149076903", 
	    from_="+19142144724", 
	    body=output,
	   	sid=ACCOUNT_SID,

    )




if __name__ == "__main__":
	app.run(debug=DEBUG)