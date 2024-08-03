# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date

class Proposals(Document):

	def validate(self):
		self.update_proposal_with_price_date()


	def update_proposal_with_price_date(self):	
		today_date = date.today()
		workflow_state = self.workflow_state
		if workflow_state == 'Send for Approval':
			self.proposal_with_price_date = today_date

	def update_proposal_approved_date(self):	
		today_date = date.today()
		workflow_state = self.workflow_state
		if workflow_state == 'Approved':
			self.proposal_approved_date = today_date		

	
