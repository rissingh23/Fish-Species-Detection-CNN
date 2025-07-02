import os
import json
import pickle

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras import layers, Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from sklearn.model_selection import train_test_split

# --- CONFIG ---
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'Fish_Dataset')
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# --- BUILD DATAFRAME ---
paths, labels = [], []
for root, _, files in os.walk(DATA_DIR):
    if 'GT' in root:
        continue
    for fname in files:
        if fname.lower().endswith('.png'):
            paths.append(os.path.join(root, fname))
            labels.append(os.path.basename(root))
df = pd.DataFrame({'path': paths, 'label': labels})

# --- SPLIT ---
train_df, test_df = train_test_split(df, train_size=0.8, random_state=42, shuffle=True)

# --- IMAGE GENS ---
train_gen = ImageDataGenerator(preprocessing_function=preprocess_input, validation_split=0.2)
test_gen  = ImageDataGenerator(preprocessing_function=preprocess_input)

train_images = train_gen.flow_from_dataframe(
    dataframe=train_df, x_col='path', y_col='label',
    target_size=(224, 224), batch_size=32,
    class_mode='categorical', subset='training', seed=42, shuffle=True
)
val_images = train_gen.flow_from_dataframe(
    dataframe=train_df, x_col='path', y_col='label',
    target_size=(224, 224), batch_size=32,
    class_mode='categorical', subset='validation', seed=42, shuffle=True
)
test_images = test_gen.flow_from_dataframe(
    dataframe=test_df,  x_col='path', y_col='label',
    target_size=(224, 224), batch_size=32,
    class_mode='categorical', shuffle=False
)

# --- SAVE CLASS INDICES ---
# so we can map back from model outputs to human labels in production
with open(os.path.join(MODELS_DIR, 'class_indices.json'), 'w') as f:
    json.dump(train_images.class_indices, f)

# --- BUILD MODEL ---
base = MobileNetV2(input_shape=(224,224,3), include_top=False, weights='imagenet', pooling='avg')
base.trainable = False

x = layers.Dense(128, activation='relu')(base.output)
x = layers.Dense(128, activation='relu')(x)
outputs = layers.Dense(len(train_images.class_indices), activation='softmax')(x)

model = Model(base.input, outputs)
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# --- TRAIN ---
history = model.fit(train_images, validation_data=val_images, epochs=5)

# --- EVAL ---
loss, acc = model.evaluate(test_images, verbose=0)
print(f"Test Loss: {loss:.5f}   Test Accuracy: {acc*100:.2f}%")

# --- SAVE MODEL (.keras format) ---
model.save(os.path.join(MODELS_DIR, 'fish_classifier.keras'))

# --- SAVE HISTORY ---
with open(os.path.join(MODELS_DIR, 'history.pkl'), 'wb') as f:
    pickle.dump(history.history, f)
