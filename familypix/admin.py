from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from familypix.models import Photo, Circle, PhotoAlbum, contactList
    
class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 3
    
class PhotoAdmin(admin.ModelAdmin):
    model = Photo
    #fields = ('name', 'photo', 'permissions',)
    
class PhotoAlbumAdmin(admin.ModelAdmin):
    model = PhotoAlbum
    #fields = ('name', 'photos',)

class CircleAdmin(admin.ModelAdmin):
    model = Circle
    #fields = ('owner','name', 'users')

class contactListAdmin(admin.ModelAdmin):
    model = contactList

#myModels = [Article,ArticleAdmin]
#admin.site.register(myModels)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Circle, CircleAdmin)
admin.site.register(contactList, contactListAdmin)
admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
