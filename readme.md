# Content borrower app
Configure donors (groups to borrow posts), recipients (ggroups to post content to). App takes posts from yesterday daily, stores them to DB, and reposts best selection to recipient with configured schedule. 


## Used technologies
- Django
- PostgeSQL, hosted on elephantsql
- Django ORM
- Psycopg for SQL queries
- Celery for asyncronous tasks
- Celery beat for scheduled tasks
- Redis as message broker and cache setup (caching views not implemented yet)
- django_cryptography for VK API keys DB storage
- Docker-compose for local development


## To do
- [x] Create a logic to pick best pics from a given selection
- [x] Create scheduled task to get and store posts for all recipients
- [x] Add posting to a group logic to scheduled task 
- [ ] Learn Telegram API and create a bot to post imgs to a channel - 11.09
- [ ] Update number of subs in all donors - 12.09
- [ ] Create dashboard view with stats and "Repost right now" button - 12.09
- [ ] Write tests 13.09
- [ ] Refactor and document code - 14.09
