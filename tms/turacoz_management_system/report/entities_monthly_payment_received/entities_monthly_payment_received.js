// Copyright (c) 2024, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Entities-Monthly Payment Received"] = {
	"filters": [
	
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dateutil.year_start(),
			"reqd": 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dateutil.year_end(),
			"reqd": 0
		},

	]
};
