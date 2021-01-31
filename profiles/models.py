# -*- coding: utf-8 -*-

# Python

# Django
from django.db                  import models
from django.contrib.auth.models import User

# Project
from videos.models              import Video

class History(models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    video      = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name        = "History"
        verbose_name_plural = "Histories"

    def __str__(self):
        return "[{}] {}".format(self.created_at, self.video)

