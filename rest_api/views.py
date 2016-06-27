from rest_framework import viewsets
from django.contrib.auth.models import User
from blog.models import Story, Tag
from . import serialisers
from rest_framework.decorators import list_route

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serialisers.UserSerializer

class StoryViewSet(viewsets.ModelViewSet):
        queryset = Story.objects.all()
        serializer_class = serialisers.StorySerializer

        def get_queryset(self):
            queryset = Story.objects.all()
            tagId = self.request.query_params.get('tag_id', None)
            if tagId is not None:
                queryset = queryset.filter(tags__id=tagId)
            titleText = self.request.query_params.get('title_text', None)
            if titleText is not None:
                queryset = queryset.filter(title__icontains=titleText)
            return queryset

class TagViewSet(viewsets.ModelViewSet):
        queryset = Tag.objects.all()
        serializer_class = serialisers.TagSerializer