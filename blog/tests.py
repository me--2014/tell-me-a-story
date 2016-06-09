"""
Test suite for blog application. To run use command 'python manage.py test blog'.
Note: SimpleTestCase contains useful additional assert methods.
"""

from django.test import TestCase
from .models import Tag, Story, User
from datetime import date
import json, collections


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
        """
        Check every page on the blog includes the stories filter widget
        """
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
        """
        Check that stories are displayed by date with most recent first
        """
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

        """
            Check that, if user filters stories by tag x, all stories with tag x are included in results.
            @TODO: Could refactor using self.assertContains()
        """
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

