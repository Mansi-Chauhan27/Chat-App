from django.contrib import admin
from apps.chat.models import Group, Message, UrlToken

# Register your models here.
myModels = [Group, Message, UrlToken]  # iterable list
admin.site.register(myModels)