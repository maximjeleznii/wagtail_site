from django.db import models
from django.shortcuts import render, HttpResponseRedirect

# Create your models here.
from wagtail.core.models import Page
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel
)
from django.forms import ModelForm
from django import forms
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from blog.forms import DeleteCommentForm, ToggleCommentForm
from django.contrib import messages
import home.models

class ContactInfo(models.Model):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    message = models.TextField(max_length=250, blank=True)

    def __str__(self):
        return self.email

class ContactForm1(ModelForm):
    class Meta:
        model = ContactInfo
        fields = ['first_name', 'last_name', 'email', 'message']
        widgets = {
          'message': forms.Textarea(attrs={'rows':4}),
        }

class ContactResponsePage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body', classname="full")
    ]

class BlogIndexPage(Page):
    hero_headline = models.CharField(blank=True, max_length=256)
    hero_text = models.CharField(blank=True, max_length=256)
    hero_button = models.CharField(blank=True, max_length=32)

    content_panels = Page.content_panels + [
        FieldPanel('hero_headline'),
        FieldPanel('hero_text'),
        FieldPanel('hero_button'),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = ['blog.BlogPage']

    def serve(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            form = ''
            if 'contact_submit' in request.POST:
                form = ContactForm1(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Contact form submission succesfull.')
                    return HttpResponseRedirect(self.get_url())
                else:
                    if not form.validate_unique():
                        messages.error(request, 'Email not unique.')
                    else:
                        messages.error(request, 'Unknown error.')
                    return HttpResponseRedirect(self.get_url())
        # if a GET (or any other method) we'll create a blank form
        else:
            contactform = ContactForm1()
            link = home.models.HomePage.objects.all().first()
            return render(request, 
                'blog/blog_index_page.html', 
                {
                    'page': self,
                    'contactform': contactform,
                    'facebook_link': link.facebook_link,
                    'twitter_link': link.twitter_link,
                    'linkedin_link': link.linkedin_link,
                    'email_link': link.email_link,
                    'instagram_link': link.instagram_link,
                }
            )

class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    comment_toggle = models.BooleanField(default=True)
    chosen = models.BooleanField(default=False)
    feed_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        ImageChooserPanel('feed_image'),
        FieldPanel('intro'),
        FieldPanel('body', classname="full"),
        FieldPanel('comment_toggle'),
        FieldPanel('chosen'),
    ]

    parent_page_types = ['blog.BlogIndexPage']
    subpage_types = []

    def serve(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            form = ''
            if 'contact_submit' in request.POST:
                form = ContactForm1(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Contact form submission succesfull.')
                    return HttpResponseRedirect(self.get_url())
                else:
                    if not form.validate_unique():
                        messages.error(request, 'Email not unique.')
                    else:
                        messages.error(request, 'Unknown error.')
                    return HttpResponseRedirect(self.get_url())
            if 'comment_submit' in request.POST:
                form = CommentForm(request.POST)
                if form.is_valid():
                    comment = form.save(commit=False)
                    comment.page = self
                    comment.save()
                    return HttpResponseRedirect(self.get_url())
            if 'comment_delete' in request.POST:
                if request.user.is_authenticated:
                    form = DeleteCommentForm(request.POST)
                    if form.is_valid():
                        comment = CommentModel.objects.get(id=form.cleaned_data['comment_id'])
                        comment.delete()
                        messages.success(request, 'Comment successfully deleted.')
                        return HttpResponseRedirect(self.get_url()+'#comments')
                    else:
                        messages.error(request, 'Failed to delete comment.')
                        return HttpResponseRedirect(self.get_url()+'#comments')
                else:
                    return HttpResponseRedirect('../../../admin')
            if 'comment_toggle' in request.POST:
                if request.user.is_authenticated:
                    form = ToggleCommentForm(request.POST)
                    if form.is_valid():
                        self.comment_toggle = not self.comment_toggle
                        self.save()
                        messages.success(request, 'Comments successfully toggled.')
                        return HttpResponseRedirect(self.get_url()+'#comments')
                    else:
                        messages.error(request, 'Failed to toggle comments.')
                        return HttpResponseRedirect(self.get_url()+'#comments')
                else:
                    return HttpResponseRedirect('../../../admin')

        # if a GET (or any other method) we'll create a blank form
        else:
            comments = CommentModel.objects.filter(page=self).order_by('pk')
            commNum = comments.count()
            paginator = Paginator(comments, 5)
            pageNumber = request.GET.get('page')
            if not pageNumber is None:
                pageNumber = int(pageNumber)
            try: 
                paginatedPage = paginator.page(pageNumber)
            except PageNotAnInteger: 
                pageNumber = 1
            except EmptyPage: 
                pageNumber = paginator.num_pages
            comments = paginator.page(pageNumber)

            contactform = ContactForm1()
            commentform = CommentForm()
            delcommentform = DeleteCommentForm()
            togglecommentform = ToggleCommentForm()
            prevPage = self.get_url()+'?page='+str(pageNumber-1)+'#comments'
            nextPage = self.get_url()+'?page='+str(pageNumber+1)+'#comments'
            maxPage = pageNumber >= paginator.num_pages
            minPage = pageNumber <= 1

            link = home.models.HomePage.objects.all().first()
            return render(request, 
                'blog/blog_page.html', 
                {
                    'page': self, 
                    'delcommentform' : delcommentform,
                    'togglecommentform' : togglecommentform,
                    'contactform': contactform, 
                    'commentform': commentform, 
                    'commNum' : commNum,
                    'comments': comments,
                    'prevpage': prevPage,
                    'nextpage': nextPage,
                    'maxPage': maxPage,
                    'minPage': minPage,
                    'facebook_link': link.facebook_link,
                    'twitter_link': link.twitter_link,
                    'linkedin_link': link.linkedin_link,
                    'email_link': link.email_link,
                    'instagram_link': link.instagram_link,
                }
            )

class CommentModel(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField(max_length=250)
    page = models.ForeignKey(BlogPage, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class CommentForm(ModelForm):
    class Meta:
        model = CommentModel
        fields = ['name', 'email', 'comment']