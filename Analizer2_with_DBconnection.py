class TweetAnalyzer:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        
    def get_top_named_entities(self, sentiment='positive', num_entities=10):
        # Query the database to find the most common named entities
        results = self.conn.execute(f'''SELECT named_entities
                                        FROM tweets
                                        WHERE sentiment = '{sentiment}' ''')

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

        # Return the top N named entities
        return sorted_named_entities[:num_entities]

analyzer = TweetAnalyzer('tweets.db')
top_named_entities = analyzer.get_top_named_entities(sentiment='positive', num_entities=10)
for named_entity, count in top_named_entities:
    print(named_entity, count)
