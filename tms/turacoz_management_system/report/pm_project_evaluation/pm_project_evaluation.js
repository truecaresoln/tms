// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["PM Project Evaluation"] = {
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
	],
	
	"formatter":function (value, row, column, data, default_formatter) {
		value = default_formatter(value,row,column,data);
		let today = new Date().toISOString().slice(0, 10)
	
		if ( data.days>365) {
			value = "<b style='color:red;'>" + value + "</b>";
	   	}
	   	
	   	return value;
	   }
};
