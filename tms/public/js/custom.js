// Copyright (c) 2020, solufy and contributors
// For license information, please see license.txt

frappe.ui.form.on('Service Types',{
	//"service": function(frm) {
	//console.log("Welcome frm::::::::",frm.doc);
		//cur_frm.set_query("service", function() {
		//alert('welcome');
	        //return {
	           // "filters": {
	            //	"status": ("=", "Active")
	            //}
	        //};
	    //});
	//}

	onload: function (frm) {		
		var so = frappe.meta.get_docfield("Service Types", "service");
		cur_frm.set_query("service", function() {
			return {
				"filters": {
			    	"status": ("=", "Active")
			    }
			};
		});
	}
});


	
