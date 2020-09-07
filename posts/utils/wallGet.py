import requests
from datetime import datetime
import psycopg2
from decouple import config
from django.conf import settings


def process_response(response_obj):
    """Takes a response and processes it for further storage in DB.
    Filters out posts that are not from yesterday"""
    # Make list from responseObject
    response_list = response_obj.json().get('response').get('items')
    formatted_list = []
    for item in response_list:
        # If post is not from yesterday - go to next item.
        # This is the only way to get unique posts every day wtih this api
        if datetime.today().day - datetime.fromtimestamp(item.get('date')).day != 1:
            continue
        attachments = item.get('attachments')
        # If no attachments - go next, we dont need this post
        if not attachments:
            continue

        # Create string which contains links to all photos of post
        string_of_links = []
        for attachment in attachments:
            # Only write photo attachments
            if attachment.get('type') != 'photo':
                continue
            best_photo_size = ''
            list_of_sizes = attachment.get('photo').get('sizes')
            
            for size in list_of_sizes:
                # Eacho photo has diffrent sizes. The one with type z has initial photo resolution
                if size['type'] > best_photo_size:
                    best_photo = size['url']
                    best_photo_size = size['type']
            string_of_links.append(best_photo)  
            
        if len(string_of_links) > 0:
            new_item = dict(date = datetime.fromtimestamp(item.get('date')), comments_amount = item.get('comments').get('count'), likes_amount = item.get('likes').get('count'), reposts_amount = item.get('reposts').get('count'), img_links = string_of_links)
            formatted_list.append(new_item)
    return formatted_list
        

def get_posts(group_domain, posts_amount = 100):
    """
    Get posts_amount of posts from groupd with domain group_domain.
    Method wants either app service token or user token.
    Returns list of posts with date, number of likes,
    text, and a link to the best resolution picture
    """
    service_token = settings.APP_SERVICE_TOKEN
    req_url = 'https://api.vk.com/method/wall.get'
    payload = {
        'domain': group_domain,
        'count': posts_amount,
        'offset': 1,
        'access_token': service_token,
        'v': '5.122'
        }
    list_of_posts = process_response(requests.get(req_url, params=payload))
    return list_of_posts


def store_posts(posts_list, donor_group, source_group, source_subs_amount):
    """ Takes posts list, donor and source group,
    subs amount and stores all posts in DB """
    conn = psycopg2.connect(dbname = settings.DB_NAME, user = settings.DB_USER,
                            password = settings.DB_PASSWORD, host = settings.DB_HOST)
    cursor = conn.cursor()
    for post in posts_list:
        cursor.execute(
            """INSERT INTO public.post
                        (posted_at,
                        likes_count,
                        reposts_count,
                        comments_count,
                        img_links,
                        for_recipient_id,
                        from_donor,
                        subs_amount,
                        posted)
                        VALUES
                       (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
                       (post['date'],
                        post['likes_amount'],
                        post['reposts_amount'],
                        post['comments_amount'],
                        post['img_links'],
                        donor_group,
                        source_group,
                        source_subs_amount,
                        False))
    conn.commit()
    cursor.close()
    conn.close()
    