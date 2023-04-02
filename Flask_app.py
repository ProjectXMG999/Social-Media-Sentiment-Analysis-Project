from flask import Flask, request, jsonify
import joblib
from transformers import TfidfVectorizer, XLMRobertaModel

app = Flask(__name__)

# Load the model and vectorizer
model = joblib.load('sentiment_model.pkl')
vectorizer = TfidfVectorizer()

@app.route('/predict', methods=['POST'])
def predict_sentiment():
    # Get the text from the request
    text = request.json['text']
    
    # Preprocess the text and extract features
    features = vectorizer.transform([text])
    
    # Make a prediction using the model
    sentiment = model.predict(features)[0]
    
    # Return the prediction as a JSON response
    response = {'sentiment': sentiment}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
