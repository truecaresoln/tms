// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Account Manager Dashboard"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 0
		},
		{
			"fieldname":"type",
			"label": __("Type"),
			"fieldtype": "Select",
			"options": ['','Ongoing Projects','Finance','Contacts','Agreements','Marketing Data'],
			"reqd": 0
		},
		{
			"fieldname":"account",
			"label": __("Account Managers"),
			"fieldtype": "Select",
			"options": ['Harshita Gupta','M Sunil  Kumar'],
			"default": 'Harshita Gupta',
			"reqd": 0
		},

	]
};
