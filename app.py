from flask import Flask, request, jsonify
import pickle
import re
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

app = Flask(__name__)
from flask_cors import CORS
CORS(app)
port_stem = PorterStemmer()
stop_words = set(stopwords.words('english'))
model = pickle.load(open('model.pkl', 'rb'))
vectorizer = pickle.load(open('vectorizer.pkl', 'rb'))

def stemming(content):
    stemmed_content = re.sub('[^a-zA-Z]', ' ', content)
    stemmed_content = stemmed_content.lower()
    stemmed_content = stemmed_content.split()
    stemmed_content = [port_stem.stem(word) for word in stemmed_content if word not in stop_words]
    return ' '.join(stemmed_content)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    text = data['text']
    processed = stemming(text)
    vect = vectorizer.transform([processed])
    pred = model.predict(vect)
    result = "Real" if pred[0] == 0 else "Fake"
    return jsonify({'prediction': result})

if __name__ == '__main__':
    app.run(debug=True)
