from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    day_of_membership = models.IntegerField()
    stripe_price_id = models.CharField(max_length=220, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    phone_number = models.CharField(max_length= 15, null=True, blank=True)
    company_name = models.CharField(max_length= 200, null=True, blank=True)
    street_name = models.CharField(max_length= 100, null=True, blank=True)
    zip_code = models.CharField(max_length= 20, null=True, blank=True)
    kvk = models.CharField(max_length= 100, null=True, blank=True)
    bank_account_number = models.CharField(max_length= 50, null=True, blank=True)

    verification_code = models.CharField(max_length=10)
    is_email_verified = models.BooleanField(default=False)

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    subscribed_at = models.DateField(blank=True, null=True)

    c = {
        ('Account', 'Account'),
        ('shop', 'shop'),
    }
    login_from = models.CharField(choices=c, max_length=20, default='Account')

    
    def __str__(self):
        return self.user.email


class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shops')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10, default="")
    house_no = models.CharField(max_length=20, default="")
    description = models.TextField()
    tags = TaggableManager()
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    


    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']

    
    @property
    def get_all_shop(self):
        return self.imagegallery_set.filter(owner=self.owner)


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='shop_images/')
    name = models.CharField(max_length=100, null=True, blank=True)
    gallery = models.ManyToManyField("coreapp.ImageGallery", related_name="gallery_image", null=True, blank=True)
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name
    
    

class ImageGallery(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    gallery_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.shop.name}--{self.gallery_name}"
    
    class Meta:
        ordering = ['-id']

    @property
    def get_image(self):
        return self.gallery_image.all()

