from django.shortcuts import render
from django.views import View
from django.http.response import HttpResponse
# Create your views here.


class HomeView(View):
     
    def get(self, request, *args, **kwargs):
        return render(request, 'blog/home.html')