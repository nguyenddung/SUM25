import cv2
import numpy as np
from matplotlib import pyplot as plt


# address = "D:/SUM25/CPV/code_at_home/cat.jpg"
address = "D:/SUM25/CPV/code_in_class/images/Lady.png"
image = cv2.imread(address)
image = cv2.resize(image, (512, 512))
original = image.copy()




def nothing(x):
    pass




def tinhHistogram(img):
    histR = np.zeros(256, dtype=int)
    histG = np.zeros(256, dtype=int)
    histB = np.zeros(256, dtype=int)


    h, w, _ = img.shape
    print(img)
    for y in range(h):
        for x in range(w):
            if img.dtype == np.float32 or img.dtype == np.float64:
                b = int(img[y, x, 0] * 255)
                g = int(img[y, x, 1] * 255)
                r = int(img[y, x, 2] * 255)
            else:
                b = int(img[y, x, 0])
                g = int(img[y, x, 1])
                r = int(img[y, x, 2])
            histR[r] += 1
            histG[g] += 1
            histB[b] += 1
    return histR, histG, histB




cv2.namedWindow("Color Balance")
cv2.createTrackbar("R", "Color Balance", 100, 200, nothing)
cv2.createTrackbar("G", "Color Balance", 100, 200, nothing)
cv2.createTrackbar("B", "Color Balance", 100, 200, nothing)


while True:
    r = cv2.getTrackbarPos("R", "Color Balance") / 100
    g = cv2.getTrackbarPos("G", "Color Balance") / 100
    b = cv2.getTrackbarPos("B", "Color Balance") / 100


    balanced = image.copy().astype(np.float32)
    balanced[:, :, 2] *= r
    balanced[:, :, 1] *= g
    balanced[:, :, 0] *= b
    balanced = np.clip(balanced, 0, 255).astype(np.uint8)


    cv2.imshow("Color Balance", balanced)


    key = cv2.waitKey(1) & 0xFF
    if key == ord("h"):
        a, b, c = tinhHistogram(balanced)
        plt.figure(figsize=(10, 5))
        plt.plot(a, color="red", label="Red Channel")
        plt.plot(b, color="green", label="Green Channel")
        plt.plot(c, color="blue", label="Blue Channel")
        plt.show()


    elif key == ord("m"):
        # Mean filter
        mean_filtered = balanced.copy()
        m, n = 1, 1
        for m in range(1, balanced.shape[0] - 1):
            for n in range(1, balanced.shape[1] - 1):
                region = balanced[m - 1 : m + 2, n - 1 : n + 2]
                mean_filtered[m, n] = np.mean(region)


        plt.imshow(mean_filtered, cmap="gray")
        # plt.imshow(cv2.cvtColor(mean_filtered, cv2.COLOR_BGR2RGB))
        plt.title("Mean Filter")
        plt.show()


    elif key == ord("d"):
        # Median filter


        median_filtered = balanced.copy()
        m, n = 1, 1
        for m in range(1, balanced.shape[0] - 1):
            for n in range(1, balanced.shape[1] - 1):
                region = balanced[m - 1 : m + 2, n - 1 : n + 2]
                median_filtered[m, n] = np.median(region)


        plt.imshow(median_filtered, cmap="gray")
        plt.title("Median Filter")
        plt.show()


    elif key == ord("g"):
        # Gaussian smoothing
        gaussian = cv2.GaussianBlur(balanced, (3, 3), 1.0)
        cv2.imshow("Gaussian Smoothing", gaussian)


    elif key == ord("r"):
        image = original.copy()  # Reset image


    elif key == ord("q"):  # ESC
        break


cv2.destroyAllWindows()




