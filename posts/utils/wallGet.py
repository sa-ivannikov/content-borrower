import requests
from datetime import datetime
import psycopg2
from decouple import config
from django.conf import settings


# Move to file, where functions will be called 



def processResponse(responseObj):
    """Takes a response and processes it for further storage in DB.\n
    Filters out posts that are not from yesterday"""
    # Make list from responseObject
    responseList = responseObj.json().get('response').get('items')
    formattedList = []
    
    for item in responseList:
        # If post is not from yesterday - go to next item.
        # This is the only way to get unique posts every day wtih this api
        if datetime.today().day - datetime.fromtimestamp(item.get('date')).day != 1:
            continue
        attachments = item.get('attachments')
        # If no attachments - go next, we dont need this post
        if not attachments:
            continue

        # Create string which contains links to all photos of post
        stringOfLinks = []
        for attachment in attachments:
            # Only write photo attachments
            if attachment.get('type') != 'photo':
                continue
            
            bestPhotoSize = ''
            listOfSizes = attachment.get('photo').get('sizes')
            for size in listOfSizes:
                # Eacho photo has diffrent sizes. The one with type z has initial photo resolution
                if size['type'] > bestPhotoSize:
                    bestPhoto = size['url']
                    bestPhotoSize = size['type']
            
            stringOfLinks.append(bestPhoto)
            
            
        if len(stringOfLinks) > 0:
            newItem = dict(date = datetime.fromtimestamp(item.get('date')), commentsAmount = item.get('comments').get('count'), likesAmount = item.get('likes').get('count'), repostsAmount = item.get('reposts').get('count'), imgLinks = stringOfLinks)
            formattedList.append(newItem)
        """ if newItem['imgLinks'] != '':
            formattedList.append(newItem) """
    return formattedList
        

def getPosts(groupDomain, postsAmount = 100):
    """
    Get {postAmount} of posts from groupd with domain {groupDomain}.\n
    Method wants either app service token or user token.\n
    Returns list of posts with date, number of likes, text, and a link to the best resolution picture
    """
    serviceToken = settings.APP_SERVICE_TOKEN
    reqUrl = 'https://api.vk.com/method/wall.get?domain={0}&count={1}&offset=1&access_token={2}&v=5.122'.format(groupDomain, postsAmount, serviceToken)

    listOfPosts = processResponse(requests.get(reqUrl))

    return listOfPosts


def storePosts(postsList, donorGroup, sourceGroup, sourceSubsAmount):
    conn = psycopg2.connect(dbname = settings.DB_NAME, user = settings.DB_USER, password = settings.DB_PASSWORD, host = settings.DB_HOST)
    
    cursor = conn.cursor()
    
    for post in postsList:
        
        cursor.execute("""INSERT INTO public.post
                        (posted_at, likes_count, reposts_count, comments_count, img_links, for_recipient_id, from_donor, subs_amount, posted)
                        VALUES
                       (%s, %s, %s, %s, %s, %s, %s, %s, %s);""", (post['date'], post['likesAmount'], post['repostsAmount'], post['commentsAmount'], post['imgLinks'], donorGroup, sourceGroup, sourceSubsAmount, False))


    conn.commit()
    
    cursor.close()

    conn.close()