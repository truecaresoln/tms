// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Financial Overview Weekly Report"] = {
	"filters": [

	],
	
	"formatter":function (value, row, column, data, default_formatter) {
		value = default_formatter(value,row,column,data);

		if (column.id == "particular") {
			value = "<span style='color:black;'><b>" + value + "</b></span>";
	 	}
			
	   return value;
	}
};
