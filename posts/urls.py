from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('repost/<int:rec_id>', views.repost, name = 'repost'),
    path('store/<int:rec_id>', views.store, name = 'store'),
    path('delete_posts/<int:rec_id>', views.delete_posts, name = 'delete_posts')
]
