// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Statement of Work', {
	 onload: function(frm) {
		
		//SOW filter
		cur_frm.set_query("sow_change_order", function() {
			return {
				"filters": {
			    	"type": ("=", "SOW")
			    }
			};
		});
	 },
});
