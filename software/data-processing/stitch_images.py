import os
import cv2
import matplotlib.pyplot as plt
from PIL import Image

DATADIR = "C:/senior-design/software/data-processing/dataset"
IMAGE_TYPES = ["defective", "processed"]
LENS_SIZES = ["5X", "10X", "20X"]

always = True


def merge_images(Image_1, Image_2):
    """
    Merge two images into one, displayed side by side
    :parameter image_1: first image file
    :parameter image_2: second image file
    :return: Result image
    """

    result = Image.new('RGB', (Image_1.size[0] + Image_2.size[0], Image_1.size[1]))
    result.paste(Image_1, (0, 0))
    result.paste(Image_2, (Image_1.size[0], 0))

    return result


def save_image(image, image_name, save_image_type):
    """
    Saves the final image to the OS (accounting for duplicates)
    :param image: Image object
    :param image_name: Name user wants for the image
    :param save_image_type: What type of image it is
    :return: Nothing
    """
    if save_image_type == "defective":
        image_save_path = os.path.join(DATADIR, "defective-stitched")
    else:
        image_save_path = os.path.join(DATADIR, "processed-stitched")

    image_save_path = os.path.join(image_save_path, image_name)

    image_save_dupe_path = ""

    is_image_save_dupe = False  # Flag for checking if output is a duplicate copy

    counter = 0

    if os.path.exists(image_save_path + ".jpg"):  # If the file exists, increment a counter to find a file that
        is_image_save_dupe = True  # does not exist
        counter = 1
        image_save_dupe_path = (image_save_path + "_{}").format(str(counter))
        while os.path.exists(image_save_dupe_path + ".jpg"):
            counter += 1
            image_save_dupe_path = (image_save_path + "_{}").format(str(counter))

    if not is_image_save_dupe:  # Gets the name for the file
        final_image_save_path = image_save_path + ".jpg"
    else:
        print(f'There are {counter} duplicate image(s) with the same name already saved. Renaming to '
              f'{(image_name + "_{}.jpg").format(str(counter))}')
        final_image_save_path = image_save_dupe_path + ".jpg"

    image.save(final_image_save_path)

    processed_image_data = cv2.imread(final_image_save_path)

    plt.imshow(processed_image_data, cmap="gray")  # display the image requested
    plt.grid(True, color='black')
    plt.show()


while always:
    first_time = True
    continue_stitching_images = 'Y'
    image_type = input("What type of images would you like to stitch together (defective, processed)?\n").lower()
    if image_type in IMAGE_TYPES:
        print(f'You entered an image type of {image_type}.')
        image_type_path = os.path.join(DATADIR, image_type)
        magnification = input("What magnification would you like to stitch images of? (5X, 10X, 20X)\n").upper()
        if magnification in LENS_SIZES:
            print(f'You entered a magnification of {magnification}.')
            lens_path = os.path.join(image_type_path, magnification)
            if first_time:
                image_1_name = input("What first image would you like to stitch together?\n").upper()
                image_1_path = os.path.join(lens_path, image_1_name + ".jpg")
            while continue_stitching_images == 'Y':
                if not first_time or os.path.exists(image_1_path):
                    if not first_time:
                        image_2_name = input("What other image would you like to stitch together?\n").upper()
                    else:
                        image_1 = Image.open(image_1_path)
                        image_2_name = input("What second image would you like to stitch together?\n").upper()
                    image_2_path = os.path.join(lens_path, image_2_name + ".jpg")
                    if os.path.exists(image_2_path):
                        image_2 = Image.open(image_2_path)
                        result_image = merge_images(image_1, image_2)
                        if first_time:
                            first_time = False
                        continue_stitching_images = input("Would you like to continue stitching images? (Y/N)\n").upper()
                        if continue_stitching_images == 'Y':
                            image_1 = result_image
                            continue
                        else:
                            save_image_name = input("What name would you like to give this image?\n").upper()
                            save_image(result_image, save_image_name, image_type)
                            user_done = input('Exit? (Y/N)\n').upper()
                            if user_done == 'Y':
                                continue_stitching_images = False
                                always = False
                    else:
                        print("That is an invalid image name.\n")
                else:
                    print("That is an invalid image name.\n")
            else:
                print("That is an invalid image name.\n")
        else:
            print("That is an invalid magnification.\n")
    else:
        print("The image type entered is not valid. Please try again.\n")
