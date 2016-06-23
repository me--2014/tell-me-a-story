from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Story, Tag

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class StorySerializer(serializers.HyperlinkedModelSerializer):
    tags = serializers.HyperlinkedRelatedField(many=True, view_name='tag-detail', queryset=Tag.objects.all())
    class Meta:
        model = Story
        fields = ('id', 'url', 'title', 'hook', 'storytext', 'dateposted', 'wordcount', 'author', 'tags')
        # add 'url' to fields

class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ('id', 'url', 'name')