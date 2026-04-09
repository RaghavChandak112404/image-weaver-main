import os
import string
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.utils import to_categorical, Sequence
from tensorflow.keras.models import Model
from model import define_model

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(BASE_DIR, 'archive (4)', 'Images')
CAPTION_FILE = os.path.join(BASE_DIR, 'archive (4)', 'captions.txt')
FEATURES_FILE = os.path.join(BASE_DIR, 'backend', 'features.pkl')
TOKENIZER_FILE = os.path.join(BASE_DIR, 'backend', 'tokenizer.pkl')
MODEL_FILE = os.path.join(BASE_DIR, 'backend', 'model.h5')

# Extract features from all images using InceptionV3
def extract_features(directory):
    model = InceptionV3()
    model = Model(inputs=model.inputs, outputs=model.layers[-2].output)
    features = dict()
    
    # We will process ALL images to achieve maximum accuracy as you requested.
    # Note: On a local CPU this will take substantial time.
    img_list = os.listdir(directory)
    print(f"Extracting features for {len(img_list)} images. This may take a while...")
    
    for idx, name in enumerate(img_list):
        filename = os.path.join(directory, name)
        image = load_img(filename, target_size=(299, 299))
        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        feature = model.predict(image, verbose=0)
        image_id = name.split('.')[0]
        features[image_id] = feature
        if idx % 100 == 0 and idx > 0:
            print(f"> Processed {idx} images")
    return features

# Load doc into memory
def load_doc(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

# Load descriptions
def load_descriptions(doc, dataset):
    mapping = dict()
    for line in doc.split('\n'):
        tokens = line.split(',')
        if len(tokens) < 2:
            continue
        # Skip the header
        if tokens[0] == 'image':
            continue
        image_id, image_desc = tokens[0], tokens[1:]
        image_id = image_id.split('.')[0]
        image_desc = ' '.join(image_desc)
        
        # Only parse descriptions for images we have extracted features for
        if image_id in dataset:
            if image_id not in mapping:
                mapping[image_id] = list()
            mapping[image_id].append(image_desc)
    return mapping

# Clean descriptions
def clean_descriptions(descriptions):
    table = str.maketrans('', '', string.punctuation)
    for key, desc_list in descriptions.items():
        for i in range(len(desc_list)):
            desc = desc_list[i]
            desc = desc.split()
            desc = [word.lower() for word in desc]
            desc = [w.translate(table) for w in desc]
            desc = [word for word in desc if len(word)>1]
            desc = [word for word in desc if word.isalpha()]
            desc_list[i] = 'startseq ' + ' '.join(desc) + ' endseq'

# Create tokenizer
def to_lines(descriptions):
    all_desc = list()
    for key in descriptions.keys():
        [all_desc.append(d) for d in descriptions[key]]
    return all_desc

def create_tokenizer(descriptions):
    lines = to_lines(descriptions)
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(lines)
    return tokenizer

def max_length(descriptions):
    lines = to_lines(descriptions)
    return max(len(d.split()) for d in lines)

class DataGenerator(Sequence):
    def __init__(self, descriptions, features, tokenizer, max_length, vocab_size, batch_size=32):
        super().__init__()
        self.descriptions = descriptions
        self.features = features
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.vocab_size = vocab_size
        self.batch_size = batch_size
        self.keys = list(descriptions.keys())

    def __len__(self):
        return int(np.ceil(len(self.keys) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_keys = self.keys[idx * self.batch_size:(idx + 1) * self.batch_size]
        X1, X2, y = list(), list(), list()
        
        for key in batch_keys:
            desc_list = self.descriptions[key]
            if key not in self.features: continue
            feature = self.features[key][0]
            for desc in desc_list:
                seq = self.tokenizer.texts_to_sequences([desc])[0]
                for i in range(1, len(seq)):
                    in_seq, out_seq = seq[:i], seq[i]
                    in_seq = pad_sequences([in_seq], maxlen=self.max_length)[0]
                    out_seq = to_categorical([out_seq], num_classes=self.vocab_size)[0]
                    X1.append(feature)
                    X2.append(in_seq)
                    y.append(out_seq)
                    
        return (np.array(X1), np.array(X2)), np.array(y)

def main():
    if not os.path.exists(FEATURES_FILE):
        features = extract_features(IMAGE_DIR)
        with open(FEATURES_FILE, 'wb') as f:
            pickle.dump(features, f)
    else:
        print("Loading features from file...")
        with open(FEATURES_FILE, 'rb') as f:
            features = pickle.load(f)

    doc = load_doc(CAPTION_FILE)
    descriptions = load_descriptions(doc, features)
    clean_descriptions(descriptions)
    print(f"Loaded {len(descriptions)} valid descriptions out of features space.")

    tokenizer = create_tokenizer(descriptions)
    with open(TOKENIZER_FILE, 'wb') as f:
        pickle.dump(tokenizer, f)
    
    vocab_size = len(tokenizer.word_index) + 1
    max_len = max_length(descriptions)
    print(f"Vocabulary Size: {vocab_size}")
    print(f"Max Description Length: {max_len}")

    model = define_model(vocab_size, max_len)
    
    epochs = 20 
    print("Starting training on FULL dataset...")
    generator = DataGenerator(descriptions, features, tokenizer, max_len, vocab_size, batch_size=32)
    
    # Save the model whenever the loss improves
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        MODEL_FILE, 
        monitor='loss', 
        verbose=1, 
        save_best_only=True, 
        mode='min'
    )
    
    model.fit(generator, epochs=epochs, verbose=1, callbacks=[checkpoint])
    print("Training finished. Best model.h5 saved.")

if __name__ == '__main__':
    main()
