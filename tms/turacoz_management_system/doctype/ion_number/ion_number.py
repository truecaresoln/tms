# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from PIL.GifImagePlugin import getdata

class IONNumber(Document):
	
	def validate(self):
		self.update_sales_payment_request_status()
		self.update_sow_percentage()
		
	
	def update_sales_payment_request_status(self):
		sales_invoice = self.sales_invoice
		payment_request = self.payment_request
		
		if sales_invoice:
			self.sales_invoice_status = "Generated"
		else:
			self.sales_invoice_status = "Not Generated"
			
		if payment_request:
			self.payment_request_status = "Generated"
		else:
			self.payment_request_status = "Not Generated"
			
	def update_sow_percentage(self):
		ion = self.name
		sow = self.statement_of_work
		project_cost = self.project_cost
		
		getData = frappe.db.sql("""select sum(tin.project_cost) as consumed_cost, 
				tin.statement_of_work,sow.amount from `tabION Number` tin 
				left join `tabStatement of Work` sow on tin.statement_of_work = sow.name
				group by tin.statement_of_work;""", as_dict = True)
		if getData:
			for rec in getData:
				consumed_cost = rec.consumed_cost
				statement_of_work = rec.statement_of_work
				sow_amount = rec.amount
				
				if statement_of_work:
					consumed_percentage = consumed_cost / sow_amount*100
					final_consumed_percentage = round(consumed_percentage, 2)
					
					dataSowUpdate = frappe.db.sql("""Update `tabStatement of Work` set sowchange_order_percentage = '{0}' where name = '{1}';""".format(final_consumed_percentage,statement_of_work))
				
				
		
				
	
