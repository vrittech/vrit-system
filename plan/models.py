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
        visible_plans_count = Plan.objects.filter(is_show=True).count()

        # Validation: At least 1 plan must be visible
        if not self.is_show and visible_plans_count <= 1:
            raise ValidationError("At least 1 plan must be visible at all times.")

        # Validation: No more than 3 plans can be visible
        if self.is_show and visible_plans_count >= 3 and not self.pk:
            raise ValidationError("No more than 3 plans can be visible at the same time.")

        # Validation: Only a visible plan can be popular
        if self.is_popular and not self.is_show:
            raise ValidationError("Only a visible plan can be marked as popular.")

        # Validation: If there is only one visible plan, it must be marked as popular
        if visible_plans_count == 1 and self.is_show:
            if not self.is_popular:
                raise ValidationError("The only visible plan must be marked as popular.")

    def save(self, *args, **kwargs):
        self.clean()  # Call clean to validate before saving
        super().save(*args, **kwargs)


class PlanHaveFeatures(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    feature = models.ForeignKey(Features, on_delete=models.CASCADE)
    status = models.BooleanField(default = True)
    
    
    def __str__(self):
        return self.status