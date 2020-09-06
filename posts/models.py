from django.db import models
from .utils import wallGet
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import datetime
from django.utils import timezone

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
    
    def showYesterdayPosts(self):
        print(wallGet.getPosts(self.group_domain))
        
    def getAndWritePosts(self, recipient):
        posts = wallGet.getPosts(self.group_domain)
        wallGet.storePosts(posts, recipient, self.group_name, self.subs_amount)

    
class Recipient(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.TextField()
    target_group_name = models.TextField()
    target_group_link = models.TextField()
    donors = models.ManyToManyField(Donor)
    
    def __str__(self):
        return self.name
    
    def writeAll(self):
        donors = self.donors.filter()
        for donor in donors:
            donor.getAndWritePosts(self.id)

    def makePostsList(self):
        # Part of post selection logic is here
        
        # Get posts only from yesterday. Modify days=x to change amount of days
        postList = Post.objects.filter(posted=False, for_recipient=self.id, posted_at__date=(timezone.now()-timezone.timedelta(days=1)).date())
        
        # sort by post_quality, take best half of posts
        postList = sorted(postList, key=lambda x: x.post_quality, reverse=True)[:len(postList) // 2]
        return postList
            
    
    
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
        #managed = False
        
    def __str__(self):
        return '{0} post with ID {1}'.format(self.for_recipient, self.id)
    
    @property
    def post_quality(self):
        return (self.likes_count + self.reposts_count * 2 + self.comments_count * 2) / self.subs_amount
    