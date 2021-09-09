from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

# class Services(models.Model):
#     name = models.CharField(max_length=122)
#     email = models.CharField(max_length=122)
#     phone = models.CharField(max_length=12)
#     desc = models.TextField()
#     date = models.DateField()
#
#     def __str__(self):
#         return self.name

class group_info_table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=122)
    amount = models.CharField(max_length=6)
    duration = models.CharField(max_length=6, default='1m')
    created_at=models.IntegerField(default=0)
    updated_at=models.IntegerField(default=0)
    start_date=models.IntegerField(default=0)
    end_date=models.IntegerField(default=0)
    status = models.CharField(max_length=12, default='inactive')
    bid_date=models.IntegerField(default=0)
    created_by_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
     )
    def __str__(self):
        return str(self.id)


class UserInfo(models.Model):
    u_id =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        related_name='user_info'
     )
    account_number = models.CharField(max_length=20)
    ifsc = models.CharField(max_length=20)
    branch_address = models.CharField(max_length=130, default = '')
    superuser = models.BooleanField(default=False)
    superuser_start_date = models.IntegerField(default=0)
    superuser_end_date = models.IntegerField(default=0)
    paytm_qr_code = models.ImageField(blank=True, upload_to='static/img/', default='')
    phonepe_qr_code = models.ImageField(blank=True, upload_to='static/img/', default='')
    gpay_qr_code = models.FileField(blank=True, upload_to='static/img/', default='')
    mobile = models.IntegerField(max_length=20, blank=False, default=0)
    address_line_1 = models.CharField(max_length=100, blank=True, default='')
    address_line_2 = models.CharField(max_length=100, blank=True, default='')
    order_id = models.CharField(max_length=50, blank=True, default='')
    razorpay_payment_id = models.CharField(max_length=50, blank=True, default='')
    razorpay_order_id = models.CharField(max_length=50, blank=True, default='')
    razorpay_signature = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return self.u_id.username
    

class group_table(models.Model):
    g_id = models.ForeignKey(
        group_info_table,
        on_delete=models.CASCADE,
        default=0
     )
    u_id =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=9
     )
    start_comity = models.BooleanField(default=False)
    winner = models.BooleanField(default=False)
    round = models.IntegerField(default=0)
    bidAmount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.u_id.username)

class bid(models.Model):
    g_id = models.ForeignKey(
        group_info_table,
        on_delete=models.CASCADE,
        null=True,
     )
    u_id =  models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
     )
    bidAmount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.u_id.username)


# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     mobile = models.IntegerField(max_length=20, blank=False, default=0)
#     address_line_1 = models.CharField(max_length=100, blank=True, default='')
#     address_line_2 = models.CharField(max_length=100, blank=True, default='')
#
#     def __str__(self):
#         return str(self.user.username)

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


# class UserInfo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     # bio = models.TextField(max_length=500, blank=True)
#     # location = models.CharField(max_length=30, blank=True)
#     # birth_date = models.DateField(null=True, blank=True)
#     accountNumber = models.CharField(max_length=30, required=False, help_text='Optional.')
#     ifsc = models.CharField(max_length=30, required=False, help_text='Optional.')
#     branchName = models.CharField(max_length=30, required=False, help_text='Optional.')

#     def __str__(self):
#         return self.user.username
    
