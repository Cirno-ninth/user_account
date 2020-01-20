from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.User)
admin.site.register(models.UserInfo)
admin.site.register(models.UserTags)
admin.site.register(models.Fans)
admin.site.register(models.ConfirmString)