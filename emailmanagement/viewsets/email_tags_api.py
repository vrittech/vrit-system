#api for email tags
## types of porpose
# ('blog','Blog'),('contact_us','Contact Us'),('newsletter_subscription','News Letter Subscription')
"""
```
1. blog
2. contact_us
3. newsletter_subscription
```
"""

blog_tags = ['blog_user','blog_title','blog_description','blog_receiver_full_name']
contact_us_tags = ['contact_first_name','contact_last_name','contact_email_address','contact_phone_number','contact_company_name','contact_project_service','contact_project_plan']
newsletter_subscription_tags = ['news_letter_subscription_full_name','news_letter_subscription_email','news_letter_subscrirption_category']

from rest_framework.views import APIView
from rest_framework.response import Response

class EmailTags(APIView):
    def get(self, request, tag_type, *args, **kwargs):
        if tag_type == "blog_tags":
            return Response(blog_tags)
        
        elif tag_type == "contact_us_tags":
            return Response("contact_us_tags")
        
        elif tag_type == "newsletter_subscription_tags":
            return Response("newsletter_subscription_tags")
        
        else:
            return Response("tags type doesnot match")