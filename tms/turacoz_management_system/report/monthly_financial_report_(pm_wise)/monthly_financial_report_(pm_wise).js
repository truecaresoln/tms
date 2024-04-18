// Copyright (c) 2023, RSA and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Financial Report (PM Wise)"] = {
	"filters": [
	],
	
	"formatter":function (value, row, column, data, default_formatter) {
		value = default_formatter(value,row,column,data);

		if (column.id == "months") {
			value = "<span style='color:black;'><b>" + value + "</b></span>";
	 	}
		if (column.id == "currency" && column.value=="Total") {
			value = "<span style='color:black;'><b>" + value + "</b></span>";
	 	}	
	   return value;
	}
};
