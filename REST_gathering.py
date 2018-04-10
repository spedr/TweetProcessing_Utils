import tweepy
from tweepy import OAuthHandler
import json
import logging
import time

#config = json.load(open('config.json'))
auth = tweepy.OAuthHandler('xUHcAIMR9jCxbSPwvyFzQDnml', 'atON1KQzZv8rGI8Rq0yoFmlILFcGY2E8pPsYwAW3hjyIadcxMB')
auth.set_access_token('136105601-g0I1GjFRQXOsZ6x3bFXu1jmER9RYgJXONwWxCa2d', '1TwojInNGl7nL7Mx3lx82cBl3quNivLY7w6Mwue1BIPE8')


api = tweepy.API(auth)


queue = open('teste.json','w')

queue.write('[')

current_tweet = {}

def json_format(data_json):
#    current_tweet['id'] = data_json.id
    current_tweet['created_at'] = data_json.created_at.strftime('%Y-%m-%dT%H:%M:%SZ')
    current_tweet['userid'] = data_json.user.id
    current_tweet['username'] = data_json.user.name
    current_tweet['screen_name'] = data_json.user.screen_name
    current_tweet['retweet_count'] = data_json.retweet_count
    current_tweet['favorite_count'] = data_json.favorite_count
    current_tweet['text'] = data_json.text
    return

counter = 0
c = 0
search_terms = '"#TheVoiceKids" OR "#TheVoiceKidsBr" OR "The Voice Kids" OR "Carlinhos Brown" OR \
    "Simone Simaria" OR "Claudia Leitte" OR "Eduarda Brasil" OR "Mariah Yohana" OR "Neto Junqueira" OR "Talita Cipriano"'

search_terms2 = '"#Aquecimento Global" OR "Aquecimento Global"'

last_id = 983095386813247488
id2 = 982971217429848064
while True:
    try:
        new_tweets = api.search(q = search_terms2, count=100, include_entities=True,monitor_rate_limit=True,wait_on_rate_limit=True,wait_on_rate_limit_notify = True,retry_count = 5,retry_delay = 5,lang='pt', since_id=str(id2), max_id=str(last_id-1))
        if not new_tweets:
            break
        for tweet in new_tweets:
            json_format(tweet)
            queue.write(json.dumps(current_tweet))
            queue.write(',\n')
            counter+=1
            print 'Number of tweets collected so far...: ', counter
        last_id = new_tweets[-1].id
    except Exception, e:
        continue
    time.sleep(3.5)

queue.close()

#for tweet in tweepy.Cursor(api.search, q = search_terms, count=100, include_entities=True,monitor_rate_limit=True,wait_on_rate_limit=True,wait_on_rate_limit_notify = True,retry_count = 5,retry_delay = 5, since = start_since, until= end_until,lang='pt').items():
#	try:
#		json_format(tweet)
#		queue.write(json.dumps(current_tweet))
#		counter+=1
#		print 'Number of tweets collected so far...:' , counter
#		queue.write('\n')
#	except Exception, e:
#		#log.error(e)
#		logging.exception("message")
#	c+=1
#	if c % 100 == 0:
#		time.sleep(5)
