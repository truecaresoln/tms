// Copyright (c) 2024, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Combined ToDo Report"] = {
	"filters": [
		{
			"fieldname": "department",
			"label": __("Department"),
			"fieldtype": "Link",
			"options": "Department",
			"reqd": 0
		},
		{
			"fieldname": "allocate_to",
			"label": __("Employee"),
			"fieldtype": "Link",
			"options": "User",
			"reqd": 0
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ['Open','Overdue'],
			"reqd": 0
		},
	]
};
