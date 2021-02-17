import cv2
import json
import os

directory = 'imgs'

#define the events for the mouse_click
def mouse_click(event, x, y, flags, param):
    height, width, channels = img.shape

    # to check if left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        
        # font for left click event
        LB = 'Left Button'

        # draw cirlce for joint annotation:
        # Center coordinates
        center_coordinates = (x, y)

        # Radius of circle
        radius = 7

        # Blue color in BGR
        color = (255, 0, 0)

        # Line thickness of 2 px
        thickness = -1

        # Draw a blue cirlce on image and Normalize Coordinates(0, 1)
        cv2.circle(img, center_coordinates, radius, color, thickness)     
        cv2.imshow('main_window', img)
        normalized_center_coordinates = (center_coordinates[0]/width, center_coordinates[1]/height)
        points_list.append(normalized_center_coordinates)

    
    # to check if right mouse button was clicked
    if event == cv2.EVENT_RBUTTONDOWN:
    
    	# font for right click event 
    	font = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX 
    	RB = 'Right Button'
    
    	# display that right button was clicked
    	cv2.putText(img, RB, (x, y),
    				font, 1, 
    				(0, 255, 255), 
    				2)
    	cv2.imshow('main_window', img)


# Create list with path/to/image and file names
img_path_list = list()
file_list = list()

for filename in os.listdir(directory):
    if filename.endswith(".jpg") or filename.endswith(".jpeg"):
        file_root = filename.split(sep='.')
        file_list.append(file_root[0])
        img_path_list.append(os.path.join(directory, filename))
        print(os.path.join(directory, filename))
        
    else:
        continue

# Annotate, Iterate through each image, and write results
i = len(os.listdir(directory))
print(i)
while i > 0:
    points_list = list()
    print(i)
    # read image 
    img = cv2.imread(img_path_list[-i])

    height, width, channels = img.shape

    print(height, width)

    # Resize image 
    #img = cv2.resize(img, (960, 550))
    img = cv2.resize(img, (0,0), fx=0.3, fy=0.3)

    # show image and set Mouse Callback
    cv2.imshow('main_window', img)
    cv2.setMouseCallback('main_window', mouse_click)
    cv2.waitKey(0)

    # Create Key Point Dictionary and Write JSON file
    key_pts = dict()
    for idx, point in enumerate(points_list):
        key_pts[idx] = point
    
    with open('results/' + '{}'.format(file_list[-i]) + '.json', 'w', encoding='utf-8') as f:
        json.dump(key_pts, f, ensure_ascii=False, indent=4)
        f.close()

    i -= 1

# close all the opened windows
cv2.destroyAllWindows()

print(key_pts)