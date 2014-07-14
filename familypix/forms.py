from django import forms
from django.forms import ModelForm
from familypix.models import Circle, Photo, PhotoAlbum, User

class addCircleForm(ModelForm):
    class Meta:
        model = Circle
        exclude = ('owner',)

class addAlbumForm(ModelForm):
    class Meta:
        model = PhotoAlbum
        exclude = ('owner',)
        
class addPhotoForm(ModelForm):
    users = forms.ModelMultipleChoiceField(User.objects.all().order_by('username'), required=False)
    class Meta:
        model = Photo
        exclude = ('owner',)


class addBatchPhotoForm(ModelForm):
    users = forms.ModelMultipleChoiceField(User.objects.all().order_by('username'), required=False)
    class Meta:
        model = Photo
        exclude = ('owner','name','photo',)