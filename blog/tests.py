"""
Test suite for blog application. To run use command 'python manage.py test blog'.
"""

from django.test import TestCase, SimpleTestCase
from .models import Tag, Story, User, Favourite
from datetime import date
import json
import collections
from urllib import quote
from rest_framework.parsers import JSONParser
import datetime
from operator import itemgetter

# TO DO: f these are only used by stories class it may be sensible to move them within that class

encoded_string_first = quote("first")
encoded_string_story = quote("story")
encoded_string_ending = quote("ending")
query_strings_valid_filled = ['', 'user_id=0', 'user_id=1', 'tag_id=0', 'tag_id=1',
                              'title_text=' + encoded_string_first,
                              'title_text=' + encoded_string_story, 'user_id=1&tag_id=2',
                              'user_id=1&title_text=' + encoded_string_first,
                              'tag_id=3&title_text=' + encoded_string_story]
query_strings_valid_empty = ['user_id=2', 'tag_id=7', 'title_text=' + encoded_string_ending,
                             'user_id=99&tag_id=2', 'user_id=1&title_text=' + encoded_string_ending,
                             'tag_id=1000&title_text=' + encoded_string_story]
query_strings_user = ['user_id=1', 'user_id=1&tag_id=2', 'user_id=1&title_text=' + encoded_string_first,
                      'user_id=1&tag_id=2&title_text=' + encoded_string_story]


class CheckStories(TestCase):
    def setUp(self):
        tag1 = Tag.objects.create(id=1, name="short")
        tag1.save()
        tag2 = Tag.objects.create(id=2, name="long")
        tag2.save()
        tag3 = Tag.objects.create(id=3, name="romantic")
        tag3.save()

        story1 = Story.objects.create(id=1, title="My first story", storytext="Once upon a time",
                                      dateposted="2010-12-19")
        story1.save()
        story1.tags.add(tag1, tag3)
        story2 = Story.objects.create(id=2, title="My second story", storytext="Happy ever after",
                                      dateposted="2010-01-30")
        story2.save()
        story2.tags.add(tag2, tag3)
        story3 = Story.objects.create(id=3, title="My third story", storytext="Three brown mice\nSee how they run",
                                      dateposted="2010-01-30")
        story3.save()
        story3.tags.add(tag2)

        user1 = User.objects.create(id=1, name="anon")
        user1.save()

        fav1 = Favourite.objects.create(id=1, story=story3, user=user1)
        fav1.save()

    def test_json_response_provided(self):
        """
        Check that different combinations of valid parameters result in a JSON response
        """

        # Check query strings which should return a JSON response with content
        url = '/rest-api/stories/'
        json_response = self.client.get(url)
        self.assertIsNotNone(json_response)
        filled = False
        if len(json_response.content) > 0:
            filled = True
        self.assertTrue(filled)

        url += '?'
        json_response = self.client.get(url)
        self.assertIsNotNone(json_response)
        filled = False
        if len(json_response.content) > 0:
            filled = True
        self.assertTrue(filled)

        for item in query_strings_valid_filled:
            current_url = url + item
            json_response = self.client.get(current_url)
            self.assertIsNotNone(json_response)
            filled = False
            if len(json_response.content) > 0:
                filled = True
            self.assertTrue(filled)

        #  Check query strings which should return an empty JSON response
        url = '/rest-api/stories/'
        for item in query_strings_valid_empty:
            current_url = url + item
            json_response = self.client.get(current_url)
            self.assertIsNotNone(json_response)
            empty = False
            if len(json_response.content) == 0:
                empty = True
            self.assertTrue(empty)

        #  Check invalid query strings

        json_response = self.client.get('rest-api/stories/tag_id=2')  # Missing the '?' from start of querystring
        self.assertEqual(json_response.status_code, 404)

        with self.assertRaises(ValueError):
            self.client.get('/rest-api/stories/?tag_id=1title_text=hello')  # Missing the '&' between parameters

        json_response = self.client.get('rest-api/stories/uesr_id=1')  # Parameter name is misspelled
        self.assertEqual(json_response.status_code, 404)

    def test_response_contains_correct_headings(self):
        """
        Check that stories sent in the response contain headings such as id, title, dateposted, etc
        """

        #  Check that Story model fields are included in the response
        url = '/rest-api/stories/'
        json_response = self.client.get(url)
        self.assertContains(json_response, 'id')
        self.assertContains(json_response, 'title')
        self.assertContains(json_response, 'hook')
        self.assertContains(json_response, 'storytext')
        self.assertContains(json_response, 'dateposted')
        self.assertContains(json_response, 'wordcount')
        self.assertContains(json_response, 'author')
        self.assertContains(json_response, 'tags')
        url += '?'
        for item in query_strings_valid_filled:
            current_url = url + item
            json_response = self.client.get(current_url)
            self.assertContains(json_response, 'id')
            self.assertContains(json_response, 'title')
            self.assertContains(json_response, 'hook')
            self.assertContains(json_response, 'storytext')
            self.assertContains(json_response, 'dateposted')
            self.assertContains(json_response, 'wordcount')
            self.assertContains(json_response, 'author')
            self.assertContains(json_response, 'tags')

        # When a user is provided, check that is_fav field has been added
        url = '/rest-api/stories/?'
        for item in query_strings_user:
            current_url = url + item
            json_response = self.client.get(current_url)
            self.assertContains(json_response, 'is_fav')

    def test_no_id_duplicated(self):
        """
        Check that there are no duplicate story ids
        """
        url = '/rest-api/stories/'
        json_response = self.client.get(url)
        ids = []

        for story in json_response.data:
            ids.append(story['id'])

        ids_set = []
        failures = 0
        for item in ids:
            if item in ids_set:
                failures += 1
            ids_set.append(item)
        self.assertEqual(failures, 0)

    def test_order(self):
        """
        Check that stories are ordered by date then title
        """
        url = '/rest-api/stories/'
        json_response = self.client.get(url)
        story_dates = []

        # Get dateposted and title from each story
        for story in json_response.data:
            date_info = story['dateposted'].split('-')
            story_date = datetime.date(int(date_info[0]), int(date_info[1]), int(date_info[2]))
            story_title = story['title']
            story_dates.append((story_date, story_title))

        # Create sorted version
        story_dates_ordered = sorted(story_dates, key=itemgetter(0), reverse=True)
        story_dates_ordered = sorted(story_dates_ordered, key=itemgetter(1))

        # Compare original and sorted versions, which should be the same
        i = 0
        failures = 0
        for item in story_dates:
            if item is not story_dates_ordered[i]:
                failures += 1
            i += 1

        self.assertEqual(failures, 0)

    def test_line_breaks(self):
        """
        Check that stories with line breaks contain '\n'
        """
        url = '/rest-api/stories/3/'
        json_response = self.client.get(url)
        self.assertContains(json_response, '\\n')


