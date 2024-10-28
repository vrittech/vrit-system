from django.db import models
from blog.models import BlogCategory,Blog

class EmailSetup(models.Model):
    smtp_server_address = models.CharField(max_length = 300)  #EMAIL_HOST
    email_address = models.EmailField(max_length = 300)
    password = models.CharField(max_length = 2000) #app password
    port = models.PositiveIntegerField()
    required_authentication = models.BooleanField(default = True)
    security = models.CharField(max_length = 200,choices = (('None','None'),('SSL','SSL'),('TSL','TSL')),default = 'None')
    smtp_username = models.CharField(max_length = 100,null = True,blank = True)
    verify_smtp_certificate = models.BooleanField(default = False)
    
    def __str__(self):
        return self.email_address


# Create your models here.
class EmailManagement(models.Model):
    template_name = models.CharField(max_length = 255)
    from_name = models.CharField(max_length = 155)
    cc = models.CharField(max_length = 5000)
    bcc = models.CharField(max_length = 5000)
    subject = models.CharField(max_length = 300)
    body = models.TextField()
    purpose = models.CharField(max_length = 50,choices = (('blog','Blog'),('contact_us','Contact Us'),('newsletter_subscription','News Letter Subscription')))
    frequency = models.CharField(max_length = 50, choices = (('day','Day'),('week','Week'),('month','Month'),('year','Year')))
    frequency_per = models.IntegerField()
    blog_category = models.ForeignKey(BlogCategory,on_delete = models.CASCADE)
    number_of_blog_based_on_user = models.IntegerField(default=1)
    number_of_blog = models.IntegerField(default=1)
    additional_blog = models.ManyToManyField(Blog)
    excerpt = models.CharField(max_length = 2000)
    featured_image = models.ImageField(upload_to='emailtemplate')
    
    def __str__(self):
        return self.template_name