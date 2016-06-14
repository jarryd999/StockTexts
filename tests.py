import unittest
from app import app

class TestStockTexts(unittest.TestCase):

	def test_single_company_no_detail(self):
		self.test_app = app.test_client()
		response = self.test_app.post('/', data={'From': '9149076903', 'Body':'GOOGL'})
		self.assertEquals(response.status, "200 OK")


	def test_multi_company_no_detail(self):
		self.test_app = app.test_client()
		response = self.test_app.post('/', data={'From': '9149076903', 'Body':'GOOGL,fb,amzn'})
		self.assertEquals(response.status, "200 OK")

	def test_single_company_detail(self):
		self.test_app = app.test_client()
		response = self.test_app.post('/', data={'From': '9149076903', 'Body':'BRK.A, detail'})
		self.assertEquals(response.status, "200 OK")

	def test_multi_company_detail(self):
		self.test_app = app.test_client()
		response = self.test_app.post('/', data={'From': '9149076903', 'Body':'GOOGL,detail,fb,amzn'})
		self.assertEquals(response.status, "200 OK")

		# test_resource ={
		# 	"resource" : { 
		# 		"classname" : "Quote",
		# 		"fields" : { 
		# 			"change" : "11.839966",
		# 			"chg_percent" : "1.619495",
		# 			"day_high" : "743.809998",
		# 			"day_low" : "735.765015",
		# 			"issuer_name" : "Alphabet Inc.",
		# 			"issuer_name_lang" : "Alphabet Inc.",
		# 			"name" : "Alphabet Inc.",
		# 			"price" : "742.929993",
		# 			"symbol" : "GOOGL",
		# 			"ts" : "1465416000",
		# 			"type" : "equity",
		# 			"utctime" : "2016-06-08T20:00:00+0000",
		# 			"volume" : "1615712",
		# 			"year_high" : "810.350000",
		# 			"year_low" : "539.210000"
		# 		}
		# 	}
		# }