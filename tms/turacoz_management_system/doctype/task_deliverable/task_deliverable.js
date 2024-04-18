// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Task Deliverable', {
	// refresh: function(frm) {

	// }

	"activity_type": function(frm) {
		var ab = frm.doc.activity_type;
		cur_frm.set_query("deliverable", function() {
			return {
				"filters": {
			    	"activity_type": ("=", ab)
			   }
			};
		});
	},
});
