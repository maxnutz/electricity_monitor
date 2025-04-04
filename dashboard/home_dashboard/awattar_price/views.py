from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    """Landing page for price dashboard"""
    context: dict = {"title": "Price Dashboard"}
    return HttpResponse("aWATTar Price Dashboard")
