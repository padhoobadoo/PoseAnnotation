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


# Create list with path/to/image and file names
img_path_list = []
file_list = []

for filename in os.listdir(directory):
    if not filename.endswith(".jpg") and not filename.endswith(".jpeg"):
        continue

    file_root = filename.split(sep='.')
    file_list.append(file_root[0])
    img_path_list.append(os.path.join(directory, filename))
    print(os.path.join(directory, filename))

# Annotate, Iterate through each image, and write results
i = len(file_list)
print(i)
first_read = True
while i > 0:
    global orig_img
    global cache
    if first_read:
        print('first read')
        points_list = []

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

        # Radius of circle
        radius = 7

        # Line thickness of 2 px
        thickness = -1
        for point in points_list:
            height, width, channels = cache.shape
            print(point)
            # Blue color in BGR
            color = (0, 0, 255)

            center_coordinates = (int(point[0]*width), int(point[1]*height))
            print(center_coordinates)

            cv2.circle(cache, center_coordinates, radius, color, thickness)     

            cv2.imshow('main_window', cache)



    elif key == 13:
        key_pts = dict(enumerate(points_list))
        with open(f'results/{file_list[-i]}.json', 'w', encoding='utf-8') as f:
            json.dump(key_pts, f, ensure_ascii=False, indent=4)
            f.close()

        # Continue on to next image
        i -= 1
        first_read = True
            #continue

    elif key == 27:
        break


# close all the opened windows
cv2.destroyAllWindows()

print(key_pts)