// Copyright (c) 2021, RSA and contributors
// For license information, please see license.txt

frappe.ui.form.on('Training Data', {
	 onload: function(frm) {
			var customer = frm.doc.customer;
			
			// filter on project
			cur_frm.set_query("project", function() {
				return {
					"filters": {
				    	"project_current_status": ("=", "Ongoing")
				   }
				};
			});
			
			if(frm.is_new()){
			var current = new Date();
			var year = current.getFullYear();
			var month = current.toLocaleString('default', { month: 'long' }).substr(0,3);
			//alert(month);
			frm.set_value("year_of_batch",year);
			frm.set_value("batch",month);
			}
			
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
	 
	"country":function(frm)
	{
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
	
	"course_fees":function(frm)
	{
		var courseFees = frm.doc.course_fees;
		var discount = frm.doc.discount;

		if(discount)
		{
			var ttlFees = courseFees - discount;
			frm.set_value("total_fees",ttlFees);
			frm.set_value("net_total",ttlFees);
			frm.set_value("grand_total",ttlFees);
			//frm.set_value("pending_fees",ttlFees);
		}
		else
		{
			var discount = 0;
			var ttlFees = courseFees - discount;
			frm.set_value("total_fees",ttlFees);
			frm.set_value("net_total",ttlFees);
			frm.set_value("grand_total",ttlFees);
			//frm.set_value("pending_fees",ttlFees);
		}
	},

	"discount":function(frm)
	{
		var courseFees = frm.doc.course_fees;
		var discount = frm.doc.discount;
		
		if(courseFees)
		{
			var ttlFees = courseFees - discount;
			frm.set_value("total_fees",ttlFees);
			frm.set_value("net_total",ttlFees);
			frm.set_value("grand_total",ttlFees);
			//frm.set_value("pending_fees",ttlFees);
		}
		else
		{
			frm.set_value("total_fees",0.00);
			frm.set_value("net_total",0.00);
			frm.set_value("grand_total",0.00);
			//frm.set_value("pending_fees",0.00);
		}
	},

	"payment_mode":function(frm)
	{
		var paymentMode = frm.doc.payment_mode;
		if(paymentMode == 'EMI')
		{
			frm.set_df_property("emi_detail", "reqd", 1);
		}
		else
		{
			frm.set_df_property("emi_detail", "reqd", 0);
		}
	}
});
