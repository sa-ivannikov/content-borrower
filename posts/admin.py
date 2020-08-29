from django.contrib import admin

# Register your models here.
from .models import Post, Donor, Recipient

class PostAdmin(admin.ModelAdmin):
    fields = ['posted_at', 'likes_count', 'reposts_count', 'comments_count', 'img_links', 'donors_group']

class DonorAdmin(admin.ModelAdmin):
    fields = ['group_name', 'group_id', 'group_domain', 'vk_link']
    
class RecipientAdmin(admin.ModelAdmin):
    fields = ['name', 'target_group_name', 'target_group_link', 'donors']


admin.site.register(Post, PostAdmin)
admin.site.register(Donor, DonorAdmin)
admin.site.register(Recipient, RecipientAdmin)