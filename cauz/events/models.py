from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category,self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('category-detail', kwargs={'slug': self.slug})
class Region(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Region,self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('region-detail', kwargs={'slug': self.slug})

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField()
    slug = models.SlugField(unique=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    region = models.ForeignKey(Region, null=True, blank=True, on_delete=models.CASCADE)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_events'
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'slug': self.slug})

class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    # supporter = models.CharField(max_length=200)
    event = models.ForeignKey(Event, null=True, blank=True, on_delete=models.CASCADE, related_name='event_pledge')
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_DEFAULT,
        related_name='supporter_pledges',
        null=True,
        default=None
    )
