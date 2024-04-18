// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PM Evaluations"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dateutil.month_start(),
			"reqd": 0
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dateutil.month_end(),
			"reqd": 0
		}
	]
};
