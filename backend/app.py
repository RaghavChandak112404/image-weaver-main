import os
import io
import pickle
import numpy as np
import base64
from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import img_to_array

# Load models and configurations
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FILE = os.path.join(BASE_DIR, 'model.h5')
TOKENIZER_FILE = os.path.join(BASE_DIR, 'tokenizer.pkl')

app = Flask(__name__)
CORS(app)

print("Loading InceptionV3 model (Feature Extractor)...")
inception = InceptionV3()
feature_extractor = tf.keras.Model(inputs=inception.inputs, outputs=inception.layers[-2].output)

caption_model = None
tokenizer = None
max_length = 34 # Standard for flickr8k, fallback

from model import define_model

if os.path.exists(MODEL_FILE) and os.path.exists(TOKENIZER_FILE):
    print("Loading Caption Model and Tokenizer...")
    with open(TOKENIZER_FILE, 'rb') as f:
        tokenizer = pickle.load(f)
    
    print("Re-assembling model architecture to load weights exclusively...")
    vocab_size = len(tokenizer.word_index) + 1
    caption_model = define_model(vocab_size, max_length)
    caption_model.load_weights(MODEL_FILE)
else:
    print("WARNING: Model or Tokenizer not found! Please run train.py first.")

def idx_to_word(integer, tokenizer):
    for word, index in tokenizer.word_index.items():
        if index == integer:
            return word
    return None

def generate_caption(image_bytes):
    if caption_model is None or tokenizer is None:
        return "Model not trained yet."
    
    # Process Image
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((299, 299))
    img_array = img_to_array(img)
    img_array = img_array.reshape((1, img_array.shape[0], img_array.shape[1], img_array.shape[2]))
    img_array = preprocess_input(img_array)
    
    # Extract feature
    feature = feature_extractor.predict(img_array, verbose=0)
    
    # Generate caption
    in_text = 'startseq'
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        sequence = pad_sequences([sequence], maxlen=max_length)
        yhat = caption_model.predict([feature, sequence], verbose=0)
        yhat = np.argmax(yhat)
        word = idx_to_word(yhat, tokenizer)
        if word is None:
            break
        in_text += " " + word
        if word == 'endseq':
            break
    
    final_caption = in_text.replace('startseq ', '').replace(' endseq', '')
    return final_caption.capitalize()

@app.route('/predict_caption', methods=['POST'])
def predict_caption():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    img_bytes = file.read()
    
    try:
        caption = generate_caption(img_bytes)
        return jsonify({'caption': caption})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
