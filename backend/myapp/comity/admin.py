from django.contrib import admin
from comity.models import Services
from comity.models import group_info_table
from comity.models import group_table
from comity.models import UserInfo

# Register your models here.
admin.site.register(Services)
admin.site.register(group_info_table)
admin.site.register(group_table)
admin.site.register(UserInfo)



