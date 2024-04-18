// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Viatris PM Evaluations"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": dateutil.month_start(),
			"reqd": 0
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": dateutil.month_end(),
			"reqd": 0
		},
		{
			"fieldname": "project_category",
			"label": __("Project Category"),
			"fieldtype": "Link",
			"options": "Project Category",
			"reqd": 0
		},
		{
			"fieldname": "viatris_project_country",
			"label": __("Country"),
			"fieldtype": "Link",
			"options": "Viatris Project Country",
			"reqd": 0
		},
		{
			"fieldname": "region",
			"label": __("Region"),
			"fieldtype": "Link",
			"options": "Viatris Team",
			"reqd": 0
		},
		{
			"fieldname": "therapeutic_area",
			"label": __("Therapeutic Area"),
			"fieldtype": "Link",
			"options": "Therapeutic Area",
			"reqd": 0
		},
	]
};
