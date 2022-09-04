import cv2
import numpy as np

def gray_to_BGR(img):
    return cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

def get_contours(img):
    contours, heirarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 30:
            cv2.drawContours(result_img, cnt, -1, (255, 0, 0), 2)
            perimeter = cv2.arcLength(cnt, True)
            # print(perimeter)
            corners = cv2.approxPolyDP(cnt, 0.02*perimeter, True)
            # print(len(corners))
            num_of_corners = len(corners)
            x, y, w, h = cv2.boundingRect(corners)

            obj_type = ""
            if num_of_corners == 3: obj_type = "Triangle"
            elif num_of_corners == 4:
                ratio = w/h
                if ratio > 0.95 and ratio < 1.05:
                    obj_type = "Square"
                else:
                    obj_type = "Rectangle"
            else: obj_type = "Circle"

            cv2.putText(result_img, obj_type, (x, y+(h//2)), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,0), 1)
            cv2.rectangle(result_img, (x, y), (x+w, y+h), (0,0,255), 1)

img = cv2.imread("resources/shapes.JPG")
img = cv2.resize(img, (280, 210))
result_img = img.copy()

gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blur_img = cv2.GaussianBlur(gray_img, (7,7), 1)
canny_img = cv2.Canny(blur_img, 50, 50)
kernel = np.ones((3,3), np.uint8)
dilated_img = cv2.dilate(canny_img, kernel, iterations=1)
eroded_img = cv2.erode(dilated_img, kernel, iterations=1)

get_contours(canny_img)

h_stack1 = np.hstack((img, gray_to_BGR(gray_img), gray_to_BGR(blur_img)))
h_stack2 = np.hstack((gray_to_BGR(canny_img), gray_to_BGR(eroded_img), result_img))
v_stack = np.vstack((h_stack1, h_stack2))

# cv2.imshow("original image", img)
# cv2.imshow("gray image", gray_img)
# cv2.imshow("blur image", blur_img)
# cv2.imshow("canny image", canny_img)
# cv2.imshow("dilated image", dilated_img)
# cv2.imshow("eroded image", eroded_img)

cv2.imshow("stacked images", v_stack)

cv2.waitKey(0)