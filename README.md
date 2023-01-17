# Senior Design Project 28: Error Detection on Wafer Surfaces
This project aims to process a 2D image taken from a microscope (and eventually from a 3D printer design wafer defect
detecting system) in order to find all wafer defects and their corresponding locations. In this repository, there are
two folders, hardware and software, which categorize each aspect of the project and will be described below.

Disclaimer: Out of the five magnifications that wafer images were taken in, preprocessing did not work very well on 50X 
and 100X magnification images, but works as expected on 5X, 10X, and 20X magnifications.

# Repository organization
## Hardware
This folder contains all of the hardware aspects of the senior design project, including driver modifications, embedded
system programming, and more. Currently, there is a zipped file containing the driver used for the 3D printer.

## Software
This folder contains the data-processing folder, which contains the data processing algorithm and all of the images 
captured to test the algorithm. There is also a user-interface folder, which contains the user interface model designed 
for the user to visibly see all wafer defects on a nearby monitor.

### data-processing
#### Dataset
The dataset folder contains all images before and after preprocessing them. The clean directory contains images of a
clean wafer. The defective directory contains all images that were taken without any processing, which are organized by
magnification sizes in subdirectories. The processed directory is similarly organized to the defective directory, but
have all images after processing them.

### Code explanation
The first script, preprocess_images.py, will convert wafer images located in the directory titled
"defective" into a black and white image. This will occur by first converting the image into a grayscale format, 
then removing the gradient and camera lens particles, which you can see in the directory titled "clean", and converting
the image into a black and white format based on a predetermined threshold value. 

The second script, stats.py, will identify all wafer defects on said black and white image and then display 
relevant statistics of the image on the console based on an image name provided by the user. There are currently two
different methods to generate these statistics. One of them is simply by counting the pixels within the array to
identify whether it is a defect or clean. However, this method will not take into account the edges of the defect, since
those are also black but not a wafer defect. To fix that issue, I am using the findContours() method found in the
opencv-python library, which will connect defective pixels together to form singular defects. This method also poses its
own problems, though. Although it does not count edges as actually defective, due to the minimum and maximum size 
limitations that I have given to identify whether a region is considered a defect or not, it tends to create more 
defective pixels in order to smooth defects together, particularly those that are oddly-shaped or joined together.
However, finding contours of an image is definitely a worthwhile means of generating statistics of the image on a 
per-defect basis, such as counting all defects, finding where the coordinates and sizes of all defects are and sorting
them from biggest to largest, and getting the smallest and largest defect size. I will present the pros and cons of 
both methods in three cases of defect images below.

The last script, cnn.py, is currently in work-in-progress. It aims to classify wafer defects based on a neural network
called a Convolutional Neural Network. However, since this is one of the last priorities of the project, this is not
currently in active development; rather, it will be worked on once we are able to generate all relevant statistics
discussed above.

# Future goals of project
Future goals of this project are to stitch images of a single magnification together to create an overall wafer image
before starting to preprocess and generate the statistics of said image.

# Results
# data-processing

Below is an image of a clean wafer, which shows the image distortion coming from the camera lens and color gradient,
as well as three cases of sample wafer defects. Each of the defective images will show the original image, the image 
after preprocessing (with and without a coordinate grid), and the statistics generated of that image. 

## Clean wafer image
![10X_CLEAN](dataset/clean/10X/10X_CLEAN.jpg)

## First case: Center image (less defects)

### Defective wafer before processing image
![OX9 quadrant3 20X take1](dataset/defective/20X/OX9%20quadrant3%2020X%20take1.jpg)

### Defective wafer after processing image (without coordinate grid)
![OX9 quadrant3 20X take1](dataset/processed/20X/OX9%20quadrant3%2020X%20take1.jpg)

### Defective wafer after processing image (with coordinate grid)
![OX9 quadrant3 20X take1](dataset/processed-with-grid/20X/OX9%20quadrant3%2020X%20take1.jpg)

