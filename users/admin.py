from django.contrib import admin
from .models import Profile

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('pk','username', 'correo', 'contraseña')

admin.site.register(Profile, ProfileAdmin)    