from __future__ import unicode_literals
from django.db import models

class Tag(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Story(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, null=True)
    hook = models.TextField(blank=True, null=True)
    storytext = models.TextField(null=True)
    dateposted = models.DateField(blank=True, null=True)
    wordcount = models.IntegerField(blank=True, null=True)
    author = models.CharField(max_length=255, blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)
    audiofile = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.title

class User(models.Model): # may want to use User from django.contrib.auth.models instead of creating own class
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, default="User")

    def __str__(self):
        return unicode(self.name)

class Favourite(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User)
    story = models.ForeignKey(Story)