from django.db import models

class Features(models.Model):
    title = models.CharField(max_length = 250)

# Create your models here.
class Plan(models.Model):
    title = models.CharField(max_length = 250)
    pricing = models.PositiveIntegerField()
    duration = models.PositiveIntegerField() #in month
    description = models.TextField()
    features = models.ManyToManyField(Features,through='PlanHaveFeatures', related_name='plans') #many to many relationship with Features model

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PlanHaveFeatures(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    feature = models.ForeignKey(Features, on_delete=models.CASCADE)
    status = models.BooleanField(default = True)