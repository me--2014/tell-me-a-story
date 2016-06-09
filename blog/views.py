# Test comment

from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from blog.models import Story, Tag, User
from django.core.urlresolvers import reverse
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'blog/index.html'
    model = Story

    def get_context_data(self):
        max_number_stories = 5
        stories_list = Story.objects.order_by('-dateposted')
        newest = stories_list[0]
        tag_list = Tag.objects.all()
        context = {
            'stories_list': stories_list,
            'tag_list': tag_list,
            'page_title': 'Tell Me a Story',
            'max': max_number_stories,
            'newest_story': newest,
        }
        return context



class DetailView(generic.DetailView):
    template_name = 'blog/detail.html'
    model = Story

    def get_object(self, queryset=None):
        object = super(DetailView, self).get_object()
        story_fulltext = object.storytext
        paras = story_fulltext.split('\n')
        for item in paras:
            if item == '\r':
                paras.remove('\r')
        object.storytext = paras
        return object

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data()
        context['tag_list'] = Tag.objects.all()
        context['story_list'] = Story.objects.all()
        return context

def filter(request):
    if request.POST['tagchoice'] == '0':
        return HttpResponseRedirect(reverse('blog:results', args=(0,)))
    else:
        try:
            tag = Tag.objects.get(pk=request.POST['tagchoice'])
        except(KeyError, Tag.DoesNotExist):
            return render(request, 'blog/index.html', {
                'error_message': "You did not choose a valid tag"
            })
        else:
            return HttpResponseRedirect(reverse('blog:results', args=(tag.id,)))

def results(request, tag_id):
    if tag_id == '0':
        tagname = 'All'
        storyqueryset = Story.objects.all()
    else:
        tagname = get_object_or_404(Tag, pk=tag_id).name
        storyqueryset = Story.objects.filter(tags__id=tag_id)
    context = {
        'tagname': tagname,
        'story_list': storyqueryset,
        'tag_list': Tag.objects.all(),
    }
    return render(request, 'blog/results.html', context)

class ContactView(generic.TemplateView):
    template_name = 'blog/contact.html'

    def get_context_data(self):
        context = super(ContactView, self).get_context_data()
        context['tag_list'] = Tag.objects.all()
        context['story_list'] = Story.objects.all()
        context['page_title'] = 'Contact Us'
        return context

class AboutView(generic.TemplateView):
    template_name = 'blog/about.html'

    def get_context_data(self):
        context = super(AboutView, self).get_context_data()
        context['tag_list'] = Tag.objects.all()
        context['story_list'] = Story.objects.all()
        context['page_title'] = 'About'
        return context

def taggedStories(request, tag_id):

    if tag_id == '0':
        storyqueryset = Story.objects.all().values().order_by('-dateposted')
    else:
        storyqueryset = Story.objects.filter(tags__id=tag_id).values().order_by('-dateposted')

    # Identify user favourites
    userId = 1 # For now, we only have one user
    current_user = User.objects.get(id=userId)
    userfavsqueryset = current_user.favourite_set.all()
    userfavslist = []
    for item in userfavsqueryset:
        userfavslist.append(item.story.id)
    for story in storyqueryset:
        if story['id'] in userfavslist:
            story['is_fav'] = True
        else:
            story['is_fav'] = False

    # Split storytext into paragraphs
    for story in storyqueryset:
        story_fulltext = story['storytext']
        paras = story_fulltext.split('\n')
        for item in paras:
            if item == '\r':
                paras.remove('\r')
        story['storytext'] = paras

    stories_dict = {}
    counter = 0
    for story in storyqueryset:
        stories_dict[counter] = story
        counter+= 1
    response = JsonResponse(stories_dict)
    return response


def getMostRecent(request):
    mostRecentStory = Story.objects.values().order_by('-dateposted')[0]

    # Split storytext into paragraphs
    story_fulltext = mostRecentStory['storytext']
    paras = story_fulltext.split('\n')
    for item in paras:
        if item == '\r':
            paras.remove('\r')
    mostRecentStory['storytext'] = paras

    mostRecentStoryDict = {}
    mostRecentStoryDict[0] = mostRecentStory
    response = JsonResponse(mostRecentStoryDict)
    return response

def getTags(request):
    tag_list = Tag.objects.all().values().order_by('name')
    tag_list_dict = {}
    counter = 0
    for tag in tag_list:
        tag_list_dict[counter] = tag
        counter += 1
    response = JsonResponse(tag_list_dict)
    return response

def toggleFav(request):

    response = JsonResponse({'success': 'true'})
    return response
