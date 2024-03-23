import os

from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django_resized import ResizedImageField
from django.contrib.auth.models import User, AbstractUser
from django.core.validators import FileExtensionValidator


# Авторы
class User(AbstractUser):
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=True)

    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [GinIndex(fields=["search_vector", ]), ]

    def __str__(self):
        return self.username

    def update_search_vector(self):
        qs = User.objects.filter(pk=self.pk)
        qs.update(search_vector=SearchVector('username'))

    @classmethod
    def get_class(cls):
        return cls.__name__

    def get_username(self):
        return self.username


# Инструменталы
class Songs(models.Model):
    name = models.CharField(max_length=21)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.FileField(upload_to='songs/', validators=[FileExtensionValidator(allowed_extensions=
                                                                                   ['mp3', 'wav'])])
    cover = ResizedImageField(upload_to='covers/', size=[225, 225], default='covers/default.png')
    text = models.TextField(default=None, blank=True)
    temp = models.PositiveSmallIntegerField(default=0)
    ton = models.CharField(default=None, max_length=6)
    hashtags = models.CharField(default=None, max_length=100, blank=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)

    price = models.PositiveIntegerField(default=0)

    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        indexes = [GinIndex(fields=["search_vector", ]), ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    def update_search_vector(self):
        qs = Songs.objects.filter(pk=self.pk)
        qs.update(search_vector=SearchVector("name", "temp", "ton", "hashtags"))

    # Возвращает название модели объекта
    @classmethod
    def get_class(cls):
        return cls.__name__


# Сигналы

# После удаления объекта в бд удаляются файлы из бд
@receiver(post_delete, sender=Songs)
def delete_song_files(sender, instance, **kwargs):
    # Удаляем файл с мелодией
    if instance.file:
        file_path = instance.file.path
        if os.path.exists(file_path):
            os.remove(file_path)

    # Удаляем файл с обложкой
    if instance.cover:
        cover_path = instance.cover.path
        if os.path.exists(cover_path):
            os.remove(cover_path)


# После создания или изменения объекта пересоздается search_vector
@receiver(post_save, sender=Songs)
@receiver(post_save, sender=User)
def update_search_vector(sender, instance, created, update_fields, **kwargs):
    instance.update_search_vector()
