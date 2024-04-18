// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Fees Received', {
	// refresh: function(frm) {

	// }

	
	"received_fees":function(frm)
	{
		var received_amount = frm.doc.received_fees;
		var pending_fees = frm.doc.pending_fees;
		var outstanding = pending_fees - received_amount;
		frm.set_value('outstanding_amount',outstanding);
	},

	"training_data":function(frm)
	{
		var studentID = frm.doc.training_data;
		cur_frm.set_query("student_invoice", function() {
			return {
				"filters": {
			    	"training_data": ("=", studentID)
			   }
			};
		});
	}
});








