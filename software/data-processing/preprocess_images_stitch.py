import os
import cv2

# Path to all layers
DATADIR = "C:/senior-design/software/data-processing/dataset"
clean_src = "clean/10X/10X_CLEAN.jpg"

# List of all lens sizes
LENS_SIZES = ["5X", "10X", "20X"]  # 50X and 100X magnifications are not processed well


# Function to create training data
def process_image_data(processed_image_path):
    """
    Processes all images stored in the defective directory and its subdirectories
    :return: Nothing
    """
    img_array = cv2.i
    clean_img_array = cv2.imread(os.path.join(DATADIR, clean_src), cv2.IMREAD_GRAYSCALE)
    path = os.path.join(DATADIR, "defective")  # gets path of each category
    processed_path = os.path.join(DATADIR, "processed")  # gets path of processed images

    for lens in LENS_SIZES:
        # first_time = True  # variable for showing only one image from each magnification
        lens_path = os.path.join(path, lens)  # gets path for each magnification
        processed_lens_path = os.path.join(processed_path, lens)
        for img in os.listdir(lens_path):
            processed_image_path = os.path.join(processed_lens_path, img)
            if not os.path.exists(processed_image_path):
                img_array = cv2.imread(os.path.join(lens_path, img),
                                       cv2.IMREAD_GRAYSCALE)  # converts image to grayscale
                processed = cv2.subtract(clean_img_array, img_array)  # subtracts the defective wafer with clean one
                processed = cv2.bitwise_not(processed)  # inverts the color so defects are black in color
                (thresh, processed) = cv2.threshold(processed, 225, 255,
                                                    cv2.THRESH_BINARY)  # produces black and white image
                cv2.imwrite(processed_image_path, processed)  # stores processed image


# Creates training data
process_image_data()
