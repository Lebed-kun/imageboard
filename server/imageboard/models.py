from django.db import models
from django.core.validators import FileExtensionValidator

import os

# Only technical admins can change data of these models

pass

# Public models

class Board(models.Model):
    name = models.CharField(max_length=100, unique=True)
    abbr = models.CharField(max_length=10, unique=True, validators=[])
    description = models.TextField(validators=[])
    bump_limit = models.IntegerField(default=500)
    spam_words = models.CharField(validators=[])
    picture = models.ImageField(upload_to="board_avas/")
    # author
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.abbr + ' : ' + self.name

class Thread(models.Model):
    sticked = models.BooleanField(default=False)
    got_bump_limit = models.BooleanField(default=False)
    read_only = models.BooleanField(default=False)
    first_post = models.OneToOneField('Post', on_delete=models.CASCADE, related_name='first_post', null=True, blank=True)
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name='boards')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return ''

class Post(models.Model):
    title = models.CharField(max_length=200, blank=True)
    author = models.CharField(max_length=100, blank=True)
    contact = models.CharField(max_length=100, blank=True, validators=[])
    options = models.ManyToManyField('PostOption', blank=True, related_name='options')
    message = models.TextField(max_length=15000)
    poster_ip = models.GenericIPAddressField()
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.poster_ip + ' : ' + self.message[:20]

    def save(self, *args, **kwargs):
        if self.thread.first_post is None:
            self.thread.first_post = self
        super().save(*args, **kwargs)

class PostOption(models.Model):
    option = models.CharField(unique=True)

    def __str__(self):
        return self.option    

class PostFile(models.Model):
    ALLOWED_EXTENSIONS = [
        'jpg', 'jpeg', 'png', 'gif', 'mp4', 'webm', 'pdf', 'djvu', 'mp3', 'ogg'
    ]
    
    post_file = models.FileField(upload_to="post_files/", validators=[FileExtensionValidator(allowed_extensions=ALLOWED_EXTENSIONS)])
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return os.path.basename(self.post_file.name) + ' : (' + str(self.post) + ')'

class Report(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name="posts")
    reason = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '(' + str(self.post) + ') : ' + self.reason[:20] 

class Ban(models.Model):
    poster_ip = models.GenericIPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expired_at = models.DateTimeField()
    reason = models.TextField(max_length=200)
    board = models.ForeignKey('Board', on_delete=models.CASCADE, related_name="boards", null=True, blank=True)

    def __str__(self):
        board = ''
        if self.board is not None:
            board = '(' + str(self.board) + ')'
        return board + ' : ' self.poster_ip + ' : ' + self.reason[:20]