class CheckTags(TestCase):

    def setUp(self):
        tag1 = Tag.objects.create(id=1, name="short")
        tag1.save()
        tag2 = Tag.objects.create(id=2, name="long")
        tag2.save()
        tag3 = Tag.objects.create(id=3, name="romantic")
        tag3.save()

        story1 = Story.objects.create(id=1, title="My first story", storytext="Once upon a time",
                                      dateposted="2010-12-19")
        story1.save()
        story1.tags.add(tag1, tag3)
        story2 = Story.objects.create(id=2, title="My second story", storytext="Happy ever after",
                                      dateposted="2010-01-30")
        story2.save()
        story2.tags.add(tag2, tag3)
        story3 = Story.objects.create(id=3, title="My third story", storytext="Three brown mice\nSee how they run",
                                      dateposted="2010-01-30")
        story3.save()
        story3.tags.add(tag2)

        user1 = User.objects.create(id=1, name="anon")
        user1.save()

        fav1 = Favourite.objects.create(id=1, story=story3, user=user1)
        fav1.save()

    def test_response_contains_correct_headings(self):
        """
        Check that tags sent in the response contain headings such as 'id'
        """

        urls = ['/rest-api/tags/', '/rest-api/tags/?', '/rest-api/tags/2/', ]

        for url in urls:
            json_response = self.client.get(url)
            self.assertContains(json_response, 'id')
            self.assertContains(json_response, 'name')

    def test_all_ids_unique(self):
        """
        Check that there are no duplicate tag ids in the response
        """

        # TO DO: add this test