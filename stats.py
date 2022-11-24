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
    print(f'Generating statistics of {image_name}...')

    processed_image_data = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    plt.imshow(processed_image_data, cmap="gray")  # display the image requested
    plt.title(image_name)
    plt.grid(True, color='black')
    plt.show()

    defect_pixel_counter = np.sum(processed_image_data == 0)  # counts number of defect pixels in image
    pixel_counter = sum(len(row) for row in processed_image_data)  # counts total number of pixels in image
    pct_defect_pixels = defect_pixel_counter / pixel_counter * 100  # calculates percentage of defect pixels

    # Generates pixel array based on a threshold value
    th, threshed = cv2.threshold(processed_image_data, 225, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)

    # Connects defects together in order to count them
    counts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[-2]

    min_defect_size = 10  # minimum defect size (may need to change this value)
    max_defect_size = 100000  # maximum defect size (may need to change this value)
    defects = []  # array to hold all defects

    # Appends all defects based on size constraints into array
    for count in counts:
        if min_defect_size < cv2.contourArea(count) < max_defect_size:
            defects.append(count)

    # TODO: Calculate biggest defect size and locations of each defect
    # print(defects)
    # max_area = 0
    #
    # for defect in defects:
    #     if defect.any() > max_area:
    #         max_area = defect

    # Prints all relevant statistics onto console
    print(f'Number of pixels in image: {pixel_counter}')
    print(f'Number of defect pixels in image: {defect_pixel_counter}')
    print(f'Percentage of defect pixels in image: {round(pct_defect_pixels, 2)}%')
    print(f'Number of defects in image: {len(defects)}')
    # print(f'Biggest defect area in image (in pixels): {max_area}')


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

# Old code that may be useful in the future

# def get_adjacent_defect_pixels(row, column, num_rows, num_columns, defect_pixel_marker, adjacent_defect_pixels):
#     if row > 0 and defect_pixel_marker[row - 1][column] == 0:
#         defect_pixel_marker[row - 1][column] = 1
#         adjacent_defect_pixels.append([row - 1, column])
#     if row + 1 < num_rows and defect_pixel_marker[row + 1][column] == 0:
#         defect_pixel_marker[row + 1][column] = 1
#         adjacent_defect_pixels.append([row + 1, column])
#     if column > 0 and defect_pixel_marker[row][column - 1] == 0:
#         defect_pixel_marker[row][column - 1] = 1
#         adjacent_defect_pixels.append([row, column - 1])
#     if column + 1 < num_columns and defect_pixel_marker[row][column + 1] == 0:
#         defect_pixel_marker[row][column + 1] = 1
#         adjacent_defect_pixels.append([row, column + 1])
#
#     adjacent_defect_pixels.pop(0)
#
#     if defect_pixel_marker.count() == 0:
#         return
#     else:
#         for [row, column] in adjacent_defect_pixels:
#             get_adjacent_defect_pixels(row, column, num_rows, num_columns,
#                                        defect_pixel_marker, adjacent_defect_pixels)

# numrows = len(processed_image_data)
    # numcolumns = len(processed_image_data[0])

    # defect_pixel_marker = [[0] * numrows for _ in range(numcolumns)]  # defect pixel marked (0 is hasn't seen before,
    # 1 is has seen and is defect)
# defect_counter = 0

    # for row in processed_image_data:
    #     for column in row:
    #         if (processed_image_data[row][column] == 0).all() and defect_pixel_marker[row][column] == 0:
    #             defect_pixel_marker[row][column] = 1
    #
    #             adjacent_defect_pixels = []
    #             get_adjacent_defect_pixels(row, column, numrows, numcolumns,
    #                                                                 defect_pixel_marker, adjacent_defect_pixels)
    #             defect_counter += 1
    #             if defect_counter == 1:
    #                 break
    #
    # print(f'Number of defects in image: {defect_counter}')