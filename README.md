# objecttracking-test

## Installation

Python version 3.9

    pip install opencv-contrib-python
    pip install numpy

## Run

    python multi_object_tracking.py --tracker <TRACKERTYPE> --video <PATH TO VIDEOFILE>

Options for --tracker are: ['MIL','TLD', 'MEDIANFLOW','MOSSE', 'CSRT']. MEDIANFLOW is the only one that can run more or less in realtime for multiple objects, this one will be used by default.

Add '--output' to save to videofile instead of displaying capture.


1. Select bounding box of first object & press **ENTER**
2. Press **q** to stop selecting and start video. Press any other key to select another bounding box.



