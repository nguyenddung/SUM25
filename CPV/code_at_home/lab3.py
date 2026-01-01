import cv2
import numpy as np
from tkinter import Tk, Button, Label, filedialog, Canvas, PhotoImage, Frame
from PIL import Image, ImageTk
from skimage.feature import hog
from skimage import color


class FeatureDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Feature Detection Workshop")
        self.image = None
        self.original_image = None

        # GUI Layout
        self.canvas = Canvas(root, width=600, height=400)
        self.canvas.pack()

        button_frame = Frame(root)
        button_frame.pack(pady=10)

        Button(button_frame, text="Chọn ảnh", command=self.load_image).grid(
            row=0, column=0, padx=5
        )
        Button(button_frame, text="Harris", command=self.apply_harris).grid(
            row=0, column=1, padx=5
        )
        Button(button_frame, text="HOG", command=self.apply_hog).grid(
            row=0, column=2, padx=5
        )
        Button(button_frame, text="Canny", command=self.apply_canny).grid(
            row=0, column=3, padx=5
        )
        Button(button_frame, text="Hough", command=self.apply_hough).grid(
            row=0, column=4, padx=5
        )
        Button(button_frame, text="Quay lại ảnh gốc", command=self.reset_image).grid(
            row=0, column=5, padx=5
        )

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.image = self.original_image.copy()
            self.display_image(self.image)

    def display_image(self, img_cv2):
        img_rgb = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil = img_pil.resize((600, 400), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(image=img_pil)
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

    def reset_image(self):
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.display_image(self.image)

    def apply_harris(self):
        if self.image is not None:
            gray = np.float32(cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY))
            dst = cv2.cornerHarris(gray, 2, 3, 0.04)
            dst = cv2.dilate(dst, None)
            result = self.image.copy()
            result[dst > 0.01 * dst.max()] = [0, 0, 255]
            self.image = result
            self.display_image(result)

    def apply_hog(self):
        if self.image is not None:
            gray = color.rgb2gray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            _, hog_img = hog(
                gray,
                orientations=9,
                pixels_per_cell=(8, 8),
                cells_per_block=(2, 2),
                visualize=True,
            )
            hog_img = (hog_img * 255).astype("uint8")
            hog_bgr = cv2.cvtColor(hog_img, cv2.COLOR_GRAY2BGR)
            self.image = hog_bgr
            self.display_image(hog_bgr)

    def apply_canny(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edges_bgr = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            self.image = edges_bgr
            self.display_image(edges_bgr)

    def apply_hough(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            edges = cv2.Canny(gray, 50, 150)
            lines = cv2.HoughLinesP(
                edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10
            )
            result = self.image.copy()
            if lines is not None:
                for line in lines:
                    x1, y1, x2, y2 = line[0]
                    cv2.line(result, (x1, y1), (x2, y2), (0, 255, 0), 2)
            self.image = result
            self.display_image(result)


# Chạy ứng dụng
if __name__ == "__main__":
    root = Tk()
    app = FeatureDetectionApp(root)
    root.mainloop()
