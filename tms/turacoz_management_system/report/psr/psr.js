// Copyright (c) 2016, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PSR"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dateutil.month_start(),
			"reqd": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dateutil.month_end(),
			"reqd": 1
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"reqd": 0
		},
		{
			"fieldname":"bd_person",
			"label": __("BD Person"),
			"fieldtype": "Link",
			"options": "User",
			"reqd": 0
		},
		{
			"fieldname":"project_manager",
			"label": __("Project Manager"),
			"fieldtype": "Link",
			"options": "User",
			"reqd": 0
		},
		{
			"fieldname":"new_menu",
			"label": __("Menu"),
			"fieldtype": "Select",
			"options": ['All','Yet to Start','Ongoing','Under Client Review','Under Journal Review','Completed Technically','Completed Financially','Completed','Cancelled'],
			"default": "All",
			"reqd": 0
		},

	]
};
