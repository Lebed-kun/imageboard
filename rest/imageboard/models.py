from django.db import models
from django.core.validators import FileExtensionValidator, EmailValidator, URLValidator
from django.db.models.signals import pre_delete, post_delete, pre_save
from django.dispatch import receiver
from datetime import datetime, timezone

import os

from . import validators

class SiteInfo(models.Model):
    info = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.info[:20]

# User models

class Privelege(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

class UserGroup(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    priveleges = models.ManyToManyField('Privelege', related_name='priveleges', blank=True)
    board = models.ForeignKey('Board', related_name='group_boards', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name + ' : ' + self.get_board()

    def get_board(self):
        return self.board

class UserToken(models.Model):
    value = models.CharField(max_length=250)
    expired_at = models.DateTimeField()
    ip = models.GenericIPAddressField(default='0.0.0.0', unique=True)

    def __str__(self):
        return self.value

class User(models.Model):
    name = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    pass_hash = models.CharField(max_length=256)
    pass_salt = models.CharField(max_length=100)
    pass_algo = models.CharField(max_length=100)
    groups = models.ManyToManyField('UserGroup', related_name='user_groups', blank=True)
    token = models.OneToOneField('UserToken', on_delete=models.SET_NULL, related_name='user_tokens', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_priveleges(self, name):
        result = []
        
        groups = self.groups.all()
        for group in groups:
            priveleges = group.priveleges.filter(name=name)
            if len(priveleges) != 0:
                data = {
                    'board' : group.get_board(),
                    'privelege' : priveleges[0].name
                }

                if data['board'] is None:
                    return [data] 

                result.append(data)
        
        return result

# Post models

class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbr = models.CharField(max_length=10, unique=True, validators=[validators.abbr_validator])
    description = models.TextField(blank=True)
    bump_limit = models.IntegerField(default=500)
    spam_words = models.TextField(blank=True, validators=[validators.csv_validator])
    picture = models.ImageField(upload_to="board_avas/", null=True, blank=True, validators=[validators.ava_validator])
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.abbr + ' : ' + self.name

@receiver(post_delete, sender=Board, dispatch_uid='board_picture_delete')
def board_picture_delete(sender, instance, using, **kwargs):
    if instance.picture and os.path.isfile(instance.picture.path):
        os.remove(instance.picture.path)

@receiver(pre_save, sender=Board, dispatch_uid='board_picture_edit')
def board_picture_edit(sender, instance, **kwargs):
    if not instance.id:
        return False

    try:
        old_file = sender.objects.get(id=instance.id).file
    except sender.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class Thread(models.Model):
    sticked = models.BooleanField(default=False)
    read_only = models.BooleanField(default=False)
    first_post = models.OneToOneField('Post', on_delete=models.CASCADE, related_name='first_post', null=True, blank=True)
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bumped_at = models.DateTimeField(auto_now_add=True)
    posts_count = models.IntegerField(default=0)

    def __str__(self):
        if self.first_post is not None:
            return str(self.first_post)
        else:
            return str(self.id)

    def has_bump_limit(self):
        return self.posts_count >= self.board.bump_limit

class Post(models.Model):
    title = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=50, blank=True)
    contact = models.CharField(max_length=100, blank=True, validators=[EmailValidator, URLValidator])
    options = models.CharField(max_length=200, blank=True, validators=[validators.csv_validator])
    message = models.TextField(max_length=15000)
    poster_ip = models.GenericIPAddressField()
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.poster_ip + ' : ' + self.title

    def save(self, *args, **kwargs):
        if not self.thread.first_post and len(self.title) == 0:
            self.title = self.message[:20]
        
        super().save(*args, **kwargs)
        
        if not self.thread.first_post:
            self.thread.first_post = self
        self.thread.posts_count += 1
        
        options = self.options.split(',')
        if not self.thread.has_bump_limit() and not 'sage' in options:
            self.thread.bumped_at = datetime.now()

        self.thread.save()

@receiver(pre_delete, sender=Post, dispatch_uid='posts_count_decrease')
def posts_count_decrease(sender, instance, using, **kwargs):
    thread = instance.thread
    thread.posts_count -=1
    thread.save()

class PostFile(models.Model):
    ALLOWED_EXTENSIONS = [
        'jpg', 'jpeg', 'png', 'gif', 'mp4', 'webm', 'pdf', 'djvu', 'mp3', 'ogg'
    ]
    
    post_file = models.FileField(upload_to="post_files/", validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)])
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return os.path.basename(self.post_file.name) + ' : (' + str(self.post) + ')'

    def get_file_name(self):
        return os.path.basename(self.post_file.name)

@receiver(post_delete, sender=PostFile, dispatch_uid='post_file_delete')
def post_file_delete(sender, instance, using, **kwargs):
    if instance.post_file and os.path.isfile(instance.post_file.path):
        os.remove(instance.post_file.path)

# Moder models

class Report(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="report_posts")
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='report_boards', null=True, blank=True)
    reason = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '(' + str(self.post) + ') : ' + self.reason[:20] 

class Ban(models.Model):
    poster_ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField(validators=[validators.exp_date_validator])
    reason = models.TextField(max_length=200)
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name="ban_boards", null=True, blank=True)

    def __str__(self):
        board = ''
        if self.board is not None:
            board = '(' + str(self.board) + ')'
        return board + ' : ' + self.poster_ip + ' : ' + self.reason[:20]

# Requests

class Requests(models.Model):
    subject = models.CharField(max_length=200)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject[:20] + ' : ' + self.text[:20]
