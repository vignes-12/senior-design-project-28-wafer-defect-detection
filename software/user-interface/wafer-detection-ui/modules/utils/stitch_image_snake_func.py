import csv
import numpy as np
import os
import cv2
from PIL import Image
# from matplotlib import pyplot as plt

# print("Welcome to the stitch wafer image algorithm!")

# DATADIR = "C:\senior-design\software\data-processing\dataset\processed-stitched-snake"
# always = True


def stitch_images_snake(directory_path, folder_name, image_name, x, y):
    """
    Stitches images in a snake pattern (assumes all images are of the same dimension)
    :param directory_path: path to directory that contains folders of images and CSV files
    :param folder_name: name of new folder containing all images to be stitched
    :param image_name: name of stitched image
    :param x: How many images wide the final image will be
    :param y: How many images long the final image will be
    :return: Stitched image
    """

    image_directory_path = os.path.join(directory_path, folder_name)
    if not os.path.exists(image_directory_path):
        os.mkdir(image_directory_path)

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
        all_images = os.listdir(image_directory_path)  # get all image names
        new_image_name = [x for x in all_images if x not in known_images]  # find new image
        if len(new_image_name) == 1:  # if there is a new image
            image_stitch_needed = True  # set the flag true

        if image_stitch_needed:  # if there are new images that need to be stitched
            # print(f"New image #{total_counter + 1} " + new_image_name[0] + " found. Stitching it now...")
            known_images.append(new_image_name[0])  # append the new image to known images
            new_image = Image.open(os.path.join(image_directory_path, new_image_name[0]))  # open the image

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

    saved_image = save_image(result_image, image_name, image_directory_path)
    if saved_image:
        generate_statistics(image_name, image_directory_path, True)


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
        # print(f'There are {counter} duplicate image(s) with the same name already saved. Renaming to '
        #       f'{(image_name + "_{}.jpg").format(str(counter))}')
        final_image_save_path = image_save_dupe_path + ".jpg"

    image.save(final_image_save_path)

    processed_image_data = cv2.imread(final_image_save_path)

    # plt.imshow(processed_image_data, cmap="gray")  # display the image requested
    # plt.grid(True, color='black')
    # plt.show()

    return True

