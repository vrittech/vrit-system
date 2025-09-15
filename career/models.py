from django.db import models
from django.utils import timezone
from django.utils.text import slugify
import uuid
from ordered_model.models import OrderedModel

class CareerCategory(OrderedModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class ExperienceLevel(OrderedModel):
    level_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.level_name


class Career(OrderedModel):
    title = models.CharField(max_length=400)
    experience_level = models.ForeignKey(
        ExperienceLevel,
        on_delete=models.SET_NULL,
        related_name='careers',
        null=True
    )
    career_category= models.ManyToManyField(CareerCategory,blank=True)
    description = models.TextField()
    num_of_vacancy = models.PositiveIntegerField(default=0)
    apply_link = models.URLField(max_length=500)
    media = models.ImageField(upload_to='career',blank=True,null=True)
    is_show = models.BooleanField(default=True)
    enable_auto_expiration = models.BooleanField(default=False)
    expiration_date = models.DateTimeField(blank=True, null=True)
    is_expired = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f'{slugify(self.title)}-{str(self.public_id)[1:5]}{str(self.public_id)[-1:-5]}'

        if not self.enable_auto_expiration:
            self.expiration_date = None   # clear expiration date
            self.is_expired = False       # reset expired flag
            self.is_show = True  
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def has_expired(self):
        """
        Check if the career has expired based on the expiration date.
        """
        if self.enable_auto_expiration and self.expiration_date:
            return timezone.now() > self.expiration_date
        return False

    def deactivate_if_expired(self):
        """
        Deactivate the career if it has expired.
        """
        if self.has_expired():
            self.is_expired = True
            self.is_show = False
            self.save()
    
    # class Meta:
    #     permissions = [
    #         ('manage_career', 'Manage Career'),
    #     ]