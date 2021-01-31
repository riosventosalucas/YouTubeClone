# -*- coding: utf-8 -*-

# Python

# Django

from django.contrib.auth.views  import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts           import render, redirect
from django.urls                import reverse_lazy
from django.views.generic       import FormView, ListView

# Project
from .forms                     import SignupForm
from .models                    import History

class SignupUserView(FormView):
    form_class    = SignupForm
    template_name = "profiles/signup.html"
    success_url   = reverse_lazy("profiles:login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class LoginUserView(LoginView):
    template_name = "profiles/login.html"

class LogoutUserView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("profiles:login")


class HistoryView(ListView):
    model               =  History
    template_name       = "profiles/history.html"
    context_object_name = "histories"
    paginate_by         = 10

    def get_queryset(self):
        queryset = History.objects.filter(user=self.request.user).order_by('-created_at')
        return queryset