from django.shortcuts import render
from rest_framework import viewsets
from .serializers import Proj1Serializer
from .models import Proj1

# Create your views here.

class Proj1View(viewsets.ModelViewSet):
    serializer_class = Proj1Serializer
    queryset = Proj1.objects.all()

