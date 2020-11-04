from django.db import models
import uuid
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Services(models.Model):
    name = models.CharField(max_length=122)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    desc = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name

class group_info_table(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=122)
    amount = models.CharField(max_length=6)
    created_at=models.IntegerField(default=0)
    updated_at=models.IntegerField(default=0)
    # start_date=models.IntegerField(default=0)
    # end_date=models.IntegerField(default=0)
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
     )
    account_number = models.CharField(max_length=122)
    ifsc = models.CharField(max_length=122)
    qr_code = models.ImageField()
    
    def __str__(self):
        return self.u_id.username
    

class group_table(models.Model):
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
    start_comity = models.BooleanField(default=False)
    winner = models.BooleanField(default=False)
    superuser = models.BooleanField(default=False)
    bidAmount = models.IntegerField(default=0)

    def __str__(self):
        return str(self.u_id.username)


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
    
