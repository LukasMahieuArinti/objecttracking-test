from __future__ import print_function
import sys
import cv2
from random import randint
import argparse

trackerTypes = ['MIL','TLD', 'MEDIANFLOW','MOSSE', 'CSRT']
parser = argparse.ArgumentParser(description='Multi Object Tracking')
parser.add_argument('--tracker', default='MEDIANFLOW', help='Tracker name')
parser.add_argument('--video', help='Path to video file.')
parser.add_argument('--output', action='store_true', help='Outputs tracking data to a file')
args = parser.parse_args()

def createTrackerByName(trackerType):
  # Create a tracker based on tracker name
  if trackerType == 'MIL':
    tracker = cv2.legacy.TrackerMIL_create()
  elif trackerType == 'TLD':
    tracker = cv2.legacy.TrackerTLD_create()
  elif trackerType == 'MEDIANFLOW':
    tracker = cv2.legacy.TrackerMedianFlow_create()
  elif trackerType == 'MOSSE':
    tracker = cv2.legacy.TrackerMOSSE_create()
  elif trackerType == 'CSRT':
    tracker = cv2.legacy.TrackerCSRT_create()
  else:
    tracker = None
    print('Incorrect tracker name')
    print('Available trackers are:')
    for t in trackerTypes:
      print(t)

  return tracker

# Create a video capture object to read videos

cap = cv2.VideoCapture(args.video)

if args.output:
  width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH) + 0.5)
  height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT) + 0.5)

  # Define the codec and create VideoWriter object
  fourcc = cv2.VideoWriter_fourcc(*"XVID")
  out = cv2.VideoWriter('output.avi', fourcc, 20.0, (width, height))

# Read first frame
success, frame = cap.read()
# quit if unable to read the video file
if not success:
  print('Failed to read video')
  sys.exit(1)
  
## Select boxes
bboxes = []
colors = [] 

# OpenCV's selectROI function doesn't work for selecting multiple objects in Python
# So we will call this function in a loop till we are done selecting all objects
while True:
  # draw bounding boxes over objects
  # selectROI's default behaviour is to draw box starting from the center
  # when fromCenter is set to false, you can draw box starting from top left corner
  bbox = cv2.selectROI('MultiTracker', frame)
  bboxes.append(bbox)
  colors.append((randint(0, 255), randint(0, 255), randint(0, 255)))
  print("Press q to quit selecting boxes and start tracking")
  print("Press any other key to select next object")
  k = cv2.waitKey(0) & 0xFF
  if (k == 113):  # q is pressed
    break

print('Selected bounding boxes {}'.format(bboxes))
if args.output:
  print('Saving output to file...')

# Specify the tracker type
trackerType = "MEDIANFLOW"

# Create MultiTracker object
multiTracker = cv2.legacy.MultiTracker_create()

# Initialize MultiTracker
for bbox in bboxes:
  multiTracker.add(createTrackerByName(args.tracker), frame, bbox)
  
# Process video and track objects
while cap.isOpened():
  success, frame = cap.read()
  if not success:
    break

  # get updated location of objects in subsequent frames
  success, boxes = multiTracker.update(frame)

  # draw tracked objects
  for i, newbox in enumerate(boxes):
    p1 = (int(newbox[0]), int(newbox[1]))
    p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
    cv2.rectangle(frame, p1, p2, colors[i], 2, 1)

  # output the frame
  if args.output:
    out.write(frame)
  
  # show frame
  cv2.imshow('MultiTracker', frame)

  # quit on ESC button
  if cv2.waitKey(1) & 0xFF == 27:  # Esc pressed
    break
  
# Close the window / Release webcam
cap.release()

# After we release our webcam, we also release the output
if args.output:
  out.release()
  
# De-allocate any associated memory usage 
cv2.destroyAllWindows()