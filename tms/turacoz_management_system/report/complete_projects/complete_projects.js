// Copyright (c) 2016, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Complete Projects"] = {
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
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 0
		},
		{
			"fieldname":"viatris",
			"label": __("Viatris"),
			"fieldtype": "Check",
			"default": 0,
			"reqd": 0
		},
	]
};