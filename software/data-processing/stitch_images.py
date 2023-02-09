import os
import time
import cv2
import matplotlib.pyplot as plt
from PIL import Image


DATADIR = "C:/senior-design/software/data-processing/dataset"
IMAGE_TYPES = ["defective", "processed"]
LENS_SIZES = ["5X", "10X", "20X"]

always = True

def merge_images(image_1, image_2, image_type):
    """
    Merge two images into one, displayed side by side
    :parameter image_1: path to first image file
    :parameter image_2: path to second image file
    :parameter image_type: identifies whether image is defective or processed
    :return: Nothing
    """
    Image_1 = Image.open(image_1)
    Image_2 = Image.open(image_2)

    result = Image.new('RGB', (2 * Image_1.size[0], Image_1.size[1]))
    result.paste(Image_1, (0, 0))
    result.paste(Image_2, (Image_1.size[0], 0))

    if image_type == "defective":
        image_save_path = os.path.join(DATADIR, "defective-stitched")
    else:
        image_save_path = os.path.join(DATADIR, "processed-stitched")

    image_save_path = os.path.join(image_save_path, "stitched")

    image_save_dupe_path = ""

    is_image_save_dupe = False  # Flag for checking if output is a duplicate copy

    if os.path.exists(image_save_path + ".jpg"):  # If the file exists, increment a counter to find a file that
        is_image_save_dupe = True  # does not exist
        counter = 1
        image_save_dupe_path = (image_save_path + "_{}").format(str(counter))
        while os.path.exists(image_save_dupe_path + ".jpg"):
            counter += 1
            image_save_dupe_path = (image_save_path + "_{}").format(str(counter))

    if not is_image_save_dupe:                          # Gets the name for the file
        final_image_save_path = image_save_path + ".jpg"
    else:
        final_image_save_path = image_save_dupe_path + ".jpg"

    result.save(final_image_save_path)

    processed_image_data = cv2.imread(final_image_save_path)

    plt.imshow(processed_image_data, cmap="gray")  # display the image requested
    plt.grid(True, color='black')
    plt.show()

while always:
    image_type = input("What type of images would you like to stitch together (defective, processed)?\n").lower()
    if image_type in IMAGE_TYPES:
        print(f'You entered an image type of {image_type}.')
        image_type_path = os.path.join(DATADIR, image_type)
        magnification = input("What magnification would you like to stitch images of? (5X, 10X, 20X)\n").upper()
        if magnification in LENS_SIZES:
            print(f'You entered a magnification of {magnification}.')
            lens_path = os.path.join(image_type_path, magnification)
            image_1_name = input("What first image would you like to stitch together?\n").upper()
            image_1_path = os.path.join(lens_path, image_1_name + ".jpg")
            if os.path.exists(image_1_path):
                image_2_name = input("What second image would you like to stitch together?\n").upper()
                image_2_path = os.path.join(lens_path, image_2_name + ".jpg")
                if os.path.exists(image_2_path):
                    start_time = time.time()  # Calculates time of statistical analysis and displays it to console
                    merge_images(image_1_path, image_2_path, image_type)
                    end_time = time.time()
                    print(f'Total time: {round(end_time - start_time, 2)} seconds')
                    user_done = input('Exit? (Y/N)\n').upper()
                    if user_done == 'Y':
                        always = False
                else:
                    print("That is an invalid image name.\n")
            else:
                print("That is an invalid image name.\n")
        else:
            print("That is an invalid magnification.\n")
    else:
        print("The image type entered is not valid. Please try again.\n")
