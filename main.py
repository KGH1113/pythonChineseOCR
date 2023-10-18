import pytesseract
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

class ChineseOCR:
    def __init__(self, root):
        self.root = root
        self.root.title("ChineseOCR")
        self.root.geometry("800x600")

        self.button = tk.Button(root, text="Open Image File", command=self.open_file_dialog)
        self.button.pack()

        self.selected_file_label = tk.Label(root, text="No file selected")
        self.selected_file_label.pack()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.selected_file_label.config(text="Result:\n" + self.extract(file_path))
        else:
            self.selected_file_label.config(text="No file selected")


    def extract(self, fileLocation):
        # TESSDATA_PREFIX environment var
        os.environ["TESSDATA_PREFIX"] = "./assets/"

        # Open the config file.
        with open("./assets/config.txt", "r") as configFile:
            content = configFile.read()
            # location of Tesseract OCR engine.
            pytesseract.pytesseract.tesseract_cmd = r"{0}".format(content.split("===")[1])  # Windows only

        # Load the image file.
        image = Image.open(fileLocation)

        text = pytesseract.image_to_string(image, lang='chi_sim')

        print(text)
        return text

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChineseOCR(root)
    app.run()
