from django.contrib import admin
from .models.client_request import ClientRequest
from .models.client import Client
from .models.comments import Comment
# Register your models here.
admin.site.register(Client)
admin.site.register(ClientRequest)
admin.site.register(Comment)
