import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle

# path to all layers
DATADIR = "C:/senior-design/dataset"

# Categories for clean or defective wafer
CATEGORIES = ["clean", "defective"]

# List of all lens sizes
LENS_SIZES = ["5X", "10X", "20X", "50X", "100X"]


# Function to create training data
# TODO: need to implement a way to subtract clean image from defective ones
def create_training_data():
    for category in CATEGORIES:
        path = os.path.join(DATADIR, category)  # gets path of each category
        for lens in os.listdir(path):
            first_time = True  # variable for showing only one image from each magnification
            lens_path = os.path.join(path, lens)  # gets path for each magnification
            for img in os.listdir(lens_path):
                img_array = cv2.imread(os.path.join(lens_path, img),
                                       cv2.IMREAD_GRAYSCALE)  # converts image to grayscale
                training_data.append(img_array)  # appends data to training data
                if first_time:  # shows one image from each magnification
                    plt.imshow(img_array, cmap="gray")  # configures image as grayscale before displaying
                    plt.title(img)  # adds title of image
                    plt.grid(True, color="black")  # creates black grid lines for identification
                    plt.show()  # shows the image to display
                    first_time = False  # resets the variable


# Initializes training data
training_data = []

# Creates training data and shuffles them randomly
create_training_data()
random.shuffle(training_data)

# Prints number of training images and array of all pixel values within each image
print("Number of Training Images: ", len(training_data))
print("Training Data: ", training_data)

X = []  # features (image data)

# Copies image data to X
for features in training_data:
    X.append(features)

# reshapes X before putting in CNN
X = np.array(X).reshape(-1)

# Stores training_data into X.pickle
pickle_out = open("X.pickle", "wb")
pickle.dump(X, pickle_out)
pickle_out.close()

