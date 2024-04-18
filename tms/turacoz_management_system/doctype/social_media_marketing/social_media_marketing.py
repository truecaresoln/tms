# Copyright (c) 2023, RSA and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class SocialMediaMarketing(Document):
	
	def validate(self):
		self.send_notification_alert()
	
	def send_notification_alert(self):
		send_notification = self.send_notification
		
		if self.linkedin_link:
			linkedin_post = self.linkedin_link
			fn_linked_in = "<li><b>Linkedin Link: </b><a href='"+linkedin_post+"'>"+linkedin_post+"</a></li>"
		else:
			fn_linked_in = ''
		
		if self.facebook_link:
			facebook_post = self.facebook_link
			fn_facebook = "<li><b>Facebook Link: </b><a href='"+facebook_post+"'>"+facebook_post+"</a></li>"
		else:
			fn_facebook = ""
			 
		if self.twitter_link:
			twitter_post = self.twitter_link
			fn_twitter = "<li><b>Twitter Link: </b><a href='"+twitter_post+"'>"+twitter_post+"</a></li>"
		else:
			fn_twitter = ""
			 
		if self.instagram_link:
			instagram_post = self.instagram_link
			fn_instagram = "<li><b>Instagram Link: </b><a href='"+instagram_post+"'>"+instagram_post+"</a></li>"
		else:
			fn_instagram = ""
			
		if self.resource_link:
			resource_post = self.resource_link
			fn_resource = "<li><b>Resource Link: </b><a href= '"+resource_post+"'>"+resourse_post+"</a></li>"
		else:
			fn_resource = ""
			
		paragrap = "<p>We've just shared an important update on our company's LinkedIn page, and we kindly request your participation. Your simple click on the post to like and share can go a long way in spreading the word and amplifying our message. Let's show our collective strength and support by joining forces to uplift our company's online presence. </p>"	
		
		if send_notification == 1:
			data_employee_emailIds = self.get_employee_list()
	#		data_employee_emailIds = [data_employee_emailIds]
   # data_employee_emailIds = ['atul.teotia@turacoz.com','abhishek.bana@turacoz.com','himanshu.rajput@turacoz.com','sanjana.chaleria@turacoz.com','harsh.yadav@turacoz.com','kartik.kashyap@turacoz.com']
			messages = "<p><b>Dear Turon,</b></p><p>Calling You! We need your support to make our social media post shine!</p>"+paragrap+"<p><b> Links for social Media Post:</b></p>"+fn_linked_in+""+fn_facebook+""+fn_instagram+""+fn_twitter+""+fn_resource+"<p><b>Thanks & Best Regards,</b></p>"
			subject_fn = "New Post!"
			frappe.sendmail(recipients=data_employee_emailIds,
						subject=(subject_fn),
						message = messages,
						)
			
	def get_employee_list(self):
		data = frappe.db.sql("""Select GROUP_CONCAT(user_id) as email_ids from `tabEmployee` where status='Active';""", as_dict = True)
		emailIds = data[0]['email_ids']
		
		return emailIds
		