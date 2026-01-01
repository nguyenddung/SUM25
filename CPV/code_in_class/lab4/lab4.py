import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.segmentation import active_contour
from skimage.filters import gaussian
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
from skimage.segmentation import watershed
from scipy import ndimage as ndi
from skimage.feature import peak_local_max
from sklearn.neighbors import NearestNeighbors

# Load ảnh đầu vào
path = r"D:\SUM25\CPV\code_in_class\images\coins.jpg"
image = cv2.imread(path)

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# ======= FUNCTION 1: SNAKES (Active Contour) =======
def snake_segmentation(img_gray):
    print("Running Snakes Algorithm...")
    img_smooth = gaussian(img_gray, 3)
    s = np.linspace(0, 2 * np.pi, 400)
    x = 100 + 80 * np.cos(s)
    y = 100 + 80 * np.sin(s)
    init = np.array([x, y]).T
    snake = active_contour(img_smooth, init, alpha=0.015, beta=10, gamma=0.001)

    fig, ax = plt.subplots()
    ax.imshow(img_gray, cmap="gray")
    ax.plot(init[:, 0], init[:, 1], "--r", label="Initial contour")
    ax.plot(snake[:, 0], snake[:, 1], "-b", label="Snakes contour")
    ax.set_title("Snakes Segmentation")
    ax.legend()
    plt.show()


# ======= FUNCTION 2: WATERSHED =======
def watershed_segmentation(img_gray):
    print("Running Watershed Algorithm...")
    ret, thresh = cv2.threshold(
        img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )
    distance = ndi.distance_transform_edt(thresh)
    coords = peak_local_max(distance, footprint=np.ones((3, 3)), labels=thresh)
    mask = np.zeros(distance.shape, dtype=bool)
    mask[tuple(coords.T)] = True
    markers, _ = ndi.label(mask)
    labels = watershed(-distance, markers, mask=thresh)

    plt.imshow(labels, cmap="nipy_spectral")
    plt.title("Watershed Segmentation")
    plt.axis("off")
    plt.show()


# ======= FUNCTION 3: K-MEANS CLUSTERING =======
def kmeans_segmentation(image, k=4):
    print("Running K-Means Clustering...")
    img = np.array(image, dtype=np.float64) / 255
    w, h, d = img.shape
    img_array = np.reshape(img, (w * h, d))

    image_array_sample = shuffle(img_array, random_state=0)[:1000]
    kmeans = KMeans(n_clusters=k, n_init=5, random_state=0).fit(image_array_sample)
    labels = kmeans.predict(img_array)
    clustered = kmeans.cluster_centers_[labels].reshape(w, h, d)

    plt.imshow(clustered)
    plt.title(f"K-Means Segmentation (k={k})")
    plt.axis("off")
    plt.show()


# ======= FUNCTION 4: MEAN SHIFT =======
def mean_shift_segmentation(image, bandwidth=0.1):
    print("Running Mean Shift Segmentation...")
    flat_image = np.reshape(image, [-1, 3])
    flat_image = np.float32(flat_image) / 255.0

    # Fit NearestNeighbors to find bandwidth radius
    nn = NearestNeighbors(radius=bandwidth)
    nn.fit(flat_image)

    labels = np.zeros(flat_image.shape[0])
    cluster_centers = []
    cluster_id = 0

    for i, pixel in enumerate(flat_image):
        if labels[i] != 0:
            continue
        neighbors = nn.radius_neighbors([pixel], return_distance=False)[0]
        if len(neighbors) == 0:
            continue
        center = np.mean(flat_image[neighbors], axis=0)
        cluster_centers.append(center)
        labels[neighbors] = cluster_id
        cluster_id += 1

    output = np.array([cluster_centers[int(l)] for l in labels])
    segmented = np.reshape(output, image.shape)

    plt.imshow(segmented)
    plt.title("Mean Shift Segmentation")
    plt.axis("off")
    plt.show()


# ========= RUN MENU =========
def main():
    while True:
        print("\nChọn thuật toán segmentation:")
        print("1. Snakes")
        print("2. Watershed")
        print("3. K-means")
        print("4. Mean shift")
        print("0. Thoát")
        choice = input("Nhập lựa chọn: ")

        if choice == "1":
            snake_segmentation(image_gray)
        elif choice == "2":
            watershed_segmentation(image_gray)
        elif choice == "3":
            kmeans_segmentation(image, k=4)
        elif choice == "4":
            mean_shift_segmentation(image)
        elif choice == "0":
            break
        else:
            print("Lựa chọn không hợp lệ!")


if __name__ == "__main__":
    main()
