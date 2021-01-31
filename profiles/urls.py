# -*- coding: utf-8 -*-

# Python

# Django
from django.contrib.auth.decorators import login_required
from django.urls                    import path

# Project
from .                              import views


urlpatterns = [
    path(
        route = 'signup/',
        view  = views.SignupUserView.as_view(),
        name  = 'signup'),
    path(
        route = 'login/',
        view  = views.LoginUserView.as_view(),
        name  = 'login'),
    path(
        route = 'logout/',
        view  = views.LogoutUserView.as_view(),
        name  = 'logout'),
    path(
        route = 'history/',
        view  = login_required(views.HistoryView.as_view()),
        name  = 'history'),
]
