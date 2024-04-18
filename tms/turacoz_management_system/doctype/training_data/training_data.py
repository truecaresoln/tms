# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from forex_python.converter import CurrencyRates
import math

class TrainingData(Document):
	def validate(self):
		self.validate_currency()
	
	def validate_currency(self):
		currency = self.currency
		grand_total = self.grand_total
		
		to_currency = "INR"
		final_total_amount_inr = float()
		
		if grand_total:
			from_currency = currency
			c = CurrencyRates()
			currenyrate = c.get_rate(from_currency, to_currency)
			currenyrate = round(currenyrate, 2)
			final_total_amount_inr = float(grand_total) * currenyrate
			final_total_amount_inr = round(final_total_amount_inr, 2)
			
			self.total_fees_inr = final_total_amount_inr
			self.pending_fees = final_total_amount_inr
			
@frappe.whitelist(allow_guest=True)				
def update_amount_inr(self,method=None):
	currency = self.currency
	grand_total = self.grand_total

	to_currency = "INR"
	final_total_amount_inr = float()
	 
	if grand_total:
		from_currency = currency
		c = CurrencyRates()
		currenyrate = c.get_rate(from_currency, to_currency)
		currenyrate = round(currenyrate, 2)
		final_total_amount_inr = float(grand_total) * currenyrate
		final_total_amount_inr = round(final_total_amount_inr, 2)
	 
		self.total_fees_inr = final_total_amount_inr
		self.pending_fees = final_total_amount_inr
		
					
