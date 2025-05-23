
# Real Time Human Detection & Counting

# imported necessary library
from tkinter import *
import numpy as np
import tkinter as tk
import tkinter.messagebox as mbox
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import argparse
from persondetection import DetectorAPI
import matplotlib.pyplot as plt
from fpdf import FPDF
from facial_expression_model import FacialExpressionModel
import subprocess

# Main Window & Configuration
window = tk.Tk()
window.title("Human Detection & Human Expression Detection")
window.iconbitmap(f'D:\Kuliah\Semester Antara\KCD\Proyek Akhir\proyek akhir\Real-Time-Human-Detection-Counting-main\Images\icon.ico')
window.geometry('1000x700')

# top label
start1 = tk.Label(text = "Human Detection &\nHuman Expression Detection", font=("Arial", 50,"underline"), fg="magenta") # same way bg
start1.place(x = 70, y = 10)

# function defined to start the main application
def start_fun():
    window.destroy()

# created a start button
Button(window, text="▶ START",command=start_fun,font=("Arial", 25), bg = "orange", fg = "blue", cursor="hand2", borderwidth=3, relief="raised").place(x =130 , y =570 )

# image on the main window
path1 = "Images/front2.png"
img2 = ImageTk.PhotoImage(Image.open(path1))
panel1 = tk.Label(window, image = img2)
panel1.place(x = 90, y = 250)

# image on the main window
path = "Images/front1.png"
img1 = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img1)
panel.place(x = 380, y = 180)

exit1 = False
# function created for exiting from window
def exit_win():
    global exit1
    if mbox.askokcancel("Exit", "Do you want to exit?"):
        exit1 = True
        window.destroy()

# exit button created
Button(window, text="❌ EXIT",command=exit_win,font=("Arial", 25), bg = "red", fg = "blue", cursor="hand2", borderwidth=3, relief="raised").place(x =680 , y = 570 )

window.protocol("WM_DELETE_WINDOW", exit_win)
window.mainloop()

