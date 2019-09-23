from django.contrib import admin

from . import models

# Post models

@admin.register(models.Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'abbr', 'bump_limit', 'author')

@admin.register(models.Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_post', 'board', 'posts_count')

@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'contact', 'options', 'thread', 'message')

@admin.register(models.PostFile)
class PostFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_file')

# Moder models

@admin.register(models.Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'post', 'reason')

@admin.register(models.Ban)
class BanAdmin(admin.ModelAdmin):
    list_display = ('id', 'poster_ip', 'expired_at', 'reason', 'board')

# User models

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')

@admin.register(models.UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(models.Privelege)
class PrivelegeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')