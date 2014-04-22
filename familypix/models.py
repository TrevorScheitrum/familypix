from BeautifulSoup import BeautifulSoup
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.fields.related import ManyToManyField
from django.utils.html import format_html
from django_resized import ResizedImageField

# Create your models here.

class Person(models.Model):
    name = models.CharField(max_length = 200)
    user = models.ManyToManyField(User)
    
    def __unicode__(self):
        return self.name

class Circle(models.Model):
    name = models.CharField(max_length = 200)
    person = models.ManyToManyField(Person, blank = True)
    
    def __unicode__(self):
        return self.name

class Photo(models.Model):
    name = models.CharField(max_length = 200)
    photo = models.ImageField(upload_to = 'Uploads/')
    permissions = ManyToManyField(Circle)
    
    def __unicode__(self):
        return self.name