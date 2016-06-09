import unittest
from app import app

class TestStockTexts(unittest.TestCase):
	def test_parseText(self):
		print "\n"
		self.test_app = app.test_client()
		response = self.test_app.post('/', data={'From': '9149076903', 'Body':'GOOGL,BRK.A'})
		self.assertEquals(response.status, "200 OK")

		print(response.get_data())
		test_resource ={
			"resource" : { 
				"classname" : "Quote",
				"fields" : { 
					"change" : "11.839966",
					"chg_percent" : "1.619495",
					"day_high" : "743.809998",
					"day_low" : "735.765015",
					"issuer_name" : "Alphabet Inc.",
					"issuer_name_lang" : "Alphabet Inc.",
					"name" : "Alphabet Inc.",
					"price" : "742.929993",
					"symbol" : "GOOGL",
					"ts" : "1465416000",
					"type" : "equity",
					"utctime" : "2016-06-08T20:00:00+0000",
					"volume" : "1615712",
					"year_high" : "810.350000",
					"year_low" : "539.210000"
				}
			}
		}