### Console output
```
Welcome to the wafer image defect statistical generator!
What image magnification would you like to see statistics of? (5X, 10X, 20X)
20x
You entered a magnification of 20X.
What image would you like to generate statistics of?
ox9 quadrant3 20x take1.jpg

Generating statistics of OX9 QUADRANT3 20X TAKE1.JPG...

Number of pixels in image: 10017440
Number of defect pixels in image (in array itself): 29166
Number of defect pixels in image (using contours): 29978
Percent error between defect pixels in array and contours: 2.78%
Percentage of defect pixels in image (in array itself): 0.29%
Percentage of defect pixels in image (using contours): 0.3%
Number of defects in image: 4
Coordinates and sizes for all defects (from largest to smallest):
#1: Defect at location [1423  928] with size of 29732
#2: Defect at location [1842  316] with size of 116
#3: Defect at location [1664 1243] with size of 100
#4: Defect at location [2507 1912] with size of 30
Largest defect size (in pixels): 29732
Smallest defect size (in pixels): 30
Total time: 1.63 seconds
Exit? (Y/N)
y
```
## Second case: Center image (more defects)

### Defective wafer before processing image
![5X_PARTICLE6](dataset/defective/5X/5X_PARTICLE6.jpg)

### Defective wafer after processing image
![5X_PARTICLE6](dataset/processed/5X/5X_PARTICLE6.jpg)

### Defective wafer after processing image (with coordinate grid)
![5X_PARTICLE6](dataset/processed-with-grid/5X/5X_PARTICLE6.jpg)

