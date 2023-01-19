from django.contrib import admin
from .models import Category, Bulletin, Response


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Bulletin)
class BulletinModelAdmin(admin.ModelAdmin):
    pass
    # prepopulated_fields = {'slug': ('title',)}


@admin.register(Response)
class ResponseModelAdmin(admin.ModelAdmin):
    pass
