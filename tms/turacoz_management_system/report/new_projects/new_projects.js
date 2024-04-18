// Copyright (c) 2016, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["New Projects"] = {
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
	/*"formatter": function (value, row, cell, column, data, default_formatter) {
		frappe._default_formatter = ();
    		value = default_formatter(row, cell, value, column, data);
	       if (data.status == "Overdue") {
		    value = "<span style='color:red!important;font-weight:bold'>" + value + "</span>";
	       }
		if (data.status == "Paid") {
		    value = "<span style='color:green!important;font-weight:bold'>" + value + "</span>";
	       }
	       return value;
	}*/
  
};
