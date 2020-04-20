from django.test import TestCase
from django.urls import reverse

from login.models import User


class RegisterViewTests(TestCase):

    def test_register(self):
        """正常注册"""
        data = {'username': 'zzy', 'password': '1234'}
        response = self.client.post(reverse('login:register'), data)
        self.assertRedirects(response, reverse('login:index') + '?message=注册成功')

    def test_existing_username(self):
        """用户名已存在"""
        User.objects.create(username='zzy', password=User.encrypt_password('1234'))
        data = {'username': 'zzy', 'password': '1234'}
        response = self.client.post(reverse('login:register'), data)
        self.assertTemplateUsed(response, 'login/register.html')
        self.assertContains(response, '用户名已存在')


class LoginViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='zzy', password=User.encrypt_password('1234'))

    def test_login(self):
        """正常登录"""
        data = {'username': 'zzy', 'password': '1234'}
        response = self.client.post(reverse('login:login'), data, follow=True)
        self.assertRedirects(response, reverse('login:index'))
        self.assertEqual(self.client.session.get('username'), 'zzy')
        self.assertContains(response, '欢迎，zzy！')

    def test_wrong_username(self):
        """用户名错误"""
        data = {'username': 'abc', 'password': '1234'}
        response = self.client.post(reverse('login:login'), data)
        self.assertTemplateUsed(response, 'login/login.html')
        self.assertContains(response, '用户名或密码错误')

    def test_wrong_password(self):
        """密码错误"""
        data = {'username': 'zzy', 'password': '123'}
        response = self.client.post(reverse('login:login'), data)
        self.assertTemplateUsed(response, 'login/login.html')
        self.assertContains(response, '用户名或密码错误')


class LogoutViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='zzy', password=User.encrypt_password('1234'))

    def test_logout(self):
        """正常注销"""
        data = {'username': 'zzy', 'password': '1234'}
        self.client.post(reverse('login:login'), data, follow=True)
        response = self.client.get(reverse('login:logout'), follow=True)
        self.assertRedirects(response, reverse('login:index') + '?message=注销成功')
        self.assertNotIn('username', self.client.session)
