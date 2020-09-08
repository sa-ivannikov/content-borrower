from django.db import models
from .utils import store_from_vk
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import datetime
from django.utils import timezone
from django_cryptography.fields import encrypt


# Create your models here.


class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.TextField()
    group_id = models.TextField(blank=True, null=True)
    group_domain = models.TextField(blank=True, null=True)
    vk_link = models.URLField(null=True, blank=True)
    subs_amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.group_name

    def get_and_write_posts(self, recipient):
        """ Gets and writes all posts
        from this donor to DB """
        posts = store_from_vk.get_posts(self.group_domain)
        store_from_vk.store_posts(posts, recipient, self.group_name, self.subs_amount)

class Recipient(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.TextField()
    target_group_name = models.TextField()
    target_group_id = models.CharField(max_length=30)
    target_group_link = models.TextField()
    donors = models.ManyToManyField(Donor)
    group_key = encrypt(models.CharField(max_length=200))
    tg_channel = models.CharField(max_length=40, blank=True, null=True)
    tg_token = encrypt(models.CharField(max_length=150, blank=True, null=True))

    def __str__(self):
        return self.name

    def write_all(self):
        """ Writes all post of
        this recipient to DB """
        donors = self.donors.filter()
        for donor in donors:
            donor.get_and_write_posts(self.id)

    def make_posts_list(self):
        """ Retrieves list of posts from DB.
        Orders by post_quality.
        Best post at the top
         """
        # Get posts only from yesterday. Modify days=x to change amount of days
        post_list = Post.objects.filter(posted=False, for_recipient=self.id, \
            posted_at__date=(datetime.datetime.now()-datetime.timedelta(days=1)).date())
        # sort by post_quality, take best half of posts
        post_list = sorted(post_list, key=lambda x: x.post_quality, \
            reverse=True)[:len(post_list) // 2]
        return post_list

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    posted_at = models.DateTimeField()
    likes_count = models.IntegerField(blank=True, null=True)
    reposts_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    img_links = ArrayField(ArrayField(models.URLField(blank=True, null=True)))
    for_recipient = models.ForeignKey(Recipient, on_delete = models.CASCADE)
    from_donor = models.TextField(blank=True, null=True)
    subs_amount = models.IntegerField(null=True, blank=True)
    posted = models.BooleanField(default=False)

    class Meta:
        db_table = 'post'

    def __str__(self):
        return '{0} post with ID {1}'.format(self.for_recipient, self.id)

    @property
    def post_quality(self):
        """ Measures post by qualiry,
        using likes, reposts and comments
        amount """
        return (self.likes_count + self.reposts_count * 2 + self.comments_count * 2)\
            / self.subs_amount
    