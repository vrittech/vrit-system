# signals.py

from django.db.models.signals import post_save,post_delete
from django.dispatch import receiver
from .models import CaseStudy,CaseStudyCategory

@receiver(post_save, sender=CaseStudy)
def set_position_same_as_id(sender, instance, created, **kwargs):
    if created and instance.position != instance.id:
        instance.position = instance.id
        instance.save()
        
@receiver(post_delete, sender=CaseStudyCategory)
def remove_deleted_category_from_case_studies(sender, instance, **kwargs):
    # Get all case studies that contain the deleted category
    case_studies_with_category = CaseStudy.objects.filter(category=instance)
    for case_study in case_studies_with_category:
        # Remove the deleted category from each case study's categories
        case_study.category.remove(instance)

