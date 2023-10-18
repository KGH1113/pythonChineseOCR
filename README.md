import pytesseract
from PIL import Image
import os
import tkinter as tk
from tkinter import filedialog

class OCRProgram:
    def __init__(self, root):
        self.root = root
        self.root.title("OCR Program for Chinese")
        self.root.geometry("800x900")

        self.create_header()
        self.create_file_selection()

    def create_header(self):
        header_frame = tk.Frame(self.root)
        header_frame.pack()

        title_label = tk.Label(header_frame, text="OCR Program for ")
        title_label.pack()

        red_label = tk.Label(header_frame, text="Chinese", fg="#FF3636")
        red_label.pack()

    def create_file_selection(self):
        main_frame = tk.Frame(self.root)
        main_frame.pack()

        self.file_frame = tk.Frame(main_frame, width=500, height=400, relief="solid", borderwidth=2)
        self.file_frame.pack(pady=20)

        file_label = tk.Label(self.file_frame, text="+", font=("Helvetica", 200), cursor="hand2")
        file_label.pack(pady=50)
        file_label.bind("<Button-1>", self.open_file_dialog)

    def open_file_dialog(self, event):
        self.file_path = filedialog.askopenfilename(title="Select a file")
        if self.file_path:
            self.load_loading_page()

    def load_loading_page(self):
        self.file_frame.destroy()

        self.loading_frame = tk.Frame(self.root, width=500, height=400, borderwidth=0, relief="solid", bg="white")
        self.loading_frame.pack()

        self.loading_bar_frame = tk.Frame(self.loading_frame, width=500, height=400)
        self.loading_bar_frame.pack()

        self.loading_bar = tk.Frame(self.loading_bar_frame, width=0, height=50, borderwidth=0, relief="solid", bg="red")
        self.loading_bar.pack(pady=20)

        self.update_loading_bar()

        loading_label = tk.Label(self.loading_frame, text="Loading...")
        loading_label.pack()

    def update_loading_bar(self):
        current_width = self.loading_bar.winfo_width()
        if current_width < 500:
            self.loading_bar.config(width=current_width + 10)
            self.root.after(100, lambda: self.update_loading_bar())
        else:
            self.load_result_page()

    def load_result_page(self):
        self.loading_frame.destroy()
        self.loading_bar_frame.destroy()
        self.loading_bar.destroy()

        result_frame = tk.Frame(self.root)
        result_frame.pack()

        result_label = tk.Label(result_frame, text="OCR Result:\n\n{0}".format(self.extract(self.file_path)), font=("Helvetica", 20))
        result_label.pack()

        goto_home_label = tk.Button(result_frame, text="Main Page")
        goto_home_label.bind("<Button-1>", self.create_file_selection)
        goto_home_label.pack()

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

def main():
    root = tk.Tk()
    app = OCRProgram(root)
    root.mainloop()

if __name__ == "__main__":
    main()
