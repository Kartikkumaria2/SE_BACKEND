from keras.preprocessing.image import ImageDataGenerator
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
import os
import json

# Load the pre-trained emotion detection model
emotion_model = load_model("E:\\SE_BACKEND\\routes\\face_emotion.h5")

# Create a list of emotion labels
emotion_labels = ["Angry", "Disgust", "Fear", "Happy", "Sad", "Surprise", "Neutral"]

# Load a face detection classifier (you can replace it with your preferred face detector)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Get the current directory
current_dir = os.getcwd()

train_aug = ImageDataGenerator(
        preprocessing_function=preprocess_input,
        rotation_range=25, width_shift_range=0.1,
        height_shift_range=0.1, shear_range=0.2, 
        zoom_range=0.2,horizontal_flip=True, 
        fill_mode="nearest")

# Specify the path to the folder containing images
image_folder = 'E:\\SE_BACKEND\\uploads\\'

# Get a list of all files in the folder
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Sort the files based on modification time (latest first)
latest_image = max(image_files, key=os.path.getmtime)

# Read the latest image
frame = cv2.imread(latest_image)

frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)

# Convert the frame to grayscale for face detection
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Detect faces in the frame
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

emotion_label = "No face detected"

for (x, y, w, h) in faces:
    # Extract the face from the frame
    face = gray[y:y+h, x:x+w]

    # Convert grayscale face to 3-channels
    face = cv2.cvtColor(face, cv2.COLOR_GRAY2BGR)
    
    # Resize the face image to the size expected by the model
    face = cv2.resize(face, (48, 48))

    # Preprocess the face image using the ImageDataGenerator object
    face = train_aug.random_transform(face)
    face = np.expand_dims(face, axis=0)
    face = preprocess_input(face)

    # Reshape the face image for the model input
    face = face.reshape((1, 48, 48, 3))

    # Predict the emotion label for the face
    emotion = emotion_model.predict(face)
    emotion_label = emotion_labels[np.argmax(emotion)]

    # Draw a rectangle around the detected face and annotate with the emotion label
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

print(json.dumps(emotion_label))
