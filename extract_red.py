# -*- coding: utf-8 -*-
"""
Script to perform extraction of red pixels from input video
Requires TEST_VIDEO to be set as path to input .avi
"""

from pathlib import Path
import cv2
import numpy as np
import matplotlib.pyplot as plt

#TEST_VIDEO = path(<PATH_TO_INPUT_AVI_FILE>)

cap = cv2.VideoCapture(str(TEST_VIDEO))
NUMBER_OF_FRAMES = cap.get(cv2.CAP_PROP_FRAME_COUNT)
FRAMERATE = cap.get(cv2.CAP_PROP_FPS )
red_value_array = np.empty(int(NUMBER_OF_FRAMES))
counter = 0

#get the ROI and process the first frame
success, frame = cap.read()

roi = cv2.selectROI("select the area", frame)
cv2.destroyWindow("select the area")

frame_cropped = frame[int(roi[1]):int(roi[1]+roi[3]),
                      int(roi[0]):int(roi[0]+roi[2])]

avg_color_per_row = np.average(frame_cropped, axis=0)
avg_color_red = np.average(avg_color_per_row, axis=0)[2]
red_value_array.flat[0] = avg_color_red

counter = 1

#loop for remaining frames
while (success & (counter < NUMBER_OF_FRAMES)):
    success, frame = cap.read()
    frame_cropped = frame[int(roi[1]):int(roi[1]+roi[3]),
                          int(roi[0]):int(roi[0]+roi[2])]

    avg_color_per_row = np.average(frame_cropped, axis=0)
    avg_color_red = np.average(avg_color_per_row, axis=0)[2]
    red_value_array.flat[counter] = avg_color_red
    counter += 1


if show_seconds:
    time_elapsed = np.arange(NUMBER_OF_FRAMES)/FRAMERATE
    plt.xlabel('Time elapsed (s)')
    plt.plot(time_elapsed, red_value_array)
else:
    plt.xlabel('Frame')
    plt.plot(red_value_array)

plt.show()

index = (red_value_array.max() - red_value_array.min()) / red_value_array.mean()

print(str(TEST_VIDEO).split('/')[-1])
print("min is: " + str(red_value_array.min()))
print("max is: " + str(red_value_array.max()))
print("mean is: " + str(red_value_array.mean()))
print("index is: " + str(index))

