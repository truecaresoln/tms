// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Company PoC', {
	// refresh: function(frm) {

	// }
	onload: function(frm) {
			var country = frm.doc.country;
			//State Filter
			cur_frm.set_query("state", function() {
			return {
				"filters": {
			    	"country_name": ("=", country)
			    }
			};
			});

	 },
	 
	 "country": function(frm) {
			var country = frm.doc.country;
			//State Filter
			cur_frm.set_query("state", function() {
			return {
				"filters": {
			    	"country_name": ("=", country)
			    }
			};
			});

	 },
});
