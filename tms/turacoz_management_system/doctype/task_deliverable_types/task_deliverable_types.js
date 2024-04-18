// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Task Deliverable Types', {
	// refresh: function(frm) {

	// }

	"task":function(frm){
		var ab = frm.doc.task;
		var ab = ab.split("-").pop();
		//var ab = ab.split('-')[0];
		var ab = ab.replace(/-|[0-9]/g, '');
		
		frm.set_value('task_name',ab);
		//cur_frm.toggle_display("designation", true);
	},
	"deliverable":function(frm){
		var ab = frm.doc.deliverable;

		cur_frm.set_query("task", function() {
			return {
				"filters": {
			    	"deliverable": ("=", ab)
			   }
			};
		});
		
	},
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
