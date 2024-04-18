// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Publication Submission Log"] = {
	"filters": [
		{
			"fieldname":"status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ['','In Submission','In Acceptance','Published','Rejected'],
			"reqd": 0
		},
	]
};
