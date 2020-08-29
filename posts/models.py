from django.db import models
from .utils import wallGet
from django.conf import settings
from django.contrib.postgres.fields import ArrayField

# Create your models here.


class Donor(models.Model):
    id = models.AutoField(primary_key=True)
    group_name = models.TextField()
    group_id = models.TextField(blank=True, null=True)
    group_domain = models.TextField(blank=True, null=True)
    vk_link = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.group_name
    
    def showYesterdayPosts(self):
        print(wallGet.getPosts(self.group_domain))
        
    def getAndWritePosts(self, recipient):
        posts = wallGet.getPosts(self.group_domain)
        wallGet.storePosts(posts, recipient)

    
class Recipient(models.Model):
    id = models.AutoField(primary_key=True)
    name =  models.TextField()
    target_group_name = models.TextField()
    target_group_link = models.TextField()
    donors = models.ManyToManyField(Donor)
    
    def __str__(self):
        return self.name
    
    def writeAll(self):
        # Problem is that self is not queryset object - it does not have .all
        donors = self.donors.filter()
        for donor in donors:
            donor.getAndWritePosts(self.id)
            
    
    
class Post(models.Model):
    id = models.AutoField(primary_key=True)
    posted_at = models.DateTimeField()
    likes_count = models.IntegerField(blank=True, null=True)
    reposts_count = models.IntegerField(blank=True, null=True)
    comments_count = models.IntegerField(blank=True, null=True)
    img_links = ArrayField(ArrayField(models.URLField(blank=True, null=True)))
    for_recipient = models.ForeignKey(Recipient, on_delete = models.CASCADE)
    

    class Meta:
        db_table = 'post'
        #managed = False
        
    def __str__(self):
        return '{0} post with ID {1}'.format(self.for_recipient, self.id)