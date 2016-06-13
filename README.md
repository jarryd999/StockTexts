# StockTexts
Python/Flask app to get stock information via text

##Description
This program will take in a text with one or more comma seperated stock ticker symbols and send a text message back with the stock current stock data.  If the keyword `detail` is provided in the same format as a ticker symbol, the program will spit back more detailed stock data.

##Installation & Deployment
###Manual
run `git clone https://github.com/jarryd999/StockTexts'.  Enter your twilio credentials in the TwilioCredentials.py file.  After that, you will want to run the app ('python app.py') on a server of your choice, exposing port 5001.

###Container
Currently, the container is not open to the public until I can figure out how to handle credentials.

###Example Text
`googl, msft, aapl,detail'
