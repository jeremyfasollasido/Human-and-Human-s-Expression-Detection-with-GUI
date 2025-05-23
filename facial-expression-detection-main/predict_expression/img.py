import cv2
import numpy as np
from tkinter import Tk, filedialog, Button, Label, messagebox, Frame
from tkinter import PhotoImage
from facial_expression_model import FacialExpressionModel

# Inisialisasi parameter
capture_size = 64
trained_face_data = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel('model.h5')
font = cv2.FONT_HERSHEY_SIMPLEX

def process_image(image_path):
    img = cv2.imread(image_path)
    grayScaledImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_co_ordinates = trained_face_data.detectMultiScale(grayScaledImg, 1.15)

    for (x, y, w, h) in face_co_ordinates:
        cropped_face = grayScaledImg[y:y+h, x:x+w]
        roi = cv2.resize(cropped_face, (capture_size, capture_size))
        prediction = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])

        text_size, _ = cv2.getTextSize(prediction, font, 1, 2)
        cv2.rectangle(img, (x, y - 30 - text_size[1]), (x + text_size[0], y - 10), (180, 184, 176), -1)
        cv2.putText(img, prediction, (x, y - 20), font, 1, (69, 74, 24), 2)
        cv2.rectangle(img, (x, y), (x + w, y + h), (106, 118, 252), 4)

    # Simpan hasil deteksi ke file baru
    result_img_path = image_path.replace('.jpg', '_result.jpg').replace('.jpeg', '_result.jpg').replace('.png', '_result.png')
    cv2.imwrite(result_img_path, img)

    # Tampilkan gambar dengan hasil deteksi
    cv2.imshow('Face Detector', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    messagebox.showinfo("Info", f"Gambar telah diproses dan disimpan sebagai {result_img_path}.")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png")])
    if file_path:
        process_image(file_path)

# GUI
root = Tk()
root.title("Facial Expression Detection")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Frame untuk konten
frame = Frame(root, bg="#ffffff", padx=20, pady=20)
frame.pack(pady=30)

# Logo atau gambar header (optional)
try:
    logo_img = PhotoImage(file="logo.png")
    logo_label = Label(frame, image=logo_img, bg="#ffffff")
    logo_label.pack(pady=10)
except Exception as e:
    print(f"Logo error: {e}")

# Label
label = Label(frame, text="Pilih file gambar untuk diproses:", bg="#ffffff", font=("Arial", 12))
label.pack(pady=10)

# Tombol pilih file
open_file_button = Button(frame, text="Pilih File", command=open_file, bg="#007bff", fg="#ffffff", font=("Arial", 12), padx=10, pady=5, relief="flat", cursor="hand2")
open_file_button.pack(pady=20)

# Deskripsi aplikasi
description = Label(frame, text="Aplikasi ini akan mendeteksi ekspresi wajah dalam gambar yang Anda pilih.", bg="#ffffff", font=("Arial", 10))
description.pack(pady=10)

root.mainloop()
