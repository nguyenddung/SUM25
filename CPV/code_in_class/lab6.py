import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, Toplevel
from PIL import Image, ImageTk


class ImageStitchingApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Stitching")
        self.images = []

        # Tạo các thành phần UI
        self.load_button = tk.Button(
            self.master, text="Load Images", command=self.load_images
        )
        self.load_button.pack()

        self.stitch_button = tk.Button(
            self.master, text="Start Stitching", command=self.stitch_images
        )
        self.stitch_button.pack()

        self.canvas = tk.Canvas(
            self.master, width=1200, height=400
        )  # Tăng kích thước canvas
        self.canvas.pack()

        # Tham chiếu đến đối tượng ảnh để tránh mất ảnh trong Tkinter
        self.current_images = []  # Lưu các đối tượng ảnh

    def load_images(self):
        file_paths = filedialog.askopenfilenames()
        if len(file_paths) < 2:
            print("Please load at least two images.")
            return

        self.images = [cv2.imread(fp) for fp in file_paths]

        # Kiểm tra xem các ảnh có được tải đúng không
        print(f"Loaded {len(self.images)} images successfully.")

        self.display_images()

    def display_images(self):
        if len(self.images) >= 2:
            # Hiển thị ảnh đầu tiên
            img1 = cv2.cvtColor(self.images[0], cv2.COLOR_BGR2RGB)
            img1 = Image.fromarray(img1)
            img1 = ImageTk.PhotoImage(img1)

            # Hiển thị ảnh thứ hai
            img2 = cv2.cvtColor(self.images[1], cv2.COLOR_BGR2RGB)
            img2 = Image.fromarray(img2)
            img2 = ImageTk.PhotoImage(img2)

            # Hiển thị hai ảnh lên canvas tại các vị trí khác nhau
            self.canvas.create_image(300, 200, image=img1)
            self.canvas.create_image(900, 200, image=img2)

            # Giữ tham chiếu đến ảnh để tránh mất ảnh trong Tkinter
            self.current_images = [img1, img2]

    def stitch_images(self):
        if len(self.images) < 2:
            print("Please load at least two images.")
            return

        # Kiểm tra kích thước của ảnh trước khi ghép
        print(f"Attempting to stitch {len(self.images)} images...")

        # Tạo đối tượng Stitcher của OpenCV
        stitcher = cv2.Stitcher_create()
        status, stitched_image = stitcher.stitch(self.images)

        # Kiểm tra trạng thái ghép ảnh
        if status == cv2.Stitcher_OK:
            print("Stitching successful!")
            stitched_image = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(stitched_image)
            img = ImageTk.PhotoImage(img)

            # Hiển thị ảnh ghép trên cửa sổ mới
            self.show_stitched_image(stitched_image)

            # Lưu ảnh
            self.save_output(stitched_image)
        else:
            print(
                f"Error during stitching! Status code: {status}. Please check the overlap between images."
            )

    def show_stitched_image(self, stitched_image):
        # Tạo cửa sổ mới để hiển thị ảnh ghép
        top = Toplevel(self.master)
        top.title("Stitched Image")

        # Chuyển ảnh OpenCV thành ImageTk
        img = Image.fromarray(stitched_image)
        img = ImageTk.PhotoImage(img)

        # Tạo canvas trong cửa sổ mới
        canvas = tk.Canvas(top, width=img.width(), height=img.height())
        canvas.pack()

        # Hiển thị ảnh ghép trong cửa sổ mới
        canvas.create_image(0, 0, image=img, anchor="nw")

        # Giữ tham chiếu đến ảnh để tránh mất ảnh
        canvas.image = img

    def save_output(self, stitched_image):
        output_path = filedialog.asksaveasfilename(defaultextension=".jpg")
        if output_path:
            cv2.imwrite(output_path, stitched_image)
            print(f"Image saved successfully to {output_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageStitchingApp(root)
    root.mainloop()
