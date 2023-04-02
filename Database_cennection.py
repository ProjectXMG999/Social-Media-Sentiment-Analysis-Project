import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('tweets.db')

# Create a table to store tweet data
conn.execute('''CREATE TABLE tweets
             (id INTEGER PRIMARY KEY,
             text TEXT,
             sentiment TEXT,
             named_entities TEXT)''')

def process_tweet(tweet_id, tweet_text, sentiment, named_entities):
    # Store the tweet data in the SQLite database
    conn.execute("INSERT INTO tweets (id, text, sentiment, named_entities) VALUES (?, ?, ?, ?)",
                 (tweet_id, tweet_text, sentiment, ', '.join(named_entities)))
    conn.commit()

    
 # some changes in Tweetlistener class

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
        
        # Extract named entities from the tweet
        named_entities = extract_named_entities(status.text)
        
        # Store the tweet data in the database
        process_tweet(status.id, status.text, sentiment, named_entities)

    def on_error(self, status_code):
        if status_code == 420:
            # Return False on_data method in case rate limit occurs.
            return False
