# preprocess a dataset of labeled tweets,
# splitting it into training and testing sets,
# training a Naive Bayes classifier on the training set,
# testing the classifier on the testing set,
# and using the classifier to classify new tweets.


import nltk
import random
from nltk.corpus import twitter_samples
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.classify import NaiveBayesClassifier

# Define a function to preprocess a tweet
def preprocess_tweet(tweet):
    # Remove URLs, usernames, and hashtags
    tweet = re.sub(r'http\S+|@\S+|#\S+', '', tweet)
    # Convert to lowercase
    tweet = tweet.lower()
    # Tokenize the tweet
    tokens = nltk.word_tokenize(tweet)
    # Remove stop words and lemmatize the tokens
    stop_words = stopwords.words('english')
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
    # Return the preprocessed tweet
    return tokens

# Load the labeled dataset of tweets
positive_tweets = [(preprocess_tweet(tweet), 'positive') for tweet in twitter_samples.strings('positive_tweets.json')]
negative_tweets = [(preprocess_tweet(tweet), 'negative') for tweet in twitter_samples.strings('negative_tweets.json')]
all_tweets = positive_tweets + negative_tweets
random.shuffle(all_tweets)

# Split the dataset into training and testing sets
train_tweets = all_tweets[:int(len(all_tweets)*0.8)]
test_tweets = all_tweets[int(len(all_tweets)*0.8):]

# Train a Naive Bayes classifier on the training set
classifier = NaiveBayesClassifier.train(train_tweets)

# Test the classifier on the testing set
accuracy = nltk.classify.accuracy(classifier, test_tweets)
print(f'Accuracy: {accuracy:.2%}')

# Classify some new tweets
new_tweets = ['I love this product!', 'This product is terrible!']
for tweet in new_tweets:
    tokens = preprocess_tweet(tweet)
    sentiment = classifier.classify(dict([token, True] for token in tokens))
    print(f'{tweet} -> {sentiment}')
    
    
    
###### Evaluating on more complex data 

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from nltk.sentiment import SentimentIntensityAnalyzer

# Load the customer reviews dataset
reviews_df = pd.read_csv('customer_reviews.csv')

# Preprocess the reviews
reviews_df['text'] = reviews_df['text'].apply(preprocess_text)

# Initialize the sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Apply the sentiment analyzer to the reviews
reviews_df['sentiment'] = reviews_df['text'].apply(lambda text: 'positive' if sia.polarity_scores(text)['compound'] > 0 else 'negative')

# Calculate the accuracy and F1 score of the model
accuracy = accuracy_score(reviews_df['sentiment'], reviews_df['true_sentiment'])
f1 = f1_score(reviews_df['sentiment'], reviews_df['true_sentiment'], pos_label='positive')
print(f'Accuracy: {accuracy:.2%}')
print(f'F1 score: {f1:.2%}')