### Console output
```
Welcome to the wafer image defect statistical generator!
What image magnification would you like to see statistics of? (5X, 10X, 20X)
5x
You entered a magnification of 5X.
What image would you like to generate statistics of?
5x_particle6.jpg

Generating statistics of 5X_PARTICLE6.JPG...

Number of pixels in image: 10017440
Number of defect pixels in image (in array itself): 57708
Number of defect pixels in image (using contours): 78532
Percent error between defect pixels in array and contours: 36.09%
Percentage of defect pixels in image (in array itself): 0.58%
Percentage of defect pixels in image (using contours): 0.78%
Number of defects in image: 133
Coordinates and sizes for all defects (from largest to smallest):
#1: Defect at location [ 542 1023] with size of 15294
#2: Defect at location [3202  626] with size of 13450
#3: Defect at location [3197  632] with size of 6063
#4: Defect at location [2524 1166] with size of 4050
#5: Defect at location [2883  856] with size of 3749
#6: Defect at location [2906 2262] with size of 3690
#7: Defect at location [162 853] with size of 3410
#8: Defect at location [ 720 2102] with size of 3190
#9: Defect at location [2162  983] with size of 2958
#10: Defect at location [1227 2140] with size of 2628
#11: Defect at location [690 848] with size of 2574
#12: Defect at location [ 73 858] with size of 695
#13: Defect at location [2081  929] with size of 684
#14: Defect at location [2162  983] with size of 671
#15: Defect at location [1127 1402] with size of 658
#16: Defect at location [530 853] with size of 646
#17: Defect at location [1741  583] with size of 626
#18: Defect at location [1485  849] with size of 476
#19: Defect at location [ 48 802] with size of 456
#20: Defect at location [ 818 1483] with size of 452
#21: Defect at location [1645 1102] with size of 442
#22: Defect at location [ 798 1645] with size of 442
#23: Defect at location [1012 1743] with size of 422
#24: Defect at location [1623  677] with size of 348
#25: Defect at location [1033  763] with size of 343
#26: Defect at location [ 226 1836] with size of 340
#27: Defect at location [1051 1879] with size of 338
#28: Defect at location [725 992] with size of 309
#29: Defect at location [ 797 2625] with size of 286
#30: Defect at location [ 461 1049] with size of 281
#31: Defect at location [3128 1913] with size of 266
#32: Defect at location [3179 2018] with size of 252
#33: Defect at location [1188 1391] with size of 248
#34: Defect at location [3115 2119] with size of 231
#35: Defect at location [837 603] with size of 200
#36: Defect at location [3030 1338] with size of 200
#37: Defect at location [672 754] with size of 197
#38: Defect at location [1043 1763] with size of 191
#39: Defect at location [1624 1927] with size of 190
#40: Defect at location [1176  458] with size of 184
#41: Defect at location [1223  364] with size of 176
#42: Defect at location [ 522 1765] with size of 174
#43: Defect at location [1009 2487] with size of 174
#44: Defect at location [ 356 1638] with size of 157
#45: Defect at location [ 625 2636] with size of 154
#46: Defect at location [1280 1870] with size of 148
#47: Defect at location [1159 1953] with size of 142
#48: Defect at location [437 953] with size of 142
#49: Defect at location [3388 1837] with size of 142
#50: Defect at location [525 816] with size of 140
#51: Defect at location [1038   25] with size of 136
#52: Defect at location [1249 2040] with size of 136
#53: Defect at location [2990  720] with size of 134
#54: Defect at location [1188  828] with size of 130
#55: Defect at location [1363 2485] with size of 129
#56: Defect at location [1303  201] with size of 123
#57: Defect at location [660 321] with size of 116
#58: Defect at location [2905 2025] with size of 107
#59: Defect at location [2687 1039] with size of 106
#60: Defect at location [385 978] with size of 104
#61: Defect at location [ 545 1912] with size of 101
#62: Defect at location [ 838 1531] with size of 98
#63: Defect at location [603 357] with size of 98
#64: Defect at location [1377 1860] with size of 91
#65: Defect at location [1012  413] with size of 91
#66: Defect at location [1006 2523] with size of 88
#67: Defect at location [1596 2130] with size of 87
#68: Defect at location [2320 1167] with size of 86
#69: Defect at location [739 897] with size of 86
#70: Defect at location [ 766 1695] with size of 80
#71: Defect at location [1013 1947] with size of 78
#72: Defect at location [789 448] with size of 77
#73: Defect at location [ 997 1951] with size of 76
#74: Defect at location [1174 1571] with size of 76
#75: Defect at location [3125 2385] with size of 75
#76: Defect at location [2512 1221] with size of 74
#77: Defect at location [1636 1212] with size of 68
#78: Defect at location [416 849] with size of 68
#79: Defect at location [2180  952] with size of 67
#80: Defect at location [1285  210] with size of 66
#81: Defect at location [ 735 2637] with size of 64
#82: Defect at location [ 444 1060] with size of 62
#83: Defect at location [1579   91] with size of 62
#84: Defect at location [ 268 1251] with size of 58
#85: Defect at location [ 939 1971] with size of 58
#86: Defect at location [2163  976] with size of 56
#87: Defect at location [764 823] with size of 56
#88: Defect at location [1306 1575] with size of 54
#89: Defect at location [ 797 2077] with size of 53
#90: Defect at location [ 967 2634] with size of 53
#91: Defect at location [684 319] with size of 52
#92: Defect at location [836 262] with size of 48
#93: Defect at location [1462 2094] with size of 48
#94: Defect at location [899 474] with size of 48
#95: Defect at location [2068   10] with size of 48
#96: Defect at location [470 540] with size of 48
#97: Defect at location [3250 2736] with size of 47
#98: Defect at location [ 317 1814] with size of 46
#99: Defect at location [2697 2468] with size of 46
#100: Defect at location [1062 1865] with size of 46
#101: Defect at location [812 925] with size of 46
#102: Defect at location [2330 1866] with size of 45
#103: Defect at location [764   3] with size of 45
#104: Defect at location [ 101 2174] with size of 39
#105: Defect at location [1434  283] with size of 35
#106: Defect at location [678 438] with size of 35
#107: Defect at location [2321 2514] with size of 35
#108: Defect at location [2219 1497] with size of 32
#109: Defect at location [2268  180] with size of 31
#110: Defect at location [ 413 1171] with size of 30
#111: Defect at location [746 825] with size of 29
#112: Defect at location [1369 1976] with size of 29
#113: Defect at location [594 902] with size of 29
#114: Defect at location [2976 2257] with size of 28
#115: Defect at location [1303 1915] with size of 28
#116: Defect at location [1222  691] with size of 27
#117: Defect at location [1974 2487] with size of 26
#118: Defect at location [ 876 1679] with size of 26
#119: Defect at location [3403 1831] with size of 26
#120: Defect at location [1342 1827] with size of 26
#121: Defect at location [1204 2540] with size of 24
#122: Defect at location [ 817 1727] with size of 24
#123: Defect at location [1152 1645] with size of 24
#124: Defect at location [1261  335] with size of 24
#125: Defect at location [2681  367] with size of 24
#126: Defect at location [1969 1486] with size of 24
#127: Defect at location [ 734 1620] with size of 24
#128: Defect at location [3158 1806] with size of 23
#129: Defect at location [2996  669] with size of 23
#130: Defect at location [899 937] with size of 23
#131: Defect at location [1066  490] with size of 22
#132: Defect at location [394 555] with size of 21
#133: Defect at location [1814  758] with size of 21
Largest defect size (in pixels): 15294
Smallest defect size (in pixels): 21
Total time: 1.9 seconds
Exit? (Y/N)
y
```

