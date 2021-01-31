# -*- coding: utf-8 -*-

# Python

# Django
from django.conf             import settings
from django.conf.urls.static import static
from django.contrib          import admin
from django.urls             import path, include
from videos.views            import VideoListView

# Project

urlpatterns = [
    path (route='', view=VideoListView.as_view(), name='list'),
    path('videos/', include(('videos.urls', 'videos'), namespace='videos')),
    path('admin/', admin.site.urls), 
    path('users/', include(('profiles.urls', 'profiles'), namespace='profiles')),
] 
