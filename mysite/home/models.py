from django.db import models
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import messages
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.models import Page
import blog.models


class HomePage(Page):

    hero_headline = models.CharField(blank=True, max_length=256)
    hero_text = models.CharField(blank=True, max_length=256)
    hero_button = models.CharField(blank=True, max_length=32)

    insurance_title = models.CharField(blank=True, max_length=256)
    insurance_description = models.CharField(blank=True, max_length=256)
    auto_description = models.CharField(blank=True, max_length=256)
    home_description = models.CharField(blank=True, max_length=256)
    life_description = models.CharField(blank=True, max_length=256)
    buisness_description = models.CharField(blank=True, max_length=256)

    blog_title = models.CharField(blank=True, max_length=128)
    blog_description = models.CharField(blank=True, max_length=256)
    blog_button = models.CharField(blank=True, max_length=32)

    video_title = models.CharField(blank=True, max_length=128)
    video_description =  models.CharField(blank=True, max_length=256)
    video_link = models.CharField(blank=True, max_length=256)

    testimonial_quote_1 = models.CharField(blank=True, max_length=256)
    testimonial_name_1 = models.CharField(blank=True, max_length=64)
    testimonial_description_1 = models.CharField(blank=True, max_length=128)
    testimonial_quote_2 = models.CharField(blank=True, max_length=256)
    testimonial_name_2 = models.CharField(blank=True, max_length=64)
    testimonial_description_2 = models.CharField(blank=True, max_length=128)
    testimonial_quote_3 = models.CharField(blank=True, max_length=256)
    testimonial_name_3 = models.CharField(blank=True, max_length=64)
    testimonial_description_3 = models.CharField(blank=True, max_length=128)

    call_to_action_headline = models.CharField(blank=True, max_length=256)
    call_to_action_text = models.CharField(blank=True, max_length=256)
    call_to_action_button = models.CharField(blank=True, max_length=32)

    facebook_link = models.CharField(blank=True, max_length=256)
    twitter_link = models.CharField(blank=True, max_length=256)
    linkedin_link = models.CharField(blank=True, max_length=256)
    email_link = models.CharField(blank=True, max_length=256)
    instagram_link = models.CharField(blank=True, max_length=256)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel('hero_headline'),
                FieldPanel('hero_text'),
                FieldPanel('hero_button'),
            ],
            heading="Hero Fields",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('insurance_title'),
                FieldPanel('insurance_description'),
                FieldPanel('auto_description'),
                FieldPanel('home_description'),
                FieldPanel('life_description'),
                FieldPanel('buisness_description'),
            ],
            heading="Insurance Fields",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('blog_title'),
                FieldPanel('blog_description'),
            ],
            heading="Blog Fields",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('video_title'),
                FieldPanel('video_description'),
                FieldPanel('video_link'),
            ],
            heading="Video Fields",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('testimonial_quote_1'),
                FieldPanel('testimonial_name_1'),
                FieldPanel('testimonial_description_1'),
                FieldPanel('testimonial_quote_2'),
                FieldPanel('testimonial_name_2'),
                FieldPanel('testimonial_description_2'),
                FieldPanel('testimonial_quote_3'),
                FieldPanel('testimonial_name_3'),
                FieldPanel('testimonial_description_3'),
            ],
            heading="Testimonial Fields",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('call_to_action_headline'),
                FieldPanel('call_to_action_text'),
                FieldPanel('call_to_action_button'),
            ],
            heading="Call to Action Fields",
            classname="collapsible collapsed"
        ),
        MultiFieldPanel(
            [
                FieldPanel('facebook_link'),
                FieldPanel('twitter_link'),
                FieldPanel('linkedin_link'),
                FieldPanel('email_link'),
                FieldPanel('instagram_link'),
            ],
            heading="Link Fields",
            classname="collapsible collapsed"
        ), 
    ]

    def serve(self, request):
        # if this is a POST request we need to process the form data
        if request.method == 'POST':
            form = ''
            if 'contact_submit' in request.POST:
                form = blog.models.ContactForm1(request.POST)
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
            contactform = blog.models.ContactForm1()
            chosen_posts = blog.models.BlogPage.objects.filter(chosen=True)
            return render(request, 
                'home/home_page.html', 
                {
                    'page': self,
                    'contactform': contactform,
                    'chosen_posts': chosen_posts,
                    'facebook_link': self.facebook_link,
                    'twitter_link': self.twitter_link,
                    'linkedin_link': self.linkedin_link,
                    'email_link': self.email_link,
                    'instagram_link': self.instagram_link,
                }
            )