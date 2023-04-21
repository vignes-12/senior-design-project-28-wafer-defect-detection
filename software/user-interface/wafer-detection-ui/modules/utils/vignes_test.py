import csv
import numpy as np
import os
import cv2
import time
from PIL import Image
import re

REPO_DIR = "C:\Project-28-Error-Detection-on-Wafer-Surfaces"

#IMG_DIR = "software/user-interface/processed-stitched-snake/getSnapshot"

CLEAN_IMG_SRC = "software/user-interface/processed-stitched-snake/getSnapshot/35.jpeg"

CSV_NAME = "auto_run.csv"

class processor(object):

    def process_image(self, image_path):
        clean_img_array = cv2.imread(os.path.join(REPO_DIR, CLEAN_IMG_SRC), cv2.IMREAD_GRAYSCALE)
        def_img_array = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        processed_img_array = cv2.subtract(clean_img_array, def_img_array)
        processed_img_array = cv2.bitwise_not(processed_img_array)
        (thresh, processed) = cv2.threshold(processed_img_array, 213, 255, cv2.THRESH_BINARY)
        # processed = cv2.rotate(processed, cv2.ROTATE_180)
        return processed

    def stitch_images(self, processed_images, x_steps, y_steps):
        first_time_stitching = True
        # temp = x_steps
        # x_steps = y_steps
        # y_steps = temp

        row_counter = 0  # row counter
        column_counter = 0  # column counter
        total_counter = 0  # total images stitched counter
        x_pixels = 0  # pixel dimension for x-axis
        y_pixels = 0  # pixel dimension for y-axis

        stitched_image = Image

        for processed_image in processed_images:
            # time.sleep(1)
            stitch_image = Image.fromarray(processed_image)
            if first_time_stitching:
                x_pixels = stitch_image.size[0]
                y_pixels = stitch_image.size[1]
                stitched_image = Image.new("RGB", (x_pixels * x_steps, y_pixels * y_steps))
                first_time_stitching = False
                # column_counter = y_steps
                
                # row_counter = x_steps

            if row_counter % 2 == 0 and column_counter < x_steps:  # if row number is even,  then we are moving right
                # print(f'{total_counter} : ({row_counter}, {column_counter})')
                stitched_image.paste(stitch_image, (column_counter * x_pixels, row_counter * y_pixels))  # stitch the image
                column_counter += 1
                total_counter += 1
                if column_counter == x_steps:  # if we are finished stitching that row, then increment row counter
                    row_counter += 1

            elif row_counter % 2 == 1 and column_counter > 0:  # else if the row number is odd, then we are moving left
                column_counter -= 1
                total_counter += 1
                # print(f'{total_counter} : ({row_counter}, {column_counter})')
                stitched_image.paste(stitch_image, (column_counter * x_pixels, row_counter * y_pixels))  # stitch the image
                # column_counter += 1  # decrement the column counter
                if column_counter == 0:  # if we are finished stitching that row, then increment row counter
                    row_counter += 1

        return stitched_image





    def get_coordinates(self, coordinates, image):

        mask = np.zeros_like(image)

        cv2.drawContours(mask, [coordinates], 0, 255, -1)

        points = np.where(mask == 255)

        points = np.column_stack((points[1], points[0]))

        return points



    def final_output_path(self, output_path):

        # output_data_dupe_path = ""



        # is_output_dupe = False  # Flag for checking if output is a duplicate copy



        # if os.path.exists(output_path + ".csv"):  # If the file exists, increment a counter to find a file that

        #     is_output_dupe = True  # does not exist

        #     counter = 1

        #     output_data_dupe_path = (output_path + "_{}").format(str(counter))

        #     while os.path.exists(output_data_dupe_path + ".csv"):

        #         counter += 1

        #         output_data_dupe_path = (output_path + "_{}").format(str(counter))



        # if not is_output_dupe:  # Gets the name for the file

        #     final_output_data_path = output_path + ".csv"

        # else:

        #     final_output_data_path = output_data_dupe_path + ".csv"



       #  return final_output_data_path
       return output_path + ".csv"



    def generate_statistics(self, directory_path, image_name):

        jpeg_images_src = os.path.join(REPO_DIR, self.IMG_DIR)



        with open(os.path.join(jpeg_images_src, CSV_NAME)) as csvfile:

            reader = csv.reader(csvfile, delimiter=",")

            row = next(reader)

            x_start = int(row[0])

            y_start = int(row[1])

            x_steps = int(row[2])

            y_steps = int(row[3])

            total_images = int(row[4])

            x_fov = float(row[5])
            y_fov = float(row[6])



        image_path = os.path.join(directory_path, image_name + ".jpeg")



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

        counts = cv2.findContours(threshed, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[-2]



        min_defect_size = 400  # minimum defect size (may need to change this value)

        max_defect_size = 100000  # maximum defect size (may need to change this value)

        defects = []  # array to hold all defects

        defect_pixel_counter_contour = 0  # counts number of defect pixels in image using contours

        defect_sizes_mm = []  # holds all defect sizes in mms
        defect_sizes_pixels = []

        defect_coors_mm = []  # holds all coordinates of defects
        defect_coors_pixels = []

        x_mm = x_steps * x_fov
        y_mm = y_steps * y_fov
        x_ratio = x_mm / x_length
        y_ratio = y_mm / y_length

        pixel_ratio = x_length * y_length / (x_fov * y_fov)

        # For each defect based on the minimum and maximum defect size constraints, calculate the number of defects,

        # the number of total defect pixels and the minimum and maximum defect size

        for count in counts:

            defect_pixels = round(cv2.contourArea(count))

            if min_defect_size < defect_pixels < max_defect_size:

                defect_sizes_pixels.append(defect_pixels)

                defect_sizes_mm.append(defect_pixels / pixel_ratio)

                defect_pixel_counter_contour += defect_pixels

                count = self.get_coordinates(count, processed_image_data)

                defects.append(count)



        # calculates percent error between counting in array and contours

        number_of_defects = len(defects)  # counts number of defects in image

        # smallest_defect_size = round(min(defect_sizes))  # gets smallest defect size

        # largest_defect_size = round(max(defect_sizes))  # gets largest defect size



        # defect_coors_and_size = []

        all_defect_coors = []



        # Calculates the x and y coordinates for all defects

        for defect in defects:

            median_x_coordinate = round(sum(pixel[0] for pixel in defect) / len(defect))

            median_y_coordinate = round(sum(pixel[1] for pixel in defect) / len(defect))

            defect_coors_pixels.append([median_x_coordinate, median_y_coordinate])

            defect_coors_mm.append([median_x_coordinate * x_ratio, median_y_coordinate * y_ratio])

            for pixel in defect:
                # pixel_mm = [pixel[0] * x_ratio, pixel[1] * y_ratio]
                new_pixel = np.append(pixel, "BAD")
                all_defect_coors.append(new_pixel)



        # Converts the sizes and coordinates to NumPy arrays for sorting

        defect_sizes_mm_nparray = np.array(defect_sizes_mm)
        defect_sizes_pixels_nparray = np.array(defect_sizes_pixels)

        defect_coors_mm_nparray = np.array(defect_coors_mm)
        defect_coors_pixels_nparray = np.array(defect_coors_pixels)



        sort_mm = np.argsort(defect_sizes_mm_nparray)  # sorts the arrays according to the defect sizes
        sort_pixels = np.argsort(defect_sizes_pixels_nparray)
        # Sorts the sizes and coordinates from largest to smallest size

        defect_pixel_mm_array_sorted = defect_sizes_mm_nparray[sort_mm][::-1]
        defect_pixel_array_sorted = defect_sizes_pixels_nparray[sort_pixels][::-1]

        defect_coors_mm_sorted = defect_coors_mm_nparray[sort_mm][::-1]
        defect_coors_pixels_sorted = defect_coors_pixels_nparray[sort_mm][::-1]


        defect_coors_and_size_mm = np.hstack((defect_coors_mm_sorted, np.atleast_2d(defect_pixel_mm_array_sorted).T))
        defect_coors_and_size_pixels = np.hstack((defect_coors_pixels_sorted, np.atleast_2d(defect_pixel_array_sorted).T))


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

        csv_all_def_coor_headers = ['x', 'y', 'OK']

        csv_overall_headers = ['X', 'Y', '#']

        overall_stats_mm = [str(x_mm), str(y_mm), str(number_of_defects)]
        overall_stats_pixels = [str(x_length), str(y_length), str(number_of_defects)]



        # Gets the output data path

        # output_path = os.path.join(DATASET_DATADIR, "output-data")

        # output_path_with_mag = os.path.join(output_path, magnification)



        output_data_path_mm = os.path.join(directory_path, image_name + "(def_center_and_size_mm)")
        output_data_path_pixels = os.path.join(directory_path, image_name + "(def_center_and_size_pixels")

        output_data_path_coors_pixels = os.path.join(directory_path, image_name + "(all_def_coor)")


        final_output_data_path_coors = self.final_output_path(output_data_path_coors_pixels)



        # print("\nStoring data in output file: '" + final_output_data_path + "'...\n")



        with open(final_output_data_path_coors, 'w+') as csvfile:  # Writes the headers and statistics to the file

            csvwriter = csv.writer(csvfile, delimiter=',')

            csvwriter.writerow(csv_overall_headers)

            csvwriter.writerow(overall_stats_pixels)

            csvwriter.writerow(csv_all_def_coor_headers)

            csvwriter.writerows(all_defect_coors)



        final_output_data_path_mm = self.final_output_path(output_data_path_mm)



        # print("\nStoring data in output file: '" + final_output_data_path + "'...\n")



        with open(final_output_data_path_mm, 'w+') as csvfile:  # Writes the headers and statistics to the file

            csvwriter = csv.writer(csvfile, delimiter=',')

            csvwriter.writerow(csv_defect_headers)

            csvwriter.writerows(defect_coors_and_size_mm)

        final_output_data_path_pixels = self.final_output_path(output_data_path_pixels)

        with open(final_output_data_path_pixels, 'w+') as csvfile:

            csvwriter = csv.writer(csvfile, delimiter=',')

            csvwriter.writerow(csv_defect_headers)

            csvwriter.writerows(defect_coors_and_size_pixels)



        return final_output_data_path_coors, final_output_data_path_mm, final_output_data_path_pixels





    def process_data(self):

        jpeg_images_src = os.path.join(REPO_DIR, self.IMG_DIR)



        with open(os.path.join(jpeg_images_src, CSV_NAME)) as csvfile:

            reader = csv.reader(csvfile, delimiter=",")

            row = next(reader)

            x_start = int(row[0])

            y_start = int(row[1])

            x_steps = int(row[2])

            y_steps = int(row[3])

            total_images = int(row[4])

            x_fov = float(row[5])
            y_fov = float(row[6])

            # x_start, y_start, x_steps, y_steps, total_images, fov = row



        jpeg_images = list(filter(lambda x: x.endswith('.jpeg') and x[:-5].isdigit(), os.listdir(jpeg_images_src)))

        # jpeg_images = [f for f in os.listdir(jpeg_images_src) if

        #                (f.endswith('.jpeg') or f.endswith('.jpg')) and isinstance(f[:-5], int)]

        jpeg_images = sorted(jpeg_images, key=lambda x: int(x.split('.')[0]), reverse=False)



        processed_images = []

        for jpeg_image in jpeg_images:

            processed_images.append(self.process_image(os.path.join(jpeg_images_src, jpeg_image)))



        # print(len(processed_images))

        # cv2.imwrite(os.path.join(jpeg_images_src, "test.png"), processed_images[2])



        stitched_image = self.stitch_images(processed_images, x_steps, y_steps)



        stitched_image.save(os.path.join(jpeg_images_src, "stitched.jpeg"))

        self.generate_statistics(jpeg_images_src, "stitched")