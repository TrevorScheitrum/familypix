from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from familypix.models import Photo, User, Circle, PhotoAlbum

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson

from familypix.forms import addCircleForm, addAlbumForm, addPhotoForm, addBatchPhotoForm
import boto
from itertools import chain
from django.contrib.auth.decorators import login_required


def addCircle(request):
    
    if request.method == 'POST':
        form = addCircleForm(request.POST)
        if form.is_valid():
            newCircle = form.save(commit=False)
            newCircle.owner = request.user
            newCircle.save()
            form.save_m2m()
    
    
    return redirect('index')

def addAlbum(request):
    
    if request.method == 'POST':
        
        form = addAlbumForm(request.POST)
        if form.is_valid():
            newAlbum = form.save(commit=False)
            newAlbum.owner = request.user
            newAlbum.save()
            form.save_m2m()
    
    
    return redirect('index')

def addPhoto(request):
    
    if request.method == 'POST':
        
        form = addPhotoForm(request.POST, request.FILES)
        users = []
        
        if form.is_valid():
            data = form.cleaned_data
            
            formPermissions = form.cleaned_data.get('permissions')
            
            for circles in formPermissions:
                circle = Circle.objects.get(id=circles.id)
                for user in circle.users.all():
                    print user.username
                    users.append(user.id)
                    
            formUsers = None
            
            if form.cleaned_data.get('users'):
                formUsers = form.cleaned_data.get('users')
                
            if formUsers is not None:
                for user in formUsers:
                    print user.username
                    users.append(user.id)
            
            newPhoto = Photo(owner=request.user, name=data['name'], photo=data['photo'])
            newPhoto.save()
            newPhoto.permissions.add(*users)
            newPhoto.save()
            #newPhoto = form.save(commit=False)
            #newPhoto.owner = request.user
            

            #form.save_m2m()
    
    
    return redirect('index')

def filePost(request):
    
    if request.method == 'POST':
        
        data = request.FILES
        
        users = []
        newPhoto = Photo(owner=request.user, name=data['file'].name, photo=data['file'])
        newPhoto.save()
        newPhoto.permissions.add(*users)
        newPhoto.save()
        #newPhoto = form.save(commit=False)
        #newPhoto.owner = request.user
        

        #form.save_m2m()
    
    
    return redirect('index')

def batchFilePost(request, index):
    if request.method == 'POST':
        
        image = request.FILES
        albumName = request.POST['batchFilename']
        batchName = albumName + " Photo "
        
        
        form = addBatchPhotoForm(request.POST, request.FILES)
        users = []
        
        if form.is_valid():
            data = form.cleaned_data
            
            formPermissions = form.cleaned_data.get('permissions')
            
            for circles in formPermissions:
                circle = Circle.objects.get(id=circles.id)
                for user in circle.users.all():
                    print user.username
                    users.append(user.id)
                    
            formUsers = None
            
            if form.cleaned_data.get('users'):
                formUsers = form.cleaned_data.get('users')
                
            if formUsers is not None:
                for user in formUsers:
                    print user.username
                    users.append(user.id)
    
        #users = []
        
        photoList = []
        
        for counter,file in enumerate(request.FILES):
            file = request.FILES['file['+`counter`+']']
            newCounter = counter +1;
            imageName =  request.POST["imageFilename["+`newCounter`+"]"]
            newPhoto = Photo(owner=request.user, name=imageName, photo=file)
            newPhoto.save()
            newPhoto.permissions.add(*users)
            newPhoto.save()
            photoList.append(newPhoto)
            
        
        newAlbum = PhotoAlbum(owner=request.user, name=albumName)
        newAlbum.save()
        newAlbum.photos.add(*photoList)
        newAlbum.save()
        #newPhoto = form.save(commit=False)
        #newPhoto.owner = request.user
        

        #form.save_m2m()
    
    
    return redirect('index')

def addAll(request):
    
    thisUser = None
    if request.user.is_authenticated():
        thisUser = request.user
    
        myCircles = Circle.objects.filter(owner=thisUser)

        myAlbums = PhotoAlbum.objects.filter(owner = thisUser)

        myPhotos = Photo.objects.filter(owner=thisUser)
    
        users = User.objects.all().order_by('name')
    
        circleForm = addCircleForm(request.POST)
    
        albumForm = addAlbumForm(request.POST)
        albumForm.fields['photos'].queryset = Photo.objects.filter(owner=thisUser)
        
        circleQuery = Circle.objects.filter(owner=thisUser)
        
        photoForm = addPhotoForm(request.POST)
        photoForm.fields['permissions'].queryset = circleQuery
        
    else:
        myCircles = None
        myAlbums = None
        myPhotos = None
        
        users = User.objects.all().order_by('name')
        circleForm = addCircleForm()
        albumForm = addAlbumForm()    
        photoForm = addPhotoForm()
    
    context = {'myCircles' : myCircles, 'myAlbums' : myAlbums, 'myPhotos' : myPhotos, 'users': users, 'circleForm' : circleForm, 'albumForm': albumForm, 'photoForm' : photoForm, 'requestPost' : request.POST}
    
    return render(request, 'familypix/addAll.html', context)


