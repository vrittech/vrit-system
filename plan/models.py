from django.db import models
from django.core.exceptions import ValidationError

class Features(models.Model):
    title = models.CharField(max_length = 250)
    is_feature_checked = models.BooleanField(default = True)
    
    
    def __str__(self):
        return self.title
    
    

# Create your models here.
class Plan(models.Model):
    title = models.CharField(max_length = 250)
    pricing = models.PositiveIntegerField()
    duration = models.CharField()
    description = models.TextField()
    features = models.ManyToManyField(Features,through='PlanHaveFeatures', related_name='plans') #many to many relationship with Features model
    is_show = models.BooleanField(default = True)
    is_popular = models.BooleanField(default = True)
    position = models.PositiveIntegerField(default = 9999)
    
   
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    def clean(self):
        # Ensure at least 3 plans remain visible when trying to set `is_show` to False
        if not self.is_show and Plan.objects.filter(is_show=True).count() <= 3:
            raise ValidationError("At least 3 plans must be visible at all times.")

    def save(self, *args, **kwargs):
        self.clean()  # Call the clean method for validation
        super().save(*args, **kwargs)


class PlanHaveFeatures(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    feature = models.ForeignKey(Features, on_delete=models.CASCADE)
    status = models.BooleanField(default = True)
    
    
    def __str__(self):
        return self.status