if exit1==False:
    # Main Window & Configuration of window1
    window1 = tk.Tk()
    window1.title("Human Detection & Human Expression Detection")
    window1.iconbitmap('Images/icon.ico')
    window1.geometry('1000x700')

    filename=""
    filename1=""
    filename2=""

    def argsParser():
        arg_parse = argparse.ArgumentParser()
        arg_parse.add_argument("-v", "--video", default=None, help="path to Video File ")
        arg_parse.add_argument("-i", "--image", default=None, help="path to Image File ")
        arg_parse.add_argument("-c", "--camera", default=False, help="Set true if you want to use the camera.")
        arg_parse.add_argument("-o", "--output", type=str, help="path to optional output video file")
        args = vars(arg_parse.parse_args())
        return args

    # ---------------------------- image section ------------------------------------------------------------
    def image_option():
        # new windowi created for image section
        windowi = tk.Tk()
        windowi.title("Human Detection from Image")
        windowi.iconbitmap('Images/icon.ico')
        windowi.geometry('1000x700')

        max_count1 = 0
        framex1 = []
        county1 = []
        max1 = []
        avg_acc1_list = []
        max_avg_acc1_list = []
        max_acc1 = 0
        max_avg_acc1 = 0

        # function defined to open the image
        def open_img():
            global filename1, max_count1, framex1, county1, max1, avg_acc1_list, max_avg_acc1_list, max_acc1, max_avg_acc1
            max_count1 = 0
            framex1 = []
            county1 = []
            max1 = []
            avg_acc1_list = []
            max_avg_acc1_list = []
            max_acc1 = 0
            max_avg_acc1 = 0

            filename1 = filedialog.askopenfilename(title="Select Image file", parent = windowi)
            path_text1.delete("1.0", "end")
            path_text1.insert(END, filename1)

        # function defined to detect the image
        def det_img():
            global filename1, max_count1, framex1, county1, max1, avg_acc1_list, max_avg_acc1_list, max_acc1, max_avg_acc1
            max_count1 = 0
            framex1 = []
            county1 = []
            max1 = []
            avg_acc1_list = []
            max_avg_acc1_list = []
            max_acc1 = 0
            max_avg_acc1 = 0

            image_path = filename1
            if(image_path==""):
                mbox.showerror("Error", "No Image File Selected!", parent = windowi)
                return
            info1.config(text="Status : Detecting...")
            # info2.config(text="                                                  ")
            mbox.showinfo("Status", "Detecting, Please Wait...", parent = windowi)
            # time.sleep(1)
            detectByPathImage(image_path)

        # main detection process process here
        def detectByPathImage(path):
            global filename1, max_count1, framex1, county1, max1, avg_acc1_list, max_avg_acc1_list, max_acc1, max_avg_acc1
            max_count1 = 0
            framex1 = []
            county1 = []
            max1 = []
            avg_acc1_list = []
            max_avg_acc1_list = []
            max_acc1 = 0
            max_avg_acc1 = 0

            # function defined to plot the enumeration fo people detected
            def img_enumeration_plot():
                plt.figure(facecolor='orange', )
                ax = plt.axes()
                ax.set_facecolor("yellow")
                plt.plot(framex1, county1, label="Human Count", color="green", marker='o', markerfacecolor='blue')
                plt.plot(framex1, max1, label="Max. Human Count", linestyle='dashed', color='fuchsia')
                plt.xlabel('Time (sec)')
                plt.ylabel('Human Count')
                plt.legend()
                plt.title("Enumeration Plot")
                # plt.get_current_fig_manager().canvas.set_window_title("Plot for Image")
                # plt.manager.set_window_title("Plot for Image")
                plt.show()

            def img_accuracy_plot():
                plt.figure(facecolor='orange', )
                ax = plt.axes()
                ax.set_facecolor("yellow")
                plt.plot(framex1, avg_acc1_list, label="Avg. Accuracy", color="green", marker='o', markerfacecolor='blue')
                plt.plot(framex1, max_avg_acc1_list, label="Max. Avg. Accuracy", linestyle='dashed', color='fuchsia')
                plt.xlabel('Time (sec)')
                plt.ylabel('Avg. Accuracy')
                plt.title('Avg. Accuracy Plot')
                plt.legend()
                plt.get_current_fig_manager().canvas.set_window_title("Plot for Image")
                plt.show()

            def img_gen_report():
                pdf = FPDF(orientation='P', unit='mm', format='A4')
                pdf.add_page()
                pdf.set_font("Arial", "", 20)
                pdf.set_text_color(128, 0, 0)
                pdf.image('Images/Crowd_Report.png', x=0, y=0, w=210, h=297)

                pdf.text(125, 150, str(max_count1))
                pdf.text(105, 163, str(max_acc1))
                pdf.text(125, 175, str(max_avg_acc1))
                if (max_count1 > 25):
                    pdf.text(26, 220, "Max. Human Detected is greater than MAX LIMIT.")
                    pdf.text(70, 235, "Region is Crowded.")
                else:
                    pdf.text(26, 220, "Max. Human Detected is in range of MAX LIMIT.")
                    pdf.text(65, 235, "Region is not Crowded.")

                pdf.output('Crowd_Report.pdf')
                mbox.showinfo("Status", "Report Generated and Saved Successfully.", parent = windowi)


            odapi = DetectorAPI()
            threshold = 0.7

            image = cv2.imread(path)
            img = cv2.resize(image, (image.shape[1], image.shape[0]))
            boxes, scores, classes, num = odapi.processFrame(img)
            person = 0
            acc=0
            for i in range(len(boxes)):

                if classes[i] == 1 and scores[i] > threshold:
                    box = boxes[i]
                    person += 1
                    cv2.rectangle(img, (box[1], box[0]), (box[3], box[2]), (255,0,0), 2)  # cv2.FILLED #BGR
                    cv2.putText(img, f'P{person, round(scores[i], 2)}', (box[1] - 30, box[0] - 8), cv2.FONT_HERSHEY_COMPLEX,0.5, (0, 0, 255), 1)  # (75,0,130),
                    acc += scores[i]
                    if (scores[i] > max_acc1):
                        max_acc1 = scores[i]

            if (person > max_count1):
                max_count1 = person
            if(person>=1):
                if((acc / person) > max_avg_acc1):
                    max_avg_acc1 = (acc / person)


            cv2.imshow("Human Detection from Image", img)
            info1.config(text="                                                  ")
            info1.config(text="Status : Detection & Counting Completed")
            # info2.config(text="                                                  ")
            # info2.config(text="Max. Human Count : " + str(max_count1))
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            for i in range(20):
                framex1.append(i)
                county1.append(max_count1)
                max1.append(max_count1)
                avg_acc1_list.append(max_avg_acc1)
                max_avg_acc1_list.append(max_avg_acc1)

        def prev_img():
            global filename1
            img = cv2.imread(filename1, 1)
            cv2.imshow("Selected Image Preview", img)

        # for images ----------------------
        lbl1 = tk.Label(windowi,text="DETECT  FROM\nIMAGE", font=("Arial", 50, "underline"),fg="brown")
        lbl1.place(x=230, y=20)
        lbl2 = tk.Label(windowi,text="Selected Image", font=("Arial", 30),fg="green")
        lbl2.place(x=80, y=200)
        path_text1 = tk.Text(windowi, height=1, width=37, font=("Arial", 30), bg="light yellow", fg="orange",borderwidth=2, relief="solid")
        path_text1.place(x=80, y = 260)

        Button(windowi, text="SELECT", command=open_img, cursor="hand2", font=("Arial", 20), bg="light green", fg="blue").place(x=220, y=350)
        Button(windowi, text="PREVIEW",command=prev_img, cursor="hand2", font=("Arial", 20), bg = "yellow", fg = "blue").place(x = 410, y = 350)
        Button(windowi, text="DETECT",command=det_img, cursor="hand2", font=("Arial", 20), bg = "orange", fg = "blue").place(x = 620, y = 350)

        info1 = tk.Label(windowi,font=( "Arial", 30),fg="gray")
        info1.place(x=100, y=445)
        # info2 = tk.Label(windowi,font=("Arial", 30), fg="gray")
        # info2.place(x=100, y=500)

        def exit_wini():
            if mbox.askokcancel("Exit", "Do you want to exit?", parent = windowi):
                windowi.destroy()
        windowi.protocol("WM_DELETE_WINDOW", exit_wini)


    # ---------------------------- ekspresi section ------------------------------------------------------------
    def ekspresi_option():
        subprocess.Popen(["python", r"D:\Kuliah\Semester Antara\KCD\Proyek Akhir\proyek akhir\facial-expression-detection-main\predict_expression\img.py"])


    # options -----------------------------
    lbl1 = tk.Label(text="OPTIONS", font=("Arial", 50, "underline"),fg="brown")  # same way bg
    lbl1.place(x=340, y=20)

    # image on the main window
    pathi = "Images/image1.jpg"
    imgi = ImageTk.PhotoImage(Image.open(pathi))
    paneli = tk.Label(window1, image = imgi)
    paneli.place(x = 90, y = 110)

    # image on the main window
    pathv = "Images/image1.jpg"
    imgv = ImageTk.PhotoImage(Image.open(pathv))
    panelv = tk.Label(window1, image = imgv)
    panelv.place(x = 700, y = 260)# 720, 260

    # created button for all three option
    Button(window1, text="DETECT  HUMAN ➡",command=image_option, cursor="hand2", font=("Arial",30), bg = "light green", fg = "blue").place(x = 350, y = 150)
    Button(window1, text="DETECT  EXPRESSION ➡",command=ekspresi_option, cursor="hand2", font=("Arial", 30), bg = "light blue", fg = "blue").place(x = 110, y = 300) #90, 300

    # function defined to exit from window1
    def exit_win1():
        if mbox.askokcancel("Exit", "Do you want to exit?"):
            window1.destroy()

    # created exit button
    Button(window1, text="❌ EXIT",command=exit_win1,  cursor="hand2", font=("Arial", 25), bg = "red", fg = "blue").place(x = 440, y = 600)

    window1.protocol("WM_DELETE_WINDOW", exit_win1)
    window1.mainloop()

