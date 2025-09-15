from django.db import models

class PrivacyPolicy(models.Model):
    description = models.TextField()

    def __str__(self):
        return f"Privacy Policy ({self.id})"
    


class TermsConditions(models.Model):
    description = models.TextField()

    def __str__(self):
        return f"Terms and Conditions ({self.id})"