
# in progress

import spacy

# Load the Spacy NLP model
nlp = spacy.load("en_core_web_sm")

def extract_named_entities(tweet_text):
    # Process the tweet text using the Spacy NLP model
    doc = nlp(tweet_text)
    
    # Extract the named entities from the processed text
    named_entities = [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'PRODUCT']]
    
    # Return the list of named entities
    return named_entities
  

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
        
        # Process the tweet (e.g., store it in a database, send an alert to a user, etc.)
        process_tweet(status.id, status.text, sentiment, named_entities)

    def on_error(self, status_code):
        if status_code == 420:
            # Return False on_data method in case rate limit occurs.
            return False

