import twitter
import csv
import re
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONSUMER_KEY= 'FXO3pOD6fQoSNr3HbAmEBDagb'
CONSUMER_SECRET= 'o5RMl7fQNP16J7I1iM90hHyT8aJWfTqFJkitDhOdiUX7IU0pUj'
ACCESS_TOKEN_KEY= '2962825242-TFuUe6CKbYR9IcdTHtylkdBzrEciwzpxqb8NEbW'
ACCESS_TOKEN_SECRET= '5LVV7pTJdJheTTtHHLx53lswhI6gWPty5Ttj5yYcsdigs'

api = twitter.Api(consumer_key=CONSUMER_KEY,
  consumer_secret=CONSUMER_SECRET,
    access_token_key=ACCESS_TOKEN_KEY,
    access_token_secret=ACCESS_TOKEN_SECRET)

print(api.VerifyCredentials())

def get_all_tweets(screen_name):
	allTweets = []

	new_tweets = api.GetUserTimeline(screen_name=screen_name, count = 200)
	allTweets.extend(new_tweets)

	oldestTweet = allTweets[-1].id - 1

	while(len(new_tweets) > 0):
		print("Getting tweets before {}".format(oldestTweet))
		new_tweets = api.GetUserTimeline(screen_name=screen_name, count = 200, max_id=oldestTweet)
		allTweets.extend(new_tweets)
		oldestTweet = allTweets[-1].id - 1
		print("... {} Tweets downloaded so far".format(len(allTweets)))
		# delete the retweets
		cleaned_text = [re.sub(r'RT.*','', i.text, flags=re.MULTILINE) for i in allTweets]
		# remove @twitter mentions
		cleaned_text = [re.sub(r'@[\w]*', '', i, flags=re.MULTILINE) for i in cleaned_text]
		# transform the tweets into a 2D array that will populate the csv
		outtweets = [[tweet.id_str, tweet.created_at, cleaned_text[idx].encode('utf-8').decode('utf-8')] for idx, tweet in 		  enumerate(allTweets)]
		
		with open(os.path.join(BASE_DIR,'data-ingestor', 'data', 'raw', '{}_tweets.csv'.format(screen_name)), 'w', newline = '') as file:
			writer = csv.writer(file)
			writer.writerow(['id','created_at', 'text'])
			writer.writerows(outtweets)

if __name__ == '__main__':
	print(api.VerifyCredentials())
	get_all_tweets("nVidia")	

