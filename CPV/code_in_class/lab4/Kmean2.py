import cv2
from sklearn.cluster import KMeans
import os
import numpy as np
import pickle
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

c_data_path = r"D:\SUM25\CPV\code_in_class\lab4\data\Busy\1"


# cong tong tung kenh cua tat ca cac diem anh trong anh
def get_feature(img):
    if img is None:
        return 0
    intensity = img.sum(axis=1)
    intensity = intensity.sum(axis=0) / (255 * img.shape[0] * img.shape[1])
    return intensity


def load_data(data_path=c_data_path):
    pickle_path = r"D:\SUM25\CPV\code_in_class\lab4\data.pickle"
    try:
        with open(pickle_path, "rb") as handle:
            X, L = pickle.load(handle)
        return X, L
    except:
        X = []
        L = []
        for file in os.listdir(data_path):
            file_path = os.path.join(data_path, file)
            img = cv2.imread(file_path)
            if img is None:
                print(f"Cannot read image: {file_path}")
                continue
            c_x = get_feature(img)
            X.append(c_x)
            L.append(file)
        X = np.array(X)
        L = np.array(L)
        with open(pickle_path, "wb") as handle:
            pickle.dump((X, L), handle, protocol=pickle.HIGHEST_PROTOCOL)
        return X, L


# Load data
X, L = load_data()
print("Feature shape:", X.shape)

# Elbow method to choose k
distortions = []
K = range(1, 10)
X_reshape = X.reshape(-1, 1) if len(X.shape) == 1 else X
for k in K:
    kmeanModel = KMeans(n_clusters=k, random_state=42)
    kmeanModel.fit(X_reshape)
    distortions.append(kmeanModel.inertia_)

# plt.figure(figsize=(10, 5))
# plt.plot(K, distortions, "bx-")
# plt.xlabel("k")
# plt.ylabel("Distortion")
# plt.title("The Elbow Method showing the optimal k")
# plt.show()

# # KMeans clustering with k=5
kmeans = KMeans(n_clusters=5, random_state=42).fit(X_reshape)
for i in range(len(kmeans.labels_)):
    print(kmeans.labels_[i], " - ", L[i])
print("Cluster centers:", kmeans.cluster_centers_)

# Show clustered images
n_row = 6
n_col = 6
for i in range(5):
    _, axs = plt.subplots(n_row, n_col, figsize=(7, 7))
    axs = axs.flatten()
    cluster_indices = np.where(kmeans.labels_ == i)[0]
    for img_name, ax in zip(L[cluster_indices][:36], axs):
        img_path = os.path.join(c_data_path, str(img_name))
        try:
            ax.imshow(mpimg.imread(img_path))
            ax.set_title(str(img_name), fontsize=6)
            ax.axis("off")
        except Exception as e:
            ax.axis("off")
            print(f"Error loading {img_path}: {e}")
    plt.tight_layout()
    plt.show()


# Đếm số lượng ảnh trong mỗi cụm
unique, counts = np.unique(kmeans.labels_, return_counts=True)
for label, count in zip(unique, counts):
    print(f"Cụm {label}: {count} ảnh")
