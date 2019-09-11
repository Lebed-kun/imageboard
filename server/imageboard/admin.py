from django.contrib import admin

from . import models
# Register your models here.

@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbr', 'bump_limit', 'author')

@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_post', 'board', 'posts_count')

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'contact', 'options', 'thread', 'message')