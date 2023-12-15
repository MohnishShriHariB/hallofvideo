from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
from .models import Hall,Video
from .forms import Videoform,Searchform
from django.forms.utils import ErrorList
from django.http import Http404,JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import urllib
import requests
import random
# Create your views here.

YOUTUBE_API_KEY="AIzaSyDAfSMwf6EG35hHhZbE3PTM6QUOTBsQ5S0"

def home(request):
    recenthalls=Hall.objects.all().order_by('-id')[:3]
    popularhalls=Hall.objects.all()[:1]
    return render(request,"hall/home.html",{'recent':recenthalls,'popular':popularhalls})

@login_required
def dashboard(request):
    halls=Hall.objects.filter(user=request.user)
    return render(request,"hall/dashboard.html",{'halls':halls})

class Signup(generic.CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy('dashboard')
    template_name="registration/signup.html"

    def form_valid(self,form):
        view=super(Signup,self).form_valid(form)
        username,password=form.cleaned_data.get("username"),form.cleaned_data.get("password1")
        user=authenticate(username=username,password=password)
        login(self.request,user)
        return view

class Createhall(LoginRequiredMixin,generic.CreateView):
    model=Hall
    fields=['title']
    template_name="hall/createhall.html"
    success_url=reverse_lazy("home")

    def form_valid(self,form):
        form.instance.user=self.request.user
        super(Createhall,self).form_valid(form)
        return redirect("dashboard")


class Detailhall(generic.DetailView):
    model=Hall
    template_name="hall/Detailhall.html"

class Updatehall(LoginRequiredMixin,generic.UpdateView):
    model=Hall
    template_name="hall/Updatehall.html"
    fields=['title']
    success_url=reverse_lazy("dashboard")

    def get_object(self):
        hall=super(Updatehall,self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        else:
            return hall

class Deletehall(LoginRequiredMixin,generic.DeleteView):
    model=Hall
    template_name="hall/deletehall.html"
    success_url=reverse_lazy("dashboard")

    def get_object(self):
        hall=super(Deletehall,self).get_object()
        if not hall.user == self.request.user:
            raise Http404
        else:
            return hall

@login_required
def Addvideo(request,pk):
    form=Videoform()
    search_form=Searchform()
    hall=Hall.objects.get(pk=pk)
    if not hall.user == request.user:
        raise Http404
    if request.method=="POST":
        form=Videoform(request.POST)
        if form.is_valid():
            video=Video()
            video.url=form.cleaned_data.get("url")
            video.hall=hall
            parse_url=urllib.parse.urlparse(video.url)
            video_id=urllib.parse.parse_qs(parse_url.query).get('v')
            if video_id:
                video.youtube_id=video_id[0]
                response=requests.get(f"https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={ video_id[0] }&key={ YOUTUBE_API_KEY }")
                json=response.json()
                title=json['items'][0]['snippet']['title']
                video.title=title
                video.save()
                return redirect("Detailhall",pk)
            else:
                errors=form._errors.setdefault('url',ErrorList())
                errors.append("Needs to be a YouTube Link")

    return render(request,"hall/addvideo.html",{"form":form,"search_form":search_form})

@login_required
def searchvideo(request):
    search_form=Searchform(request.GET)
    if search_form.is_valid():
        encoded_search_text=urllib.parse.quote(search_form.cleaned_data['search_term'])
        response=requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={ encoded_search_text }&key={ YOUTUBE_API_KEY }')
        return JsonResponse(response.json())
    return JsonResponse({"error":"not found"})

class deletevideo(LoginRequiredMixin,generic.DeleteView):
    model=Video
    template_name="hall/deletevideo.html"
    success_url=reverse_lazy("dashboard")

    def get_object(self):
        video=super(deletevideo,self).get_object()
        if not video.hall.user == self.request.user:
            raise Http404
        else:
            return video
