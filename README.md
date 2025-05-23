# Real-Time Human Detection & Human Expression Detection with GUI

This project implements a real-time human detection system along with a human facial expression detection module, all integrated within a user-friendly Graphical User Interface (GUI) built with Tkinter.

## Features

* **Human Detection from Image:** Detects and counts humans present in a static image file.
* **Human Expression Detection:** Launches a separate module to detect facial expressions (e.g., happy, sad, angry) from a camera feed or video.
* **Crowd Analysis Report (for Image Detection):** Generates a PDF report summarizing the maximum human count, maximum individual detection accuracy, and maximum average accuracy for analyzed images.
* **Intuitive Tkinter GUI:** Provides an easy-to-use interface for selecting options and viewing results.
* **Visualization:** Displays bounding boxes around detected humans and their confidence scores.

## Technologies Used

* **Python 3.x**
* **Tkinter:** For building the graphical user interface.
* **OpenCV (`cv2`):** For image and video processing, including reading frames, drawing bounding boxes, and displaying output.
* **TensorFlow / Keras:** (Implied by `persondetection.py` and `facial_expression_model.py`) For the underlying deep learning models used for detection and classification.
* **NumPy:** For numerical operations.
* **PIL (Pillow):** For image manipulation in Tkinter.
* **Matplotlib:** For plotting enumeration and accuracy graphs.
* **FPDF:** For generating PDF reports.
* **Argparse:** For command-line argument parsing (though primarily used internally within the detection modules).
* **Subprocess:** To run the facial expression detection module as a separate process.

## Setup Instructions

To run this project, follow these steps:

1.  **Clone the Repository (or download the code):**
    If you're cloning this from GitHub, use:
    ```bash
    git clone [https://github.com/jeremyfasollasido/Human-and-Human-s-Expression-Detection-with-GUI.git](https://github.com/jeremyfasollasido/Human-and-Human-s-Expression-Detection-with-GUI.git)
    cd Human-and-Human-s-Expression-Detection-with-GUI
    ```
    If you've just uploaded it, ensure your local project folder contains all the necessary files.

2.  **Create a Virtual Environment (Recommended):**
    It's good practice to use a virtual environment to manage dependencies.
    ```bash
    python -m venv venv
    ```
    **Activate the virtual environment:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

3.  **Install Dependencies:**
    You'll need to install the required Python libraries. Create a `requirements.txt` file in your main project directory with the following content:

    ```
    tkinter
    numpy
    Pillow
    opencv-python
    tensorflow # Or tensorflow-cpu depending on your setup
    matplotlib
    fpdf
    # You might also need specific versions of the deep learning models
    # e.g., if DetectorAPI or FacialExpressionModel rely on specific Keras/TF versions.
    # Add any other specific dependencies for persondetection.py and facial_expression_model.py
    ```
    Then install them:
    ```bash
    pip install -r requirements.txt
    ```
    **Note:** `tkinter` is usually built-in with Python. `DetectorAPI` and `FacialExpressionModel` are custom classes, so ensure their respective `.py` files (`persondetection.py` and `facial_expression_model.py`) are in the same directory as `main.py` or in your Python path. You'll also need the pre-trained models (e.g., `.pb` files for TensorFlow detection, `.h5` for Keras models) that these classes would load. Ensure these model files are correctly placed according to your `persondetection.py` and `facial_expression_model.py` scripts.

4.  **Verify Asset Paths:**
    Ensure the `Images` folder is in the same directory as `main.py` and contains `icon.ico`, `front1.png`, `front2.png`, `Crowd_Report.png`, `image1.jpg`.
    Also, ensure the path for the facial expression detection script is correct:
    `r"D:\Kuliah\Semester Antara\KCD\Proyek Akhir\proyek akhir\facial-expression-detection-main\predict_expression\img.py"`
    It's recommended to make this relative if possible, or place `facial-expression-detection-main` alongside your current project.

## How to Run

1.  **Activate your virtual environment** (if you created one, as shown in Setup Step 2).
2.  **Navigate to the project's root directory** in your terminal where `main.py` is located.
3.  **Run the main application:**
    ```bash
    python main.py
    ```

## Usage

1.  **Main Window:**
    * Click "▶ START" to proceed to the main options.
    * Click "❌ EXIT" to close the application.

2.  **Options Window:**
    * **"DETECT HUMAN"**: Opens a new window for image-based human detection.
        * Click "SELECT" to choose an image file.
        * Click "PREVIEW" to see the selected image.
        * Click "DETECT" to run the human detection. The result (image with bounding boxes and counts) will be displayed in an OpenCV window, and a report will be generated.
    * **"DETECT EXPRESSION"**: Launches the separate facial expression detection script.
    * Click "❌ EXIT" to return to the previous window or close the application.

---

**Note on Absolute Paths:**
You currently have an absolute path in `main.py` for the initial window icon:
`window.iconbitmap(f'D:\Kuliah\Semester Antara\KCD\Proyek Akhir\proyek akhir\Real-Time-Human-Detection-Counting-main\Images\icon.ico')`
While this works on your machine, it will cause issues for others. It's recommended to change this to a relative path:
`window.iconbitmap('Images/icon.ico')`
Similarly, for the `subprocess.Popen` call for facial expression detection, consider making the path relative or ensuring the `facial-expression-detection-main` project is structured such that it can be launched easily by users.

---
