from rest_framework import viewsets
from django.contrib.auth.models import User
from blog.models import Story
from . import serialisers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serialisers.UserSerializer

class StoryViewSet(viewsets.ModelViewSet):
        queryset = Story.objects.all()
        serializer_class = serialisers.StorySerializer