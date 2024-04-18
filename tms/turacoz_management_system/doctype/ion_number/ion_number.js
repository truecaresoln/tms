// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('ION Number', {
	// refresh: function(frm) {

	// }
	
});

//dynamic buttons
/**frappe.ui.form.on("ION Number", "refresh", function(frm) 
{
	var project = frm.doc.project;
	if(frm.doc.project!=undefined)
	{
		frm.add_custom_button(__('Generate Sale Invoice'), function(){ 
			generate_sales_invoice();
		});
	} 

	if(frm.doc.project!=undefined)
	{
		frappe.call({
			"method": "frappe.client.get",
			 args: {
				doctype: "Challenges and Commitments",
				name: "CHALLENGE-2021-Internal-8524"
			},
			callback: function (data) {
				frm.add_custom_button(__('Generate Payment Request'), function(){ 
					//getUpdate();
				});
			}
		})
	}

});

function generate_sales_invoice()
{
	var project = cur_frm.doc.project;
	alert(project);
	var d = new frappe.ui.Dialog({
	    'fields': [
		{'fieldname': 'items', 'label': 'Items', 'fieldtype': 'Table', 'options': 'Sales Invoice Item'},
		{'fieldname': 'month', 'fieldtype': 'Data', 'label': 'Month', 'placeholder': 'Month','required': '1'},
		{'fieldname': 'year', 'fieldtype': 'Data','label': 'Year', 'placeholder': 'Year'},
		{'fieldname': 'fortype', 'fieldtype': 'Select','label': 'For Type', 'placeholder': 'For Type', 'options':['', 'New Projects This Month','Invoice to be Raised','Expected Payments','Received Payment'], 'required':'1'},
		{'fieldname': 'comment', 'fieldtype': 'Small Text', 'label': 'Comment','placeholder': 'Comment'}
	    ],
	    primary_action: function(frm){
		d.hide();
		//show_alert(d.get_values());
		
	    }
	});
	
	d.show();
}**/

