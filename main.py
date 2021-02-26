import cv2
import json
import os

directory = 'imgs'
global orig_img
global img
global cache
global points_list

#define the events for the mouse_click
def mouse_click(event, x, y, flags, param):
    global orig_img
    global cache
    global points_list
    height, width, channels = cache.shape

    # to check if left mouse button was clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        #img = cache.copy()

        # font for left click event
        LB = 'Left Button'

        # draw cirlce for joint annotation:
        # Center coordinates
        center_coordinates = (x, y)

        # Radius of circle
        radius = 7

        # Blue color in BGR
        color = (0, 0, 255)

        # Line thickness of 2 px
        thickness = -1

        # Draw a blue cirlce on image and Normalize Coordinates(0, 1)
        cv2.circle(cache, center_coordinates, radius, color, thickness)     
        cv2.imshow('main_window', cache)
        normalized_center_coordinates = (center_coordinates[0]/width, center_coordinates[1]/height)
        points_list.append(normalized_center_coordinates)

    
    # to check if right mouse button was clicked
    if event == cv2.EVENT_RBUTTONDOWN:
        pass


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
i = len(file_list)
print(i)
first_read = True
while i > 0:
    global orig_img
    global cache
    if first_read:
        print('first read')
        points_list = list()

        # read image 
        orig_img = cv2.imread(img_path_list[-i])

        height, width, channels = orig_img.shape

        #print(height, width)

        # Resize image 
        #img = cv2.resize(img, (960, 550))
        orig_img = cv2.resize(orig_img, (0,0), fx=0.3, fy=0.3)
        
        cache = orig_img.copy()
        
        # show image and set Mouse Callback
        cv2.imshow('main_window', cache)
        cv2.setMouseCallback('main_window', mouse_click)
        first_read = False

    
    else:
        cv2.imshow('main_window', cache)
        print('not first read')
        cv2.setMouseCallback('main_window', mouse_click)

    key = cv2.waitKey(0)

    ### ASCII Table can be found at: asciitable.com ###
    # If "p" is pressed - undo last annotation
    if key == 101:
        cache = orig_img.copy()
        #cv2.destroyAllWindows()
        print("p was pressed")
        if points_list != []:
            points_list.pop()
    
        for point in points_list:
            height, width, channels = cache.shape
            print(point)
            # Radius of circle
            radius = 7

            # Blue color in BGR
            color = (0, 0, 255)

            # Line thickness of 2 px
            thickness = -1
            center_coordinates = (int(point[0]*width), int(point[1]*height))
            print(center_coordinates)
            
            cv2.circle(cache, center_coordinates, radius, color, thickness)     
            
            cv2.imshow('main_window', cache)
            
              

    # If spacebar is pressed - Skip Joint
    # if key == 32:
    #     img_2 = orig_img.copy()
    #     height, width, channels = img_2.shape
    #     img_2 = cv2.resize(img_2, (0, 0), fx=0.3, fy=0.3)
        
    #     print('space')
    #     print(points_list)
    #     if points_list != []:
    #         print(points_list.pop())
    #     print(points_list)
    #     for point in points_list:
    #         print(point)
    #         # Radius of circle
    #         radius = 7

    #         # Blue color in BGR
    #         color = (0, 255, 0)

    #         # Line thickness of 2 px
    #         thickness = -1
    #         center_coordinates = (int(point[0]*width), int(point[1]*height))
    #         cv2.circle(img_2, center_coordinates, radius, color, thickness)
    #         cv2.imshow('main_window', img_2)     
        


    # If Enter key is pressed - Next Image
    elif key == 13:
        # Create Key Point Dictionary and Write JSON file
        key_pts = dict()
        for idx, point in enumerate(points_list):
            key_pts[idx] = point
        
        with open('results/' + '{}'.format(file_list[-i]) + '.json', 'w', encoding='utf-8') as f:
            json.dump(key_pts, f, ensure_ascii=False, indent=4)
            f.close()

        # Continue on to next image
        i -= 1
        first_read = True
        #continue

    # If backspace is pressed - Previous Image
    # elif key == 8:
    #     print('backspace mf')
    #     cv2.setMouseCallback('main_window', mouse_click)

    # if escape key is pressed - Exit Program
    elif key == 27:
        break


# close all the opened windows
cv2.destroyAllWindows()

print(key_pts)