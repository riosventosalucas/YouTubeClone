# -*- coding: utf-8 -*-

# Python

# Django
from django.db                  import models
from django.contrib.auth.models import User
from django.utils               import timezone

# Project

class Video(models.Model):
    
    title         = models.CharField(max_length=256, null=False)
    views         = models.IntegerField(null=False, default=0)
    author        = models.CharField(max_length=200)
    youtube_id    = models.CharField(max_length=50, null=False)
    thumbnail_url = models.URLField(max_length=200)
    slug          = models.SlugField(max_length=200,unique=True)
    likes         = models.ManyToManyField(User, blank=True)
    created_at    = models.DateTimeField(auto_now_add=True, null=True)
    dislikes      = models.ManyToManyField(User, related_name='dislike_videos', blank=True)
    comments      = models.ManyToManyField(User, through='Comment', related_name='comments_videos')
    active        = models.BooleanField(default=True)

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)

    def calculate_popularity(self):
        value_for_likes    = len(self.likes.all()) * 10
        value_for_comments = len(self.comments.all()) 
        dislikes           = len(self.dislikes.all()) 
        if dislikes > 0:
            value_for_dislikes = dislikes * 5
        else:
            value_for_dislikes = 0

        if self.created_at.date() == timezone.now().date():
            today_bonus = 100
        else:
            today_bonus = 0

        total = (value_for_likes + value_for_comments + today_bonus) - value_for_dislikes 

        return total


class Comment(models.Model):
    video      = models.ForeignKey(Video, on_delete=models.CASCADE)
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    comment    = models.CharField(max_length=300, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '{} by {}'.format(self.created_at, self.user.username)