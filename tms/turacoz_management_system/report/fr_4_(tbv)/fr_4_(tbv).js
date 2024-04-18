// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["FR-4 (TBV)"] = {
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
