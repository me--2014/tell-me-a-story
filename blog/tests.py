"""
Test suite for blog application. To run use command 'python manage.py test blog'.
Note: SimpleTestCase contains useful additional assert methods.
"""

from django.test import TestCase, SimpleTestCase
from .models import Tag, Story, User, Favourite
from datetime import date
import json, collections
from urllib import quote
from rest_framework.parsers import JSONParser

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

class checkStories(TestCase):
    def setUp(self):
        tag1 = Tag.objects.create(id=1, name="short")
        tag1.save()
        tag2 = Tag.objects.create(id=2, name="long")
        tag2.save()
        tag3 = Tag.objects.create(id=3, name="romantic")
        tag3.save()

        story1 = Story.objects.create(id=1, title="My first story", storytext="Once upon a time")
        story1.save()
        story1.tags.add(tag1, tag3)
        story2 = Story.objects.create(id=2, title="My second story", storytext="Happy ever after")
        story2.save()
        story2.tags.add(tag2, tag3)
        story3 = Story.objects.create(id=3, title="My third story", storytext="Three brown mice")
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

        url = url + '?'
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

        # Check query strings which should return an empty JSON response
        url = '/rest-api/stories/'
        for item in query_strings_valid_empty:
            current_url = url + item
            json_response = self.client.get(current_url)
            self.assertIsNotNone(json_response)
            empty = False
            if len(json_response.content) == 0:
                empty = True
            self.assertTrue(empty)

        # Check invalid query strings

        json_response = self.client.get('rest-api/stories/tag_id=2')  # Missing the '?' from start of querystring
        self.assertEqual(json_response.status_code, 404)

        with self.assertRaises(ValueError):
            self.client.get('/rest-api/stories/?tag_id=1title_text=hello') # Missing the '&' between parameters

        json_response = self.client.get('rest-api/stories/uesr_id=1') # Parameter name is misspelled
        self.assertEqual(json_response.status_code, 404)

    def test_response_contains_correct_headings(self):
        """
        Check that stories sent in the response contain headings such as id, title, dateposted, etc
        """

        # Check that Story model fields are included in the response
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
        url = url + '?'
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

        for story in json_response.data:
            story_dates.append(story['dateposted'])

        # Need to finish


"""
class GeneralTests(TestCase):

    def setUp(self):
        tag1 = Tag.objects.create(id=1, name="short")
        tag1.save()
        tag2 = Tag.objects.create(id=2, name="long")
        tag2.save()
        tag3 = Tag.objects.create(id=3, name="romantic")
        tag3.save()
        story1 = Story.objects.create(id=1, title="My first story", storytext="Once upon a time")
        story1.save()
        story1.tags.add(tag1, tag3)
        story2 = Story.objects.create(id=2, title="My second story", storytext="Happy ever after")
        story2.save()
        story2.tags.add(tag2, tag3)
        story3 = Story.objects.create(id=3, title="My third story", storytext="Three brown mice")
        story3.save()
        story3.tags.add(tag2)
        user1 = User.objects.create(id=1, name="anon")
        user1.save()

    def test_header_on_every_page(self):

        discover = self.client.get('/')
        contact = self.client.get('/contact/')
        about = self.client.get('/about/')
        test_pages = [discover, contact, about]
        fails = 0
        for page in test_pages:
            if 'header_top' not in page.content:
                fails += 1
        self.assertEqual(fails, 0)

class DiscoverTests(TestCase):

    def setUp(self):
        tag1 = Tag.objects.create(id=1, name="short")
        tag1.save()
        tag2 = Tag.objects.create(id=2, name="long")
        tag2.save()
        tag3 = Tag.objects.create(id=3, name="romantic")
        tag3.save()
        story1 = Story.objects.create(id=1, title="My first story", storytext="Once upon a time", dateposted="2000-01-01")
        story1.save()
        story1.tags.add(tag1, tag3)
        story2 = Story.objects.create(id=2, title="My second story", storytext="Happy ever after", dateposted="2005-10-13")
        story2.save()
        story2.tags.add(tag2, tag3)
        story3 = Story.objects.create(id=3, title="My third story", storytext="Three brown mice", dateposted="1992-05-31")
        story3.save()
        story3.tags.add(tag2)
        user1 = User.objects.create(id=1, name="anon")
        user1.save()

    def test_order_stories(self):

        response = self.client.get('/0/getTaggedStories/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        stories = json.loads(response.content, object_pairs_hook=collections.OrderedDict)
        fails = 0
        prev_date = ""
        for story in stories:
                if prev_date != "":
                    current_date = stories[story]['dateposted']
                    if prev_date < current_date:
                        fails+= 1
                prev_date = stories[story]['dateposted']
        self.assertEqual(fails, 0)

    def test_tag_filter_chooses_correct_stories(self):


        no_stories_message = "There are no stories with that tag."
        fails = 0
        all_tags = Tag.objects.all()
        for tag in all_tags:
            response = self.client.get('/' + unicode(tag.id) + '/getTaggedStories/',
                                       HTTP_X_REQUESTED_WITH='XMLHttpRequest')
            stories_with_tag = Story.objects.filter(tags__id=tag.id)
            if len(stories_with_tag) > 0:
                for story in stories_with_tag:
                    if story.title not in response.content:
                        fails += 1
            elif len(stories_with_tag) == 0:
                if no_stories_message not in response:
                    fails += 1
            else:
                fails += 1
        response = self.client.get(
            '/' + unicode(0) + '/getTaggedStories/',
            HTTP_X_REQUESTED_WITH='XMLHttpRequest')  # Filter with value 0 should result in all stories
        all_stories = Story.objects.all()
        if len(all_stories) > 0:
            for story in all_stories:
                if story.title not in response.content:
                    fails += 1
        elif len(all_stories) == 0:
            if no_stories_message not in response:
                fails += 1
        else:
            fails += 1

        self.assertEqual(fails, 0)

"""