// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Project Vs Team Dashbaord"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dateutil.month_start(),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dateutil.month_end(),
			"reqd": 1
		},
		{
			"fieldname":"team",
			"label": __("Team"),
			"fieldtype": "Select",
			"options": ['','UK','France','GKB1','GKB2','EM1','EM2'],
			"reqd": 0
		},
	]
};
