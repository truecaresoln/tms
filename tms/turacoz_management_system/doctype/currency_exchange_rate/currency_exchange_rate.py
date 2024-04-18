# Copyright (c) 2022, RSA and contributors
# For license information, please see license.txt

import frappe
from collections import Counter
from datetime import datetime
import datetime
from forex_python.converter import CurrencyRates
import math
from dateutil.relativedelta import relativedelta
from frappe.model.document import Document
import requests
import json

class CurrencyExchangeRate(Document):
	
	pass

@frappe.whitelist()
def currency_exchange_rate():
	to_currency = "INR"
	modified = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
	
	data = frappe.db.sql("""Select name,currency from `tabCurrency Exchange Rate`""", as_dict=True);
	for rec in data:
		from_currency = rec.currency
		if from_currency:
			url = 'https://v6.exchangerate-api.com/v6/40ddc488166a3cf314212937/pair/'+from_currency+'/INR'

			# Making our request
			response = requests.get(url)
			data = response.json()
				
				# Your JSON object
			currenyrate = round(data['conversion_rate'],2)
   # c = CurrencyRates()
   # currenyrate = c.get_rate(from_currency, to_currency)
   # print('Currency is : '+from_currency+' Currency Rate is : '+str(currenyrate)+'/n')
   # currenyrate = round(currenyrate, 2)
			data1 = frappe.db.sql("""UPDATE `tabCurrency Exchange Rate` set rate_in_inr='{0}',modified='{2}' where name='{1}'""".format(currenyrate,rec.name,modified))
