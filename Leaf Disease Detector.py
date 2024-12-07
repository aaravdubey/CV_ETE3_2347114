from tkinter import filedialog, PhotoImage
import cv2
import sys
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

# Function to process the input image
def ProcessImage():
    try:
        # Load the selected image
        OriginalImage = cv2.imread(filename, 1)
        cv2.imshow("Original Image", OriginalImage)

        # Split the image into Blue, Green, and Red channels
        b = OriginalImage[:, :, 0]
        g = OriginalImage[:, :, 1]
        r = OriginalImage[:, :, 2]

        # Display individual color channels
        cv2.imshow("Red Channel", r)
        cv2.imshow("Green Channel", g)
        cv2.imshow("Blue Channel", b)

        # Calculate the Disease channel (difference between red and green channels)
        Disease = r - g

        # Initialize the Alpha channel globally
        global Alpha
        Alpha = b

        # Generate the Alpha channel
        GetAlpha(OriginalImage)
        cv2.imshow("Alpha Channel", Alpha)

        # Get the Processing Factor from the slider
        ProcessingFactor = slider.get()

        # Apply processing logic to the Disease channel
        for i in range(OriginalImage.shape[0]):
            for j in range(OriginalImage.shape[1]):
                if int(g[i, j]) > ProcessingFactor:
                    Disease[i, j] = 255

        # Display the processed Disease image
        cv2.imshow("Disease Image", Disease)

        # Calculate and display the disease percentage
        DisplayDiseasePercentage(Disease)
        status_bar["text"] = "Processing complete."
    except Exception as e:
        # Display error in the status bar if any exception occurs
        status_bar["text"] = f"Error: {e}"

# Function to generate the Alpha channel based on color threshold
def GetAlpha(OriginalImage):
    global Alpha
    for i in range(OriginalImage.shape[0]):
        for j in range(OriginalImage.shape[1]):
            # Check if the pixel is close to white (high intensity in all channels)
            if OriginalImage[i, j, 0] > 200 and OriginalImage[i, j, 1] > 200 and OriginalImage[i, j, 2] > 200:
                Alpha[i, j] = 255
            else:
                Alpha[i, j] = 0

# Function to select an image file using a file dialog
def GetFile():
    global filename
    filename = filedialog.askopenfilename(title="Select Image", filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
    if filename:
        # Update the status bar with the selected file
        status_bar["text"] = f"File loaded: {filename}"
        DisplayImagePreview(filename)
    else:
        status_bar["text"] = "No file selected."

# Function to display a preview of the selected image
def DisplayImagePreview(image_path):
    img = Image.open(image_path)
    img.thumbnail((300, 300))
    img_tk = ImageTk.PhotoImage(img)
    image_preview_label.config(image=img_tk)
    image_preview_label.image = img_tk

# Function to calculate and display the disease percentage
def DisplayDiseasePercentage(Disease):
    Count = 0
    Res = 0

    # Iterate through the image to count relevant pixels
    for i in range(Disease.shape[0]):
        for j in range(Disease.shape[1]):
            if Alpha[i, j] == 0:  # Count pixels in non-white areas
                Res += 1
            if Disease[i, j] < slider.get():  # Count pixels below the threshold
                Count += 1

    # Calculate the percentage of diseased pixels
    Percent = (Count / Res) * 100 if Res > 0 else 0
    disease_percent_label["text"] = f"Disease Percentage: {round(Percent, 2)}%"

# Global variables
Alpha = None
filename = ""

# Main window setup
MainWindow = tk.Tk()
MainWindow.title("Plant Disease Detector by Shrey Gupta And Aarav Dubey")
MainWindow.geometry("800x600")
MainWindow.configure(bg="#eef7ff")

# Header label
header_label = tk.Label(
    MainWindow, text="Plant Disease Detector", font=("Helvetica", 20, "bold"), bg="#1e81b0", fg="white", pady=10
)
header_label.pack(fill="x")

# Control frame for slider
control_frame = tk.Frame(MainWindow, bg="#eef7ff", pady=10)
control_frame.pack()

slider_label = tk.Label(
    control_frame, text="Processing Factor", font=("Helvetica", 12), bg="#eef7ff", fg="#333"
)
slider_label.grid(row=0, column=0, padx=10)

slider = ttk.Scale(control_frame, from_=0, to=255, length=400, orient="horizontal")
slider.grid(row=0, column=1, padx=10)
slider.set(150)

# Button frame for file selection and processing
button_frame = tk.Frame(MainWindow, bg="#eef7ff")
button_frame.pack(pady=10)

select_image_button = ttk.Button(
    button_frame, text="Select Image", command=GetFile, style="Accent.TButton"
)
select_image_button.grid(row=0, column=0, padx=10)

process_button = ttk.Button(
    button_frame, text="Process Image", command=ProcessImage, style="Accent.TButton"
)
process_button.grid(row=0, column=1, padx=10)

# Label to preview the selected image
image_preview_label = tk.Label(MainWindow, bg="#eef7ff")
image_preview_label.pack(pady=10)

# Label to display the calculated disease percentage
disease_percent_label = tk.Label(
    MainWindow, text="Disease Percentage: N/A", font=("Helvetica", 14), bg="#eef7ff", fg="#333"
)
disease_percent_label.pack(pady=10)

# Status bar to display messages
status_bar = tk.Label(MainWindow, text="Select an image to begin.", bg="#1e81b0", fg="white", anchor="w", font=("Helvetica", 10))
status_bar.pack(side="bottom", fill="x")

# Styling for buttons
style = ttk.Style()
style.configure("Accent.TButton", font=("Helvetica", 12), background="#1e81b0", foreground="white")
style.configure("TButton", padding=5)

# Run the main event loop
MainWindow.mainloop()