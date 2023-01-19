from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, UserManager
from django.db import models
from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
from django.urls import reverse

from sign.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class Bulletin(models.Model):
    title = models.CharField(max_length=150)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from='title', unique=True)

    def __str__(self):
        return f'{self.title} ({self.author.username})'

    def get_absolute_url(self):
        return reverse('bulletin', kwargs={'slug': self.slug})


class Response(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    bulletin = models.ForeignKey(Bulletin, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)
