import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
import random
import pickle

# path to all layers
DATADIR = "C:/senior-design/dataset"
clean_src = "clean/10X/10X_CLEAN.jpg"

# Categories for clean or defective wafer
# CATEGORIES = ["clean", "defective"]

# List of all lens sizes
LENS_SIZES = ["5X", "10X", "20X", "50X"]  # need to add 100X later


# Function to create training data
# TODO: need to implement a way to subtract clean image from defective ones
def create_training_data():
    clean_img_array = cv2.imread(os.path.join(DATADIR, clean_src), cv2.IMREAD_GRAYSCALE)
    plt.imshow(clean_img_array, cmap="gray")
    plt.title("10X_CLEAN.jpg")  # adds title of image
    plt.grid(True, color="black")  # creates black grid lines for identification
    plt.show()  # shows the image to display

    path = os.path.join(DATADIR, "defective")  # gets path of each category

    for lens in LENS_SIZES:
        first_time = True  # variable for showing only one image from each magnification
        lens_path = os.path.join(path, lens)  # gets path for each magnification
        for img in os.listdir(lens_path):
            img_array = cv2.imread(os.path.join(lens_path, img),
                                   cv2.IMREAD_GRAYSCALE)  # converts image to grayscale
            subtracted = cv2.subtract(clean_img_array, img_array)  # subtracts the defective wafers with the clean wafer
            subtracted = cv2.bitwise_not(subtracted)  # inverts the color so defects are black in color
            (thresh, subtracted) = cv2.threshold(subtracted, 200, 255,
                                                 cv2.THRESH_BINARY)  # produces black and white image
            training_data.append(subtracted)  # appends data to training data
            if first_time:  # shows one image from each magnification
                plt.imshow(subtracted, cmap="gray")  # configures image as grayscale before displaying
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
