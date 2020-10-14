# Content borrower app
Configure donors (groups to borrow posts), recipients (groups to post content to). App takes posts from yesterday daily, stores them to DB, and reposts best selection to recipient with configured schedule. 


## Used technologies
- Django, Django ORM
- PostgeSQL
- Celery for asyncronous tasks
- Celery beat for scheduled tasks
