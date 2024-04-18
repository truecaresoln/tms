// Copyright (c) 2022, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('DMS ALERT SYSTEM', {
	"department": function(frm) {
		var ab = frm.doc.department;
		cur_frm.set_query("category", function() {
			return {
				"filters": {
			    	"department": ("=", ab)
			   }
			};
		});
		frm.set_value('sub_category','');
	},
	"category": function(frm) {
		var ab = frm.doc.category;
		cur_frm.set_query("sub_category", function() {
			return {
				"filters": {
			    	"category": ("=", ab)
			   }
			};
		});
		if(ab && frm.doc.sub_category==''){
			frm.set_value('heading',ab);
		}
	},
	"sub_category": function(frm) {
		var ab = frm.doc.sub_category;
		if(ab){
			frm.set_value('heading',ab);
		}
	},
});
