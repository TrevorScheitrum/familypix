from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from familypix.models import Photo, User, Circle, Person

from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponse
from django.utils import simplejson

from django.conf import settings
import boto




def index(request):
    
    circle_list = Circle.objects.all().order_by('name')
    
    context = {'circles' : circle_list}
    
    return render(request, 'familypix/index.html', context)
    
def album(request):
    
    photo_list = Photo.objects.filter(permissions = 2)
    
    context = {'photos' : photo_list}
    
    return render(request, 'familypix/album.html', context)
    