from django.contrib import admin

from .models import Picture, Favorite


class PictureAdmin(admin.ModelAdmin):
    list_display = ("title",)


admin.site.register(Picture, PictureAdmin)
admin.site.register(Favorite)
