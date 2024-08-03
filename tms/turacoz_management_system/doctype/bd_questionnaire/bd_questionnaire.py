# Copyright (c) 2024, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc

class BDquestionnaire(Document):
	pass

@frappe.whitelist()
def fetch_questionnaire_template(deliverable):
	items = frappe.get_all('BD questionnaires',
        filters={'parent': deliverable, 'parenttype':'BD questionnaire Template'},
        fields=['questions'])
	return items

# @frappe.whitelist()
# def fetch_questionnaire_template2(source_name, target_doc=None):
# 	target_doc = get_mapped_doc("BD questionnaire Template 2", source_name, {
# 		"BD questionnaire Template 2": {
# 			"doctype": "BD questionnaire",
# 		},
# 		"BD questionnaires": {
# 			"doctype": "BD questionnaires Answers2",
# 		}
# 	}, target_doc)

# 	return target_doc

# @frappe.whitelist()
# def fetch_questionnaire_template3(source_name, target_doc=None):
# 	target_doc = get_mapped_doc("BD questionnaire Template 3", source_name, {
# 		"BD questionnaire Template 3": {
# 			"doctype": "BD questionnaire",
# 		},
# 		"BD questionnaires": {
# 			"doctype": "BD questionnaires Answers3",
# 		}
# 	}, target_doc)

# 	return target_doc

# @frappe.whitelist()
# def fetch_questionnaire_template4(source_name, target_doc=None):
# 	target_doc = get_mapped_doc("BD questionnaire Template 4", source_name, {
# 		"BD questionnaire Template 4": {
# 			"doctype": "BD questionnaire",
# 		},
# 		"BD questionnaires": {
# 			"doctype": "BD questionnaires Answers4",
# 		}
# 	}, target_doc)

# 	return target_doc
