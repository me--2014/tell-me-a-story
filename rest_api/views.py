from rest_framework import viewsets
from django.contrib.auth.models import User
from blog.models import Story, Tag, Favourite
from . import serialisers
from rest_framework.decorators import list_route

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serialisers.UserSerializer

class StoryViewSet(viewsets.ModelViewSet):
        queryset = Story.objects.all().order_by('-dateposted').order_by('title')
        serializer_class = serialisers.StorySerializer

        def get_queryset(self):
            queryset = Story.objects.all().order_by('-dateposted').order_by('title')

            # If tag id provided, filter by tag
            tagId = self.request.query_params.get('tag_id', None)
            if tagId != '0' and tagId is not None:
                queryset = queryset.filter(tags__id=tagId)

            # If snippet of text provided, filter by title
            titleText = self.request.query_params.get('title_text', None)
            if titleText is not None:
                queryset = queryset.filter(title__icontains=titleText)

            # If user provided, add is_fav field
            userId = self.request.query_params.get('user_id', None)
            if userId != '0' and userId is not None:
                favs_queryset = Favourite.objects.filter(user=userId);
                favs = set([])
                for fav in favs_queryset:
                    favs.add(fav.story.id)
                for item in queryset:
                    if item.id in favs:
                        item.is_fav = True
                    else:
                        item.is_fav = False
            return queryset

class TagViewSet(viewsets.ModelViewSet):
        queryset = Tag.objects.all()
        serializer_class = serialisers.TagSerializer