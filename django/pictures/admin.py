from django.contrib import admin

from .models import Picture

class PictureAdmin(admin.ModelAdmin):
    list_display = ('title',)

admin.site.register(Picture, PictureAdmin)