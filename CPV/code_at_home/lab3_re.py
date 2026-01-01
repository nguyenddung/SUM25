import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import color


def show_image(title, image):
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Function 1: Harris Corner Detector
def harris_corner_detector(image):
    gray = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
    dst = cv2.cornerHarris(gray, 2, 3, 0.04)
    dst = cv2.dilate(dst, None)
    image[dst > 0.01 * dst.max()] = [0, 0, 255]
    return image


# Function 2: Histogram of Oriented Gradients (HOG)
def hog_descriptor(image):
    gray = color.rgb2gray(image)
    fd, hog_image = hog(
        gray,
        orientations=9,
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2),
        visualize=True,
    )
    hog_image = (hog_image * 255).astype("uint8")
    return hog_image


# Function 3: Canny Edge Detection
def canny_edge_detection(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    return edges


# Function 4: Hough Transform (Line Detection)
def hough_transform(image):
    edges = canny_edge_detection(image)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10
    )
    line_img = image.copy()
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(line_img, (x1, y1), (x2, y2), (0, 255, 0), 2)
    return line_img


# Main function
def main():
    path = "cat.jpg"  # Replace with your image path
    image = cv2.imread(path)
    if image is None:
        print("Không thể đọc ảnh.")
        return

    print("Chọn chức năng:")
    print("1: Harris Corner Detector")
    print("2: Histogram of Oriented Gradients (HOG)")
    print("3: Canny Edge Detection")
    print("4: Hough Transform")
    choice = input("Lựa chọn (1/2/3/4): ")

    if choice == "1":
        result = harris_corner_detector(image.copy())
        show_image("Harris Corner Detector", result)

    elif choice == "2":
        hog_img = hog_descriptor(image)
        cv2.imshow("HOG Descriptor", hog_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == "3":
        result = canny_edge_detection(image.copy())
        show_image("Canny Edge Detection", result)

    elif choice == "4":
        result = hough_transform(image.copy())
        show_image("Hough Transform", result)

    else:
        print("Lựa chọn không hợp lệ.")


if __name__ == "__main__":
    main()