## Third case: Edge image

### Defective wafer before processing image
![5X_BOTEDGE.jpg](dataset/defective/5X/5X_BOTEDGE.jpg)

### Defective wafer after processing image
![5X_BOTEDGE.jpg](dataset/processed/5X/5X_BOTEDGE.jpg)

### Defective wafer after processing image (with coordinate grid)
![5X_BOTEDGE.jpg](dataset/processed-with-grid/5X/5X_BOTEDGE.jpg)

### Console output
```
Welcome to the wafer image defect statistical generator!
What image magnification would you like to see statistics of? (5X, 10X, 20X)
5x
You entered a magnification of 5X.
What image would you like to generate statistics of?
5x_botedge.jpg

Generating statistics of 5X_BOTEDGE.JPG...

Number of pixels in image: 10017440
Number of defect pixels in image (in array itself): 4740638
Number of defect pixels in image (using contours): 52875
Percent error between defect pixels in array and contours: 98.88%
Percentage of defect pixels in image (in array itself): 47.32%
Percentage of defect pixels in image (using contours): 0.53%
Number of defects in image: 25
Coordinates and sizes for all defects (from largest to smallest):
#1: Defect at location [1988 1630] with size of 9138
#2: Defect at location [2195 2610] with size of 6916
#3: Defect at location [ 809 2695] with size of 6304
#4: Defect at location [ 832 2249] with size of 5230
#5: Defect at location [ 162 1670] with size of 4444
#6: Defect at location [1492 1944] with size of 4130
#7: Defect at location [ 473 1535] with size of 3970
#8: Defect at location [2574 1348] with size of 3592
#9: Defect at location [ 503 2275] with size of 2204
#10: Defect at location [ 837 2382] with size of 1264
#11: Defect at location [ 895 2678] with size of 792
#12: Defect at location [1281 1342] with size of 686
#13: Defect at location [3568  750] with size of 615
#14: Defect at location [1536 1550] with size of 607
#15: Defect at location [ 118 2166] with size of 443
#16: Defect at location [ 390 1637] with size of 426
#17: Defect at location [ 236 2201] with size of 400
#18: Defect at location [ 814 2492] with size of 350
#19: Defect at location [  66 1677] with size of 334
#20: Defect at location [3403 1335] with size of 316
#21: Defect at location [ 285 2724] with size of 208
#22: Defect at location [ 582 1811] with size of 164
#23: Defect at location [  64 1601] with size of 149
#24: Defect at location [ 858 1464] with size of 114
#25: Defect at location [ 591 1514] with size of 79
Largest defect size (in pixels): 9138
Smallest defect size (in pixels): 79
Total time: 1.71 seconds
Exit? (Y/N)
y
```

## Results Summary
The preprocessing between both images worked fairly well. It was able to grab almost all noticeable defects into a black
and white image. From the image statistics, though, there seems to be a much bigger story to tell. In the first case,
it seems like both methods were comparable in counting defect pixels, since there was only a 2.78% difference in pixel
count. The number of defects is also accurate at 4, as well as their corresponding locations. 

In the second case, though, the two different methods have captured somewhat different data between the number of 
defective pixels in the image. The number of defective pixels in the contour method is about 20,000 more than the 
array method, representing a staggering 36.07% difference between the two methods. Moreover, although it would be a 
massively tedious task to count all defects on the image, I do believe that the contour method is working somewhat 
correctly, as it has detected over 100 different defects. This proves how the contour method does have some flaws 
over the array method in terms of counting defective pixels. 

Finally, the third case shows how useful the contour method can be over the array method. From the image, you can see 
a black bar covering half of the image, which shows that the image was taken near an edge of the wafer. With the array 
method, it will count all pixels that are defective, regardless of edge or not, whereas the contour method will only 
count defective pixels based on the size of the defect itself. Therefore, the contour method's calculation of defective 
pixels, although slightly inaccurate from the previous image, are far more accurate than the array method's calculation 
of defective pixels in this case. Finally, I noticed that calculating all of these statistics took no more than 2 
seconds of processing, even on a heavily defective wafer image such as case 2, proving how efficient 
the contour methods are.




