import cv2
import numpy as np
import os
import sys
import tensorflow as tf
import keras
from keras import layers

from sklearn.model_selection import train_test_split

EPOCHS = 10
IMG_WIDTH = 30
IMG_HEIGHT = 30
NUM_CATEGORIES = 43
TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) not in [2, 3]:
        sys.exit("Usage: python traffic.py data_directory [model.h5]")

    # Get image arrays and labels for all image files
    images, labels = load_data(sys.argv[1])

    # Split data into training and testing sets
    labels = tf.keras.utils.to_categorical(labels)
    x_train, x_test, y_train, y_test = train_test_split(
        np.array(images), np.array(labels), test_size=TEST_SIZE
    )

    # Get a compiled neural network
    model = get_model()

    # Fit model on training data
    model.fit(x_train, y_train, epochs=EPOCHS)

    # Evaluate neural network performance
    model.evaluate(x_test,  y_test, verbose=2)

    # Save model to file
    if len(sys.argv) == 3:
        filename = sys.argv[2]
        model.save(filename)
        print(f"Model saved to {filename}.")


def load_data(data_dir):
    """
    Load image data from directory `data_dir`.

    Assume `data_dir` has one directory named after each category, numbered
    0 through NUM_CATEGORIES - 1. Inside each category directory will be some
    number of image files.

    Return tuple `(images, labels)`. `images` should be a list of all
    of the images in the data directory, where each image is formatted as a
    numpy ndarray with dimensions IMG_WIDTH x IMG_HEIGHT x 3. `labels` should
    be a list of integer labels, representing the categories for each of the
    corresponding `images`.


    """
    images = []
    labels = []
    
    for dir in os.scandir(data_dir):
        if dir.is_dir():
            categorie = dir.name
            for image in os.scandir(dir):

                img_array = cv2.imread(image.path)
                resized_img = cv2.resize(img_array, (IMG_WIDTH, IMG_HEIGHT))

                images.append(resized_img)
                labels.append(categorie)

    data = (images, labels)

    return data

def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    input_layer = layers.InputLayer(input_shape=[IMG_WIDTH, IMG_HEIGHT, 3])
    conv2d_layer = layers.Conv2D(32, 3, activation='relu')
    pooling2d_layer = layers.MaxPooling2D(pool_size=(2, 2))
    flatten_layer = layers.Flatten()
    dense_layer = layers.Dense(32, activation='relu')
    output_layer = layers.Dense(43, activation='softmax')

    model = tf.keras.Sequential(
        [
            input_layer,
            conv2d_layer,
            pooling2d_layer,
            flatten_layer,
            dense_layer,
            output_layer
        ]
    )
    return model

if __name__ == "__main__":
    main()
