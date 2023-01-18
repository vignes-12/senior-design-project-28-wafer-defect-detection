import os
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np

print("Welcome to the wafer image defect statistical generator!")

LENS_SIZES = ["5X", "10X", "20X"]
PROCESSED_DATADIR = "C:/senior-design/dataset/processed"

always = True


def generate_statistics():
    print(f'\nGenerating statistics of {image_name}...\n')

    processed_image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    plt.imshow(processed_image_data, cmap="gray")  # display the image requested
    plt.title(image_name)
    plt.grid(True, color='black')
    plt.show()

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

    defect_pixel_counter_array = np.sum(processed_image_data == 0)  # counts number of defect pixels in image in array
    pixel_counter = sum(len(row) for row in processed_image_data)  # counts total number of pixels in image
    # calculates percentage of defect pixels in array and contour respectively
    pct_defect_pixels_array = round(defect_pixel_counter_array / pixel_counter * 100, 2)
    pct_defect_pixels_contour = round(defect_pixel_counter_contour / pixel_counter * 100, 2)
    # calculates percent error between counting in array and contours
    pct_error_in_defect_pixels = round(abs(defect_pixel_counter_contour - defect_pixel_counter_array) / \
                                       defect_pixel_counter_array * 100, 2)
    number_of_defects = len(defects)  # counts number of defects in image
    smallest_defect_size = round(min(defect_sizes))  # gets smallest defect size
    largest_defect_size = round(max(defect_sizes))  # gets largest defect size

    # Calculates the x and y coordinates for all defects
    for defect in defects:
        median_x_coordinate = round(sum(pixel[0][0] for pixel in defect) / len(defect))
        median_y_coordinate = round(sum(pixel[0][1] for pixel in defect) / len(defect))
        defect_coors.append([median_x_coordinate, median_y_coordinate])

    # Converts the sizes and coordinates to NumPy arrays for sorting
    defect_sizes_nparray = np.array(defect_sizes)
    defect_coors_nparray = np.array(defect_coors)

    sort = np.argsort(defect_sizes_nparray)  # sorts the arrays according to the defect sizes

    # Sorts the sizes and coordinates from largest to smallest size
    defect_pixel_array_sorted = defect_sizes_nparray[sort][::-1]
    defect_coors_sorted = defect_coors_nparray[sort][::-1]

    # Prints all relevant statistics below
    print(f'Number of pixels in image: {pixel_counter}')
    print(f'Number of defect pixels in image (in array itself): {defect_pixel_counter_array}')
    print(f'Number of defect pixels in image (using contours): {defect_pixel_counter_contour}')
    print(
        f'Percent error between defect pixels in array and contours: {pct_error_in_defect_pixels}%')
    print(f'Percentage of defect pixels in image (in array itself): {pct_defect_pixels_array}%')
    print(f'Percentage of defect pixels in image (using contours): {pct_defect_pixels_contour}%')
    print(f'Number of defects in image: {number_of_defects}')
    print('Coordinates and sizes for all defects (from largest to smallest):')
    for i in range(len(defect_pixel_array_sorted)):
        print(f'#{i + 1}: Defect at location {defect_coors_sorted[i]} with size of {defect_pixel_array_sorted[i]}')
    print(f'Largest defect size (in pixels): {largest_defect_size}')
    print(f'Smallest defect size (in pixels): {smallest_defect_size}')


# This controls what image to generate statistics of based on user input.
while always:
    magnification = input("What image magnification would you like to see statistics of? (5X, 10X, 20X)\n").upper()
    if magnification in LENS_SIZES:
        print(f'You entered a magnification of {magnification}.')
        lens_path = os.path.join(PROCESSED_DATADIR, magnification)
        image_name = input('What image would you like to generate statistics of?\n').upper()
        image_path = os.path.join(lens_path, image_name)
        if os.path.exists(image_path):
            start_time = time.time()  # Calculates time of statistical analysis and displays it to console
            generate_statistics()
            end_time = time.time()
            print(f'Total time: {round(end_time - start_time, 2)} seconds')
            user_done = input('Exit? (Y/N)\n').upper()
            if user_done == 'Y':
                always = False
        else:
            print('That is an invalid image name.\n')
    else:
        print('That is an invalid magnification size.\n')
