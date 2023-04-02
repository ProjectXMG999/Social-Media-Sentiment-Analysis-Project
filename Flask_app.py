from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import joblib
from transformers import TfidfVectorizer, XLMRobertaModel

app = Flask(__name__)

# Load the model and vectorizer
model = joblib.load('sentiment_model.pkl')
vectorizer = TfidfVectorizer()

# Set up rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['100 per day']
)

# Define a simple authentication function
def authenticate(username, password):
    if username == 'admin' and password == 'password':
        return True
    else:
        return False

@app.route('/predict', methods=['POST'])
@limiter.limit('10 per minute')
def predict_sentiment():
    # Check authentication
    auth = request.authorization
    if not auth or not authenticate(auth.username, auth.password):
        abort(401)
    
    # Get the text from the request
    text = request.json.get('text')
    if not text:
        abort(400, description='Text field is missing or empty')
    
    # Preprocess the text and extract features
    features = vectorizer.transform([text])
    
    # Make a prediction using the model
    sentiment = model.predict(features)[0]
    
    # Return the prediction as a JSON response
    response = {'sentiment': sentiment}
    return jsonify(response)

@app.errorhandler(400)
def bad_request(error):
    response = jsonify({'message': error.description})
    response.status_code = 400
    return response

@app.errorhandler(401)
def unauthorized(error):
    response = jsonify({'message': 'Unauthorized access'})
    response.status_code = 401
    return response

@app.errorhandler(429)
def ratelimit_handler(e):
    response = jsonify({
        'error': 'ratelimit exceeded {}'.format(e.description)
    })
    response.status_code = 429
    return response

if __name__ == '__main__':
    app.run(debug=True)
