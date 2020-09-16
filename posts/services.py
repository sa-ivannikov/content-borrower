import os
from datetime import datetime
import requests


from django.conf import settings

from .models import Recipient, Post
import logging

logger = logging.getLogger(__name__)

def store_posts():
    """ Writes all posts from all
    recipients to DB
     """
    logger.error('test')
    recipients = Recipient.objects.all()
    for recipient in recipients:
        recipient.write_all()

def download_post_photo(image_url):
    # OK
    """ Takes image_url and downloads it
    to project folder. Returns file name. """
    filename = image_url.rsplit('/', 1)[1]
    res = requests.get(image_url, allow_redirects = True)
    open(filename, 'wb').write(res.content)
    return filename

def get_upload_server(group_id, token):
    """ Takes group ID, user token of the Recipient,
    and returns Upload URL as a string,
    which is required for upload_to_server """
    upload_server_url = 'https://api.vk.com/method/photos.getWallUploadServer'
    upload_server_payload = {
        'group_id': group_id,
        'access_token': token,
        'v':'5.122',
    }
    upload_server = requests.get(upload_server_url, params=upload_server_payload)
    return upload_server.json().get('response').get('upload_url')

def upload_to_server(filename, upload_url):
    """ Takes file name of the photo and upload server.
    Photo must be stored in the project folder.
    Uploads photo to server.
    Returns VK API response, where photo
    object is used from further saving.
    Also removes file from project folder """
    file_dict = {'photo': open(filename, 'rb')}
    res = requests.post(upload_url, files=file_dict)
    os.remove(filename)
    return res

def save_to_wall(upload_response, group_id, token):
    """ Takes response from uploading file,
    group ID and token.
    Saves photo to group wall,
    returns jsoned response from VK API """
    api_url = 'https://api.vk.com/method/photos.saveWallPhoto'
    payload = {
        'group_id':group_id,
        'photo': upload_response.json().get('photo'),
        'server': upload_response.json().get('server'),
        'hash': upload_response.json().get('hash'),
        'access_token': token,
        'v':'5.122',
    }
    res = requests.get(api_url, params=payload)
    return res.json()

def post_to_group(post, group_id, token):
    """ Takes post, group_id and token.
    Posts post's img to group with given id.
    Auth with token """
    # Take only 0th element, because img_links currently is a list of links. Would fix later
    filename = download_post_photo(post.img_links[0])
    upload_url = get_upload_server(group_id, token)
    upload_response = upload_to_server(filename, upload_url)
    save_response = save_to_wall(upload_response, group_id, token)
    # VK API expects negative ID when posting to a group
    group_id = '-' + group_id
    attachment = 'photo' + str(save_response.get('response')[0].get('owner_id')) + '_' \
        + str(save_response.get('response')[0].get('id'))
    url = 'https://api.vk.com/method/wall.post'
    payload = {
        'owner_id':group_id,
        'access_token':token,
        'v':'5.122',
        'friends_only':'0',
        'from_group':'1',
        'attachments':attachment,
        }
    result = requests.get(url, params=payload)
    return result

def tg_get_request(token, method_name, payload={}):
    """ Makes get request to Telegram API.
     """
    url = 'https://api.telegram.org/bot{0}/{1}'.format(token, method_name)
    res = requests.get(url, params=payload)
    return res

def tg_send_photo(token, chat_id, photo_url):
    """ Sends photo to given chat
     """
    payload = {
        'chat_id': chat_id,
        'photo': photo_url,
    }
    res = tg_get_request(token, 'sendPhoto', payload=payload)
    return res

def repost_for_recipient(recipient):
    """ For given recipient, repost best
    post to VK and Tg(if tg info specified) """
    posts = recipient.make_posts_list()
    if posts:
        best_post = posts[0]
        post_to_group(best_post, recipient.target_group_id, recipient.group_key).json()
        if recipient.tg_channel and recipient.tg_token:
            res = tg_send_photo(recipient.tg_token, recipient.tg_channel, best_post.img_links[0])
        best_post.posted = True
        best_post.save()
     
def delete_recipients_post(rec_id):
    """ Delete all posts of
    recipient with given ID """
    Post.objects.filter(for_recipient=rec_id).delete()

def repost_top_post():
    """ For all recipients in DB,
    post one best photo to tagret group.
    Edit post to be no longer
    available for make_post_list """
    recipients = Recipient.objects.all()
    for recipient in recipients:
        repost_for_recipient(recipient)