def index(request):
    
    thisUser = None
    if request.user.is_authenticated():
        thisUser = request.user
    
        myCircles = Circle.objects.filter(owner=thisUser)
        
        myAlbums = PhotoAlbum.objects.filter(owner = thisUser)

        myPhotos = Photo.objects.filter(owner=thisUser)
    
        users = User.objects.all().order_by('name')
    
        circleForm = addCircleForm(request.POST)
    
        albumForm = addAlbumForm(request.POST)
        albumForm.fields['photos'].queryset = Photo.objects.filter(owner=thisUser)
        
        circleQuery = Circle.objects.filter(owner=thisUser)
        
        photoForm = addPhotoForm(request.POST)
        photoForm.fields['permissions'].queryset = circleQuery
        
    else:
        myCircles = None
        myAlbums = None
        myPhotos = None
        
        users = User.objects.all().order_by('name')
        circleForm = addCircleForm()
        albumForm = addAlbumForm()    
        photoForm = addPhotoForm()
    
    context = {'myCircles' : myCircles, 'myAlbums' : myAlbums, 'myPhotos' : myPhotos, 'users': users, 'circleForm' : circleForm, 'albumForm': albumForm, 'photoForm' : photoForm, 'requestPost' : request.POST}
    
    return render(request, 'familypix/index.html', context)

def photoUpload(request):
    
    thisUser = None
    if request.user.is_authenticated():
        thisUser = request.user
    
        myCircles = Circle.objects.filter(owner=thisUser)

        myAlbums = PhotoAlbum.objects.filter(owner = thisUser)

        myPhotos = Photo.objects.filter(owner=thisUser)
    
        users = User.objects.all().order_by('name')
    
        circleForm = addCircleForm(request.POST)
    
        albumForm = addAlbumForm(request.POST)
        albumForm.fields['photos'].queryset = Photo.objects.filter(owner=thisUser)
        
        circleQuery = Circle.objects.filter(owner=thisUser)
        
        photoForm = addPhotoForm(request.POST)
        photoForm.fields['permissions'].queryset = circleQuery
        
    else:
        myCircles = None
        myAlbums = None
        myPhotos = None
        
        users = User.objects.all().order_by('name')
        circleForm = addCircleForm()
        albumForm = addAlbumForm()    
        photoForm = addPhotoForm()
    
    context = {'myCircles' : myCircles, 'myAlbums' : myAlbums, 'myPhotos' : myPhotos, 'users': users, 'circleForm' : circleForm, 'albumForm': albumForm, 'photoForm' : photoForm, 'requestPost' : request.POST}
    
    return render(request, 'familypix/photoUpload.html', context)
    
    

@login_required()
def albumUpload(request):
    thisUser = None
    if request.user.is_authenticated():
        thisUser = request.user
    
        myCircles = Circle.objects.filter(owner=thisUser)

        myAlbums = PhotoAlbum.objects.filter(owner = thisUser)

        myPhotos = Photo.objects.filter(owner=thisUser)
    
        users = User.objects.all().order_by('name')
    
        circleForm = addCircleForm(request.POST)
    
        albumForm = addAlbumForm(request.POST)
        albumForm.fields['photos'].queryset = Photo.objects.filter(owner=thisUser)
        
        circleQuery = Circle.objects.filter(owner=thisUser)
        
        photoForm = addPhotoForm(request.POST)
        photoForm.fields['permissions'].queryset = circleQuery
        
        batchPhotoForm = addBatchPhotoForm(request.POST)
        batchPhotoForm.fields['permissions'].queryset = circleQuery
        
    else:
        myCircles = None
        myAlbums = None
        myPhotos = None
        
        
        users = User.objects.all().order_by('name')
        circleForm = addCircleForm()
        albumForm = addAlbumForm()    
        photoForm = addPhotoForm()
        batchPhotoForm = addBatchPhotoForm()
    
    context = {'myCircles' : myCircles, 'myAlbums' : myAlbums, 'myPhotos' : myPhotos, 'users': users, 'circleForm' : circleForm, 'albumForm': albumForm, 'photoForm' : photoForm, 'requestPost' : request.POST, 'batchPhotoForm' : batchPhotoForm,}
    
    return render(request, 'familypix/albumUpload.html', context)


def album(request, userpage):
    
    thisUser = None
    if request.user.is_authenticated():
        thisUser = request.user
    
    URLuser = User.objects.get(username = userpage)
    
    circles = Circle.objects.filter(owner = URLuser)
    
    permission = 0
    circlesImIn = []
    
    for circle in circles.all():
        circleObj = Circle.objects.get(name=circle)
        for user in circleObj.users.all():
            if(user == thisUser):
                permission = 1
                circlesImIn.append(circleObj)
    
    photos = []
    
    for circle in circlesImIn:
        photos.extend(Photo.objects.filter(permissions = circle.pk))
    photos.extend(Photo.objects.filter(permissions = thisUser.id))
    
    albums = PhotoAlbum.objects.all().order_by("name")
    
    #context = {'photos' : photos, 'albums' : albums, 'username' : username, 'circles' : circles}
    context = {'thisUser' : thisUser, 'URLuser' : URLuser, 'circles' : circles, 'permission' : permission,  'circlesImIn' : circlesImIn, 'photos' : photos, 'albums' : albums}
    return render(request, 'familypix/album.html', context)
    