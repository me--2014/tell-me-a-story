from rest_framework import viewsets
from django.contrib.auth.models import User
from blog.models import Story, Tag
from . import serialisers

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serialisers.UserSerializer

class StoryViewSet(viewsets.ModelViewSet):
        queryset = Story.objects.all()
        serializer_class = serialisers.StorySerializer

class TagViewSet(viewsets.ModelViewSet):
        queryset = Tag.objects.all()
        serializer_class = serialisers.TagSerializer