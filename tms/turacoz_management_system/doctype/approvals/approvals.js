// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Approvals', {
	// refresh: function(frm) {

	// }

});
//dynamic buttons
frappe.ui.form.on("Approvals", "refresh", function(frm) 
{
	if(frm.doc.status=='Draft'){
		frm.add_custom_button(__('Approve'), function(){ 
			setApproved();
		});
		frm.add_custom_button(__('Reject'), function(){ 
			setRejected();
		});
	}
	else if(frm.doc.status=='Rejected'){
		frm.add_custom_button(__('Approve'), function(){ 
			setApproved();
		});
	}		
});

function setApproved(){

	frappe.confirm(
	    'Are you sure, you want to approve it?',
	    function(){
		var document_name = cur_frm.doc.document_name;
		var document = cur_frm.doc.document;
		frappe.call({
        		method: "tms.turacoz_management_system.doctype.approvals.approvals.approve_record",
			args:{ "document":document,"document_name":document_name
		},
		callback:function(res){
			let a = res.message;
			if (a==0){
				show_alert("Approved");
				window.location.reload();
			}
		}
        })
	    },
	    function(){
		window.close();	
	    }
	)

}

function setRejected(){
	frappe.confirm(
	    'Are you sure, you want to reject it?',
	    function(){
		var document_name = cur_frm.doc.document_name;
		var document = cur_frm.doc.document;
		frappe.call({
        		method: "tms.turacoz_management_system.doctype.approvals.approvals.reject_record",
			args:{ "document":document,"document_name":document_name
		},
		callback:function(res){
			let a = res.message;
			if (a==0){
				show_alert("Rejected");
				window.location.reload();
			}
		}
        })
	    },
	    function(){
		window.close();	
	    }
	)
}
