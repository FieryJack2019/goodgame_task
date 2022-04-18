from django.contrib import admin
from .models import UserProfile, Game, Category


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)


class GameAdmin(admin.ModelAdmin):
    pass

admin.site.register(Game, GameAdmin)


class UserProfileAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserProfile, UserProfileAdmin)