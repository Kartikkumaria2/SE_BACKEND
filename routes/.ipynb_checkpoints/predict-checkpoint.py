{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 9,
   "id": "c286963d",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "WARNING:tensorflow:6 out of the last 6 calls to <function Model.make_predict_function.<locals>.predict_function at 0x000001F081CCBE20> triggered tf.function retracing. Tracing is expensive and the excessive number of tracings could be due to (1) creating @tf.function repeatedly in a loop, (2) passing tensors with different shapes, (3) passing Python objects instead of tensors. For (1), please define your @tf.function outside of the loop. For (2), @tf.function has reduce_retracing=True option that can avoid unnecessary retracing. For (3), please refer to https://www.tensorflow.org/guide/function#controlling_retracing and https://www.tensorflow.org/api_docs/python/tf/function for  more details.\n",
      "1/1 [==============================] - 0s 200ms/step\n",
      "Surprise\n"
     ]
    }
   ],
   "source": [
    "from keras.preprocessing.image import ImageDataGenerator\n",
    "import cv2\n",
    "import numpy as np\n",
    "from tensorflow.keras.models import load_model\n",
    "from tensorflow.keras.applications.resnet50 import preprocess_input\n",
    "import os\n",
    "\n",
    "# Load the pre-trained emotion detection model\n",
    "emotion_model = load_model(\"face_emotion.h5\")\n",
    "\n",
    "# Create a list of emotion labels\n",
    "emotion_labels = [\"Angry\", \"Disgust\", \"Fear\", \"Happy\", \"Sad\", \"Surprise\", \"Neutral\"]\n",
    "\n",
    "# Load a face detection classifier (you can replace it with your preferred face detector)\n",
    "face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')\n",
    "\n",
    "# Create an ImageDataGenerator object with the same preprocessing parameters as your training data\n",
    "train_aug = ImageDataGenerator(\n",
    "        preprocessing_function=preprocess_input,\n",
    "        rotation_range=25, width_shift_range=0.1,\n",
    "        height_shift_range=0.1, shear_range=0.2, \n",
    "        zoom_range=0.2,horizontal_flip=True, \n",
    "        fill_mode=\"nearest\")\n",
    "\n",
    "# Get the current directory\n",
    "current_dir = os.getcwd()\n",
    "\n",
    "# Construct the path to the image\n",
    "image_path = os.path.join(current_dir, '..', 'uploads/photo-1699243507318.jpg')\n",
    "\n",
    "frame = cv2.imread(image_path)\n",
    "\n",
    "frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)\n",
    "\n",
    "# Convert the frame to grayscale for face detection\n",
    "gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)\n",
    "\n",
    "# Detect faces in the frame\n",
    "faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))\n",
    "\n",
    "for (x, y, w, h) in faces:\n",
    "    # Extract the face from the frame\n",
    "    face = gray[y:y+h, x:x+w]\n",
    "\n",
    "    # Convert grayscale face to 3-channels\n",
    "    face = cv2.cvtColor(face, cv2.COLOR_GRAY2BGR)\n",
    "    \n",
    "    # Resize the face image to the size expected by the model\n",
    "    face = cv2.resize(face, (48, 48))\n",
    "\n",
    "    # Preprocess the face image using the ImageDataGenerator object\n",
    "    face = train_aug.random_transform(face)\n",
    "    face = np.expand_dims(face, axis=0)\n",
    "    face = preprocess_input(face)  # Now it should not raise an error\n",
    "\n",
    "    # Reshape the face image for the model input\n",
    "    face = face.reshape((1, 48, 48, 3))\n",
    "\n",
    "    # Predict the emotion label for the face\n",
    "    emotion = emotion_model.predict(face)\n",
    "    emotion_label = emotion_labels[np.argmax(emotion)]\n",
    "\n",
    "    # Draw a rectangle around the detected face and annotate with the emotion label\n",
    "    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)\n",
    "    cv2.putText(frame, emotion_label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)\n",
    "\n",
    "print(emotion_label)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "42fe215b",
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "f753b8f3",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.4"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
