import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from sklearn.cluster import KMeans
import cv2


# Hàm chọn ảnh từ máy
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        process_image(file_path)


# Hàm xử lý ảnh bằng K-Means
def process_image(path):
    # Đọc ảnh với OpenCV và chuyển về RGB
    img = cv2.imread(path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Hiển thị ảnh gốc
    show_image(img_rgb, "Original Image", 0)

    # Reshape ảnh về dạng (số pixel, 3 kênh màu)
    pixel_data = img_rgb.reshape((-1, 3))

    # Áp dụng KMeans với K cụm (số màu mong muốn)
    K = 8  # bạn có thể thay đổi
    kmeans = KMeans(n_clusters=K, random_state=0).fit(pixel_data)
    new_colors = kmeans.cluster_centers_.astype("uint8")
    labels = kmeans.labels_

    # Tạo ảnh mới
    quantized_img = new_colors[labels].reshape(img_rgb.shape)

    # Hiển thị ảnh sau khi xử lý
    show_image(quantized_img, f"K-Means with K={K}", 1)


# Hàm hiển thị ảnh bằng Tkinter
def show_image(img_array, title, position):
    img_pil = Image.fromarray(img_array)
    img_resized = img_pil.resize((300, 300))
    img_tk = ImageTk.PhotoImage(img_resized)

    panel = tk.Label(image=img_tk)
    panel.image = img_tk
    panel.grid(row=0, column=position)
    title_label = tk.Label(text=title)
    title_label.grid(row=1, column=position)


# Tạo GUI
root = tk.Tk()
root.title("K-Means Color Quantization")

btn = tk.Button(root, text="Chọn ảnh", command=select_image)
btn.grid(row=2, column=0, columnspan=2, pady=10)

root.mainloop()
