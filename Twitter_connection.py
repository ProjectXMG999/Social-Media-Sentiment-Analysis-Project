import tweepy

consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_token_secret = 'your_access_token_secret'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class TweetListener(tweepy.StreamListener):
    def on_status(self, status):
        # Ignore retweets
        if 'RT @' in status.text:
            return
        
        # Ignore replies
        if status.in_reply_to_status_id is not None:
            return
        
        # Ignore tweets that don't mention our brand
        if 'my_brand' not in status.text.lower():
            return
        
        # Classify the sentiment of the tweet
        sentiment = classify_sentiment(status.text)
        
        # Process the tweet (e.g., store it in a database, send an alert to a user, etc.)
        process_tweet(status.id, status.text, sentiment)

    def on_error(self, status_code):
        if status_code == 420:
            # Return False on_data method in case rate limit occurs.
            return False


listener = TweetListener()
stream = tweepy.Stream(auth=api.auth, listener=listener)
stream.filter(track=['my_brand'])


# analyze the data stored in the database to gain insights.
# querying the database to find the most common named entities mentioned in tweets about our brand.

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('tweets.db')

# Query the database to find the most common named entities
results = conn.execute('''SELECT named_entities
                          FROM tweets
                          WHERE sentiment = 'positive' ''')

# Count the frequency of named entities
named_entities_count = {}
for row in results:
    named_entities = row[0].split(', ')
    for named_entity in named_entities:
        if named_entity in named_entities_count:
            named_entities_count[named_entity] += 1
        else:
            named_entities_count[named_entity] = 1

# Sort the named entities by frequency
sorted_named_entities = sorted(named_entities_count.items(), key=lambda x: x[1], reverse=True)

# Print the top 10 named entities
for named_entity, count in sorted_named_entities[:10]:
    print(named_entity, count)


