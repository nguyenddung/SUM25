import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

DISPLAY_W, DISPLAY_H = 420, 300  # Kích thước hiển thị ảnh lớn


class FeatureAlignApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Feature-Based Alignment (RANSAC Demo)")
        self.master.geometry("1000x820")
        self.master.resizable(False, False)

        # Lưu đường dẫn và ảnh đã chọn
        self.images = [None, None]
        self.image_paths = ["", ""]

        # Khung chọn ảnh và hiển thị ảnh gốc
        self.img_labels = []
        for i in range(2):
            frame = tk.Frame(master, bd=2, relief=tk.GROOVE)
            frame.place(
                x=30 + i * (DISPLAY_W + 40),
                y=20,
                width=DISPLAY_W + 20,
                height=DISPLAY_H + 60,
            )
            btn = tk.Button(
                frame,
                text=f"Chọn ảnh {i+1}",
                font=("Arial", 12),
                command=lambda idx=i: self.load_image(idx),
            )
            btn.pack(pady=5)
            lbl = tk.Label(
                frame,
                text="Chưa chọn ảnh",
                bg="#eee",
                width=DISPLAY_W,
                height=DISPLAY_H,
            )
            lbl.pack()
            self.img_labels.append(lbl)

        # Nút thực hiện Align
        self.btn_align = tk.Button(
            master,
            text="Align & Show Result",
            font=("Arial", 15, "bold"),
            bg="#2196F3",
            fg="white",
            command=self.align_images,
        )
        self.btn_align.place(x=DISPLAY_W + 70, y=DISPLAY_H + 45, width=220, height=50)

        # Hiển thị kết quả Align
        tk.Label(
            master,
            text="Kết quả Align (Ảnh 1 biến đổi theo Ảnh 2):",
            font=("Arial", 13),
        ).place(x=60, y=DISPLAY_H + 140)
        self.result_aligned = tk.Label(
            master, bg="#eee", width=DISPLAY_W, height=DISPLAY_H
        )
        self.result_aligned.place(x=60, y=DISPLAY_H + 170)

        # Hiển thị ghép đặc trưng
        tk.Label(master, text="Kết quả ghép đặc trưng:", font=("Arial", 13)).place(
            x=DISPLAY_W + 100, y=DISPLAY_H + 140
        )
        self.result_matches = tk.Label(
            master, bg="#eee", width=DISPLAY_W, height=DISPLAY_H
        )
        self.result_matches.place(x=DISPLAY_W + 100, y=DISPLAY_H + 170)

    def load_image(self, idx):
        path = filedialog.askopenfilename(
            title="Chọn file ảnh",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp")],
        )
        if path:
            img = cv2.imread(path)
            if img is not None:
                self.images[idx] = img
                self.image_paths[idx] = path
                # Hiển thị ảnh lên giao diện
                thumb = cv2.resize(img, (DISPLAY_W, DISPLAY_H))
                thumb = cv2.cvtColor(thumb, cv2.COLOR_BGR2RGB)
                im = Image.fromarray(thumb)
                imgtk = ImageTk.PhotoImage(im)
                self.img_labels[idx].configure(image=imgtk, text="")
                self.img_labels[idx].image = imgtk  # Giữ tham chiếu ảnh

    def align_images(self):
        if self.images[0] is None or self.images[1] is None:
            messagebox.showerror(
                "Lỗi", "Vui lòng chọn cả 2 ảnh trước khi thực hiện align!"
            )
            return
        img1 = self.images[0]
        img2 = self.images[1]

        # 1. Detect features
        detector = cv2.ORB_create(2000)
        kp1, des1 = detector.detectAndCompute(img1, None)
        kp2, des2 = detector.detectAndCompute(img2, None)

        # 2. Match features
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = matcher.match(des1, des2)
        matches = sorted(matches, key=lambda x: x.distance)
        good_matches = matches[:80]  # Lấy 80 match tốt nhất

        if len(good_matches) < 4:
            messagebox.showerror("Lỗi", "Không đủ đặc trưng để align!")
            return

        pts1 = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
        pts2 = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

        # 3. RANSAC
        H, mask = cv2.findHomography(pts1, pts2, cv2.RANSAC, 5.0)
        if H is None:
            messagebox.showerror("Lỗi", "Không thể tìm phép biến đổi phù hợp.")
            return

        # 4. Warp ảnh 1 theo ảnh 2
        height, width = img2.shape[:2]
        aligned = cv2.warpPerspective(img1, H, (width, height))

        # 5. Hiển thị kết quả Align
        align_disp = cv2.resize(aligned, (DISPLAY_W, DISPLAY_H))
        align_disp = cv2.cvtColor(align_disp, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(align_disp)
        imgtk = ImageTk.PhotoImage(img)
        self.result_aligned.configure(image=imgtk, text="")
        self.result_aligned.image = imgtk

        # 6. Hiển thị kết quả ghép đặc trưng (matches)
        mask_flat = mask.ravel().tolist()
        match_img = cv2.drawMatches(
            img1,
            kp1,
            img2,
            kp2,
            good_matches,
            None,
            matchesMask=mask_flat,
            flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS,
        )
        match_disp = cv2.resize(match_img, (DISPLAY_W, DISPLAY_H))
        match_disp = cv2.cvtColor(match_disp, cv2.COLOR_BGR2RGB)
        imgm = Image.fromarray(match_disp)
        imgmtk = ImageTk.PhotoImage(imgm)
        self.result_matches.configure(image=imgmtk, text="")
        self.result_matches.image = imgmtk


# Chạy app
if __name__ == "__main__":
    root = tk.Tk()
    app = FeatureAlignApp(root)
    root.mainloop()
