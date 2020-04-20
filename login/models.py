import hashlib

from django.db import models


class User(models.Model):
    """用户实体类"""
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=40)

    def __str__(self):
        return self.username

    @classmethod
    def encrypt_password(cls, password):
        """使用SHA-1加密密码，返回长度为40的加密后的字符串。"""
        return hashlib.sha1(password.encode()).hexdigest()
