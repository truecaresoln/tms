# -*- coding: utf-8 -*-
# Copyright (c) 2021, RSA and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
import frappe
from frappe import _

from frappe.model.document import Document

class OverlapError(frappe.ValidationError): pass
class OverWorkLoggedError(frappe.ValidationError): pass

class FeesReceived(Document):
	def validate(self):
		doc = frappe.get_doc("Training Data", self.training_data)
		doc.pending_fees = self.outstanding_amount	
		doc.save()	
	