def generate_statistics(image_name, directory_path, all_def_coor):
    """
    Generates and displays relevant statistics of a user-inputted image.
    :param all_def_coor: Flag to show all defective coordinates or the center of all defects
    :return: Nothing
    """

    # print(f'\nGenerating statistics of {image_name}...\n')

    image_path = os.path.join(directory_path, image_name + ".jpg")

    processed_image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # plt.imshow(processed_image_data, cmap="gray")  # display the image requested
    # plt.title(image_name)
    # plt.grid(True, color='black')
    # plt.show()

    y_length = len(processed_image_data)
    x_length = len(processed_image_data[0])

    # Generates pixel array based on a threshold value
    th, threshed = cv2.threshold(processed_image_data, 225, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Connects defects together to form contours in order to count them
    counts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

    min_defect_size = 20  # minimum defect size (may need to change this value)
    max_defect_size = 100000  # maximum defect size (may need to change this value)
    defects = []  # array to hold all defects
    defect_pixel_counter_contour = 0  # counts number of defect pixels in image using contours
    defect_sizes = []  # holds all defect sizes in pixels
    defect_coors = []  # holds all coordinates of defects

    # For each defect based on the minimum and maximum defect size constraints, calculate the number of defects,
    # the number of total defect pixels and the minimum and maximum defect size
    for count in counts:
        defect_pixels = round(cv2.contourArea(count))
        if min_defect_size < defect_pixels < max_defect_size:
            defect_sizes.append(defect_pixels)
            defect_pixel_counter_contour += defect_pixels
            defects.append(count)

    # calculates percent error between counting in array and contours
    number_of_defects = len(defects)  # counts number of defects in image
    smallest_defect_size = round(min(defect_sizes))  # gets smallest defect size
    largest_defect_size = round(max(defect_sizes))  # gets largest defect size

    defect_coors_and_size = []

    # Calculates the x and y coordinates for all defects
    for defect in defects:
        median_x_coordinate = round(sum(pixel[0][0] for pixel in defect) / len(defect))
        median_y_coordinate = round(sum(pixel[0][1] for pixel in defect) / len(defect))
        defect_coors.append([median_x_coordinate, median_y_coordinate])
        if all_def_coor:
            for pixel in defect:
                defect_coors_and_size.append(pixel)

    # Converts the sizes and coordinates to NumPy arrays for sorting
    defect_sizes_nparray = np.array(defect_sizes)
    defect_coors_nparray = np.array(defect_coors)

    sort = np.argsort(defect_sizes_nparray)  # sorts the arrays according to the defect sizes

    # Sorts the sizes and coordinates from largest to smallest size
    defect_pixel_array_sorted = defect_sizes_nparray[sort][::-1]
    defect_coors_sorted = defect_coors_nparray[sort][::-1]

    if not all_def_coor:
        defect_coors_and_size = np.hstack((defect_coors_sorted,
                                           np.atleast_2d(defect_pixel_array_sorted).T))

    # Prints all relevant statistics below
    # print(f'Length of image: {x_length}')
    # print(f'Width of image: {y_length}')
    # print(f'Number of defects in image: {number_of_defects}')
    # print('Coordinates and sizes for all defects (from largest to smallest):')
    # for i in range(len(defect_pixel_array_sorted)):
    #     print(f'#{i + 1}: Defect at location {defect_coors_sorted[i]} with size of {defect_pixel_array_sorted[i]}')
    # print(f'Largest defect size (in pixels): {largest_defect_size}')
    # print(f'Smallest defect size (in pixels): {smallest_defect_size}')

    # Outputs data to CSV
    # Headers for CSV file
    csv_defect_headers = ['x', 'y', 'size']
    csv_defect_headers_all_def_coor = ['x', 'y']
    csv_overall_headers = ['X', 'Y', '#']
    overall_stats = [str(x_length), str(y_length), str(number_of_defects)]

    # Gets the output data path
    # output_path = os.path.join(DATASET_DATADIR, "output-data")
    # output_path_with_mag = os.path.join(output_path, magnification)

    if not all_def_coor:
        output_data_path = os.path.join(directory_path, image_name)
    else:
        output_data_path = os.path.join(directory_path, image_name + "(all_def_coor)")

    output_data_dupe_path = ""

    is_output_dupe = False  # Flag for checking if output is a duplicate copy

    if os.path.exists(output_data_path + ".csv"):   # If the file exists, increment a counter to find a file that
        is_output_dupe = True                       # does not exist
        counter = 1
        output_data_dupe_path = (output_data_path + "_{}").format(str(counter))
        while os.path.exists(output_data_dupe_path + ".csv"):
            counter += 1
            output_data_dupe_path = (output_data_path + "_{}").format(str(counter))

    if not is_output_dupe:                          # Gets the name for the file
        final_output_data_path = output_data_path + ".csv"
    else:
        final_output_data_path = output_data_dupe_path + ".csv"

    # print("\nStoring data in output file: '" + final_output_data_path + "'...\n")

    with open(final_output_data_path, 'w') as csvfile:  # Writes the headers and statistics to the file
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(csv_overall_headers)
        csvwriter.writerow(overall_stats)
        if all_def_coor:
            csvwriter.writerow(csv_defect_headers_all_def_coor)
        else:
            csvwriter.writerow(csv_defect_headers)
        csvwriter.writerows(defect_coors_and_size)



# while always:
#     directory_name = input("What directory would you like to store all images for stitching into?").upper()
#     directory_path = os.path.join(DATADIR, directory_name)
#     if not os.path.exists(directory_path):
#         print("Path does not exist. Creating new directory " + directory_name + "...")
#         os.mkdir(directory_path)
#     else:
#         x_images = input("How many images horizontally will the final image be?")
#         if not x_images.isnumeric():
#             print("That is not a valid dimension size. Please try again.")
#             continue
#         else:
#             x_images = int(x_images)
#             y_images = input("How many images vertically will the final image be?")
#             if not y_images.isnumeric():
#                 print("That is not a valid dimension size. Please try again.")
#                 continue
#             else:
#                 y_images = int(y_images)
#                 stitched_image = stitch_images_snake(directory_path, x_images, y_images)
#                 stitched_image_name = input("What would you like to call the final image name?").upper()
#                 saved_image = save_image(stitched_image, stitched_image_name, directory_path)
#                 if saved_image:
#                     generate_statistics(stitched_image_name, directory_path, False)
#                 user_done = input('Exit? (Y/N)\n').upper()
#                 if user_done == 'Y':
#                     always = False
