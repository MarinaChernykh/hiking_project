from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms


User = get_user_model()


class UserTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client()
        cls.user = User.objects.create_user(username='Test User')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

    def test_anonim_user_urls_exist_and_use_correct_templates(self):
        """
        URLs are available for anonimous users
        and uses customized user templates.
        """
        url_names_templates = {
            'users:signup': 'users/signup.html',
            'users:login': 'users/login.html',
            'users:password_reset':
                'users/password_reset_form.html',
            'users:password_reset_done':
                'users/password_reset_done.html',
            'users:password_reset_complete':
                'users/password_reset_complete.html'
        }
        for url_name, template in url_names_templates.items():
            with self.subTest(url_name=url_name):
                response = self.guest_client.get(reverse(url_name))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_authorized_user_urls_exist_and_use_correct_templates(self):
        """
        URLs are available for auth users and uses customized user templates.
        """
        url_names_templates = {
            'users:password_change': 'users/password_change_form.html',
            'users:password_change_done': 'users/password_change_done.html',
        }
        for url_name, template in url_names_templates.items():
            with self.subTest(url_name=url_name):
                response = self.authorized_client.get(reverse(url_name))
                self.assertEqual(response.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(response, template)

    def test_signup_page_shows_correct_context(self):
        """Signup template gets correct context."""
        response = self.guest_client.get(reverse('users:signup'))
        form_fields = {
            'username': forms.fields.CharField,
            'email': forms.fields.EmailField,
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_create_user(self):
        """Post request with valid data creates new user."""
        users_count = User.objects.count()
        form_data = {
            'username': 'some_test_user',
            'email': 'abc@gmail.com',
            'password1': '1h23kLsifklw',
            'password2': '1h23kLsifklw'
        }
        response = self.guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse('trails:index'))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.latest_user = User.objects.latest('pk')
        self.assertEqual(self.latest_user.username, 'some_test_user')
        self.assertEqual(self.latest_user.email, 'abc@gmail.com')
