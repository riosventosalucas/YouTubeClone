# -*- coding: utf-8 -*-

# Python
from faker                      import Factory

# Django
from django.test                import TestCase
from django.contrib.auth.models import User
from django.urls                import reverse

# Project
from profiles.forms             import SignupForm


# Create your tests here.
faker = Factory.create()

class TestProfilesViews(TestCase):

    def setUp(self):
        test_user = User.objects.create_user(
            username='test_user',
            password='123456')
        test_user.save()        

    def test_render_correct_template_sign_up(self):
        resp = self.client.get(reverse('profiles:signup'))
        self.assertEqual(resp.status_code, 200)

    def test_redirect_after_signup(self):
        resp = self.client.post(reverse('profiles:signup'), data={'username':'test_user', 'password':'123456', 'password_confirmation':'123456'})
        self.assertEqual(resp.status_code, 200)
    
    def test_logout(self):
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('profiles:logout'))
        self.assertEqual(resp.status_code, 302)

    def test_signup_fail(self):
        resp = self.client.post(reverse('profiles:signup'), data={'username':'test_user', 'password':'123456', 'password_confirmation':'12346'})
        self.assertEqual(resp.status_code, 200)

    def test_history_as_login_user(self):
        login = self.client.login(username='test_user', password='123456')
        resp = self.client.get(reverse('profiles:history'))
        self.assertEqual(resp.status_code, 200)

    def test_history_as_anonymouse_user(self):
        resp = self.client.get(reverse('profiles:history'))
        self.assertEqual(resp.status_code, 302)