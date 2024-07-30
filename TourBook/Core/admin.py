from django.contrib import admin
from django.contrib.auth import get_user_model
from .models.notification import Notification
from .models.report import Report

User = get_user_model()
# Register your models here.


admin.site.register(User)
admin.site.register(Report)
admin.site.register(Notification)
