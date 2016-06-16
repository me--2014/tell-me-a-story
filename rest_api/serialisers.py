from rest_framework import serializers
from django.contrib.auth.models import User
from blog.models import Story

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')


class StorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Story
        fields = ('id', 'title', 'storytext')