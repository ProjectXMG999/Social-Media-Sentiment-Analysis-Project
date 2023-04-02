import matplotlib.pyplot as plt

# Create a TweetAnalyzer object and get the top named entities
analyzer = TweetAnalyzer('tweets.db')
top_named_entities = analyzer.get_top_named_entities(sentiment='positive', num_entities=10)

# Extract the named entities and their frequencies into separate lists
named_entities = [ne[0] for ne in top_named_entities]
frequencies = [ne[1] for ne in top_named_entities]

# Create a bar chart of the top named entities
fig, ax = plt.subplots()
ax.bar(named_entities, frequencies)
ax.set_xticklabels(named_entities, rotation=45, ha='right')
ax.set_xlabel('Named Entity')
ax.set_ylabel('Frequency')
ax.set_title('Most Common Named Entities in Positive Tweets')

plt.show()


# need to connect with TweetAnalyzer class
