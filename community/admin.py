from django.contrib import admin

from .models import Answer, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "is_resolved", "created_at")
    list_filter = ("category", "is_resolved")


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")