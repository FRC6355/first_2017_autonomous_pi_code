#!/usr/bin/python3

"""
Sample program that uses a generated GRIP pipeline to detect red areas in an image and publish them to NetworkTables.
"""

import cv2
from networktables import NetworkTables
from grip import GripPipeline


def extra_processing(pipeline):
    """
    Performs extra processing on the pipeline's outputs and publishes data to NetworkTables.
    :param pipeline: the pipeline that just processed an image
    :return: None
    """
    center_x_positions = []
    center_y_positions = []
    widths = []
    heights = []

    # Find the bounding boxes of the contours to get x, y, width, and height
    for contour in pipeline.filter_contours_output:
        x, y, w, h = cv2.boundingRect(contour)
        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(h)


    #print(center_x_positions)
    print(widths)

    



    # Publish to the '/vision/red_areas' network table
    table = NetworkTables.getTable('/vision/gear')
    table.putNumberArray('x', center_x_positions)
    table.putNumberArray('y', center_y_positions)
    table.putNumberArray('width', widths)
    table.putNumberArray('height', heights)

import sys

def main():
    if len(sys.argv) != 2:
        print("Error: specify an IP to connect to!")
        exit(0)

    ip = sys.argv[1]
    
    print(ip)


    print('Initializing NetworkTables')
    NetworkTables.setClientMode()
    #NetworkTables.setIPAddress('roboRIO-6355-FRC')
    NetworkTables.setTeam(6355)
    # NetworkTables.initialize()
    NetworkTables.initialize(server=ip)

    print('Creating video capture')
    cap = cv2.VideoCapture(0)

    print('Creating pipeline')
    pipeline = GripPipeline()

    print('Running pipeline')
    while cap.isOpened():
        have_frame, frame = cap.read()
        if have_frame:
            print('have frame')
            cv2.imshow('Unprocessed',cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY))
            cv2.waitKey()
            pipeline.process(frame)
            extra_processing(pipeline)

    print('Capture closed')


if __name__ == '__main__':
    main()
