// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Viatris Monthly Financial Report"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"label": __("Invoice Date"),
			"fieldtype": "Date",
			"default": dateutil.month_start(),
			"reqd": 1
		},
	]
};
