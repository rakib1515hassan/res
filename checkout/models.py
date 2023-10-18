from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class StripeCustomer(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)

    def __str__(self):
        return self.user.first_name

class SubscriptionPaid(models.Model):
    user = models.ForeignKey(StripeCustomer, on_delete=models.CASCADE, null=True, default=None, blank=True)
    time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    subscription_status = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.user.user.first_name