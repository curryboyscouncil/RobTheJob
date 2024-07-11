from django.contrib import admin

from .models import Resume

# admin stuff
name = "RobTheJob"
admin.site.site_header = f"{name} Admin"
admin.site.site_title = f"{name} Admin Portal"
admin.site.index_title = f"Welcome to {name} Portal"

# Register your models here.

admin.site.register(Resume)