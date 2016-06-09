from django.contrib import admin
from .models import Story, Tag, User, Favourite


class FavouriteInline(admin.StackedInline):
    model = Favourite
    extra = 3

class UserAdmin(admin.ModelAdmin):
    fields = ['id', 'name']
    inlines = [FavouriteInline]

admin.site.register(Story)
admin.site.register(Tag)
admin.site.register(User, UserAdmin)
