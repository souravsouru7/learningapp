from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True,null=True)

    def __str__(self):
        return self.user.username


class PurchasedProduct(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    payment_status = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user_profile', 'product')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    images = models.ImageField(upload_to='product_images/')
    video_file = models.FileField(upload_to='video_files/', validators=[FileExtensionValidator(['mp4', 'mov'])], blank=True)
    # Remove payment_status from here
    order_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name
