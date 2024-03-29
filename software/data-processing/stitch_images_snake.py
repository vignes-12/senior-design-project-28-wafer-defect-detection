import os
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from stats_stitch import generate_statistics

print("Welcome to the stitch wafer image algorithm!")

DATADIR = "C:\senior-design\software\data-processing\dataset\processed-stitched-snake"
always = True


def stitch_images_snake(directory_path, x, y):
    """
    Stitches images in a snake pattern (assumes all images are of the same dimension)
    :param directory_path: path to stitching image
    :param x: How many images wide the final image will be
    :param y: How many images long the final image will be
    :return: Stitched image
    """

    total_images = x * y  # total number of images in final image
    known_images = []  # list of known images
    image_stitch_needed = False  # flag for whether a new image needs to be stitched
    first_time = True  # first time stitching flag

    # Image stitching counters
    row_counter = 0  # row counter
    column_counter = 0  # column counter
    total_counter = 0  # total images stitched counter
    x_pixels = 0  # pixel counter for x-axis
    y_pixels = 0  # pixel counter for y-axis

    result_image = Image  # result image

    while total_counter < total_images:  # loop for each image that needs stitching
        all_images = os.listdir(directory_path)  # get all image names
        new_image_name = [x for x in all_images if x not in known_images]  # find new image
        if len(new_image_name) == 1:  # if there is a new image
            image_stitch_needed = True  # set the flag true

        if image_stitch_needed:  # if there are new images that need to be stitched
            print(f"New image #{total_counter + 1} " + new_image_name[0] + " found. Stitching it now...")
            known_images.append(new_image_name[0])  # append the new image to known images
            new_image = Image.open(os.path.join(directory_path, new_image_name[0]))  # open the image

            if first_time:  # if it's the first time stitching
                first_time = False  # set the flag to false
                x_pixels = new_image.size[0]  # get the x and y lengths of each image
                y_pixels = new_image.size[1]
                result_image = Image.new("RGB", (x_pixels * x, y_pixels * y))  # and create a resulting image

            if row_counter % 2 == 0 and column_counter < y:  # if row number is even,  then we are moving right
                result_image.paste(new_image, (row_counter * x_pixels, column_counter * y_pixels))  # stitch the image
                total_counter += 1  # increase the total image counter
                column_counter += 1  # increase the column counter
                if column_counter == y:  # if we are finished stitching that row, then increment row counter
                    row_counter += 1
                image_stitch_needed = False  # and set the image stitch needed flag to false

            elif row_counter % 2 == 1 and column_counter > 0:  # else if the row number is odd, then we are moving left
                column_counter -= 1  # decrement the column counter
                result_image.paste(new_image, (row_counter * x_pixels, column_counter * y_pixels))  # stitch the image
                total_counter += 1  # increment the total image counter
                if column_counter == 0:  # if we are finished stitching that row, then increment row counter
                    row_counter += 1
                image_stitch_needed = False  # and set the image stitch needed flag to false

    return result_image


def save_image(image, image_name, image_path):
    """
    Saves the image given its name and specified location
    :param image: Stitched image
    :param image_name: Name of image
    :param image_path: Path of image
    :return: Flag saying it's done
    """

    image_save_path = os.path.join(image_path, image_name)

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

    return True


while always:
    directory_name = input("What directory would you like to store all images for stitching into?").upper()
    directory_path = os.path.join(DATADIR, directory_name)
    if not os.path.exists(directory_path):
        print("Path does not exist. Creating new directory " + directory_name + "...")
        os.mkdir(directory_path)
    else:
        x_images = input("How many images horizontally will the final image be?")
        if not x_images.isnumeric():
            print("That is not a valid dimension size. Please try again.")
            continue
        else:
            x_images = int(x_images)
            y_images = input("How many images vertically will the final image be?")
            if not y_images.isnumeric():
                print("That is not a valid dimension size. Please try again.")
                continue
            else:
                y_images = int(y_images)
                stitched_image = stitch_images_snake(directory_path, x_images, y_images)
                stitched_image_name = input("What would you like to call the final image name?").upper()
                saved_image = save_image(stitched_image, stitched_image_name, directory_path)
                if saved_image:
                    generate_statistics(stitched_image_name, directory_path, False)
                user_done = input('Exit? (Y/N)\n').upper()
                if user_done == 'Y':
                    always = False