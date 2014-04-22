from django.contrib import admin
from familypix.models import Photo, Circle, Person
    
class PhotoInline(admin.StackedInline):
    model = Photo
    extra = 3
    
class PhotoAdmin(admin.ModelAdmin):
    fields = ('name', 'photo', 'permissions',)

class CircleAdmin(admin.ModelAdmin):
    model = Circle
    fields = ('name', 'person',)
    
class PersonAdmin(admin.ModelAdmin):
    model = Person
    fields = ('name','user',)

#myModels = [Article,ArticleAdmin]
#admin.site.register(myModels)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Circle, CircleAdmin)
admin.site.register(Person, PersonAdmin)
