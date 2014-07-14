from BeautifulSoup import BeautifulSoup
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.db.models.fields.related import ManyToManyField
from django.utils.html import format_html
from django_resized import ResizedImageField
from django.db.models.signals import post_save

# Create your models here.

#class Profile(models.Model):
#    user = models.OneToOneField(User)
#    #circles = models.ManyToManyField(Circle, null=True, blank=True)
#    #albums = models.ManyToManyField(PhotoAlbum, null=True, blank=True)
#    #photos = models.ManyToManyField(Photo, null=True, blank=True)
#    
#    def __unicode__(self):
#        return self.user.username

class Circle(models.Model):
    owner = models.ForeignKey(User, related_name="owner")
    name = models.CharField(max_length = 200)
    users = models.ManyToManyField(User, related_name="users")
    
    def __unicode__(self):
        return self.name

class Photo(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length = 200)
    photo = models.ImageField(upload_to = 'Uploads/', null=True, blank=True)
    permissions = ManyToManyField(User, null=True, blank=True, related_name="permissions")
    
    def __unicode__(self):
        return self.name
    
class PhotoAlbum(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=200)
    photos = models.ManyToManyField(Photo, null=True, blank=True)
    
    def __unicode__(self):
        return self.name
    
class contactList(models.Model):
    owner = models.ForeignKey(User)
    contacts = models.ManyToManyField(User, related_name="contacts")
    
    
    
#def create_user_profile(sender, **kwargs):
#    """When creating a new user, make a profile for him or her."""
#    u = kwargs["instance"]
#    if not Profile.objects.filter(user=u):
#        Profile(user=u).save()
#
#post_save.connect(create_user_profile, sender=User)