from django.db import models
from blog.models import BlogCategory,Blog
from django.core.mail import send_mail
from django.conf import settings
import logging
logger = logging.getLogger(__name__)



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
    class Meta:
        permissions = [
            ('manage_email_setup', 'Manage Email Setup'),
        ]


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
    number_of_blog_attachments_based_on_user = models.IntegerField(default=1)
    number_of_blog = models.IntegerField(default=1)
    additional_blog = models.ManyToManyField(Blog)
    excerpt = models.CharField(max_length = 2000)
    featured_image = models.ImageField(upload_to='emailtemplate')
    
    is_show = models.BooleanField(default = True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.template_name
    class Meta:
        permissions = [
            ('manage_email_management', 'Manage Email Management'),
        ]
    

class EmailLogRecipient(models.Model):
    email = models.EmailField(max_length=230)


class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'sent'),
        ('failed', 'failed'),
        ('scheduled', 'scheduled'),
        ('canceled', 'canceled'),
    ]

    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    purpose = models.CharField(max_length = 50,choices = (('contact_us','Contact Us'),('newsletter_subscription','News Letter Subscription')))
    recipient = models.ManyToManyField(EmailLogRecipient)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    preview = models.TextField(blank=True, null=True)
    scheduled_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.subject} - {self.recipient} - {self.status}'
    class Meta:
        permissions = [
            ('manage_email_log', 'Manage Email Log'),
        ]
    
    

    def send_email(self):
        try:
            send_mail(
                subject=self.subject,
                message=self.preview,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.recipient],
                fail_silently=False,
            )
            self.status = 'sent'
        except Exception as e:
            logger.error(f"Failed to send email to {self.recipient}: {e}")
            self.status = 'failed'
        self.save()