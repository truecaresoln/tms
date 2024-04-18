// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["FR-6B (TSPL - Business Details)"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("Invoice Start Date"),
			"fieldtype": "Date",
			"default": dateutil.month_start(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("Invoice End Date"),
			"fieldtype": "Date",
			"default": dateutil.month_end(),
			"reqd": 1
		},	
	]
};
