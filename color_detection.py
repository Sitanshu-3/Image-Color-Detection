import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
from colorthief import ColorThief
import colorsys

# ---------- Helper Functions ----------

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def brightness(rgb):
    r, g, b = rgb
    return colorsys.rgb_to_hsv(r/255, g/255, b/255)[2]

# ---------- Main App ----------

class ColorDetectApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Color Detection - Enhanced")
        self.geometry("800x600")
        self.configure(bg="#2e2e2e")  # Dark modern background
        
        # Image Label
        self.image_label = tk.Label(self, text="Upload an image", bg="#2e2e2e", fg="white", font=("Helvetica", 14))
        self.image_label.pack(pady=10)

        # Upload Button
        self.btn_upload = ttk.Button(self, text="Upload Image", command=self.upload_image)
        self.btn_upload.pack(pady=5)

        # Sort checkbox
        self.sort_var = tk.IntVar(value=1)
        self.chk_sort = ttk.Checkbutton(self, text="Sort by Brightness", variable=self.sort_var, command=self.show_colors)
        self.chk_sort.pack(pady=5)

        # Colors Frame
        self.colors_frame = tk.Frame(self, bg="#2e2e2e")
        self.colors_frame.pack(fill='both', expand=True, padx=20, pady=20)

        self.img_path = None
        self.colors = []

        # Style for ttk buttons and checkbox
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', background="#4a90e2", foreground="white", font=("Helvetica", 12), padding=6)
        style.map('TButton', background=[('active', '#357ABD')])
        # Checkbox style (hover effect removed)
        style.configure('TCheckbutton', background="#2e2e2e", foreground="white", font=("Helvetica", 12))
        style.map('TCheckbutton', background=[('active', '#2e2e2e')], foreground=[('active', 'white')])

    # ---------- Upload Image ----------
    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
        if not path:
            return
        self.img_path = path
        img = Image.open(path)
        img.thumbnail((400, 400))
        self.img_display = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.img_display, text="")
        self.extract_colors()

    # ---------- Extract Colors ----------
    def extract_colors(self):
        if not self.img_path:
            return
        ct = ColorThief(self.img_path)
        self.colors = ct.get_palette(color_count=10)
        self.show_colors()

    # ---------- Show Colors ----------
    def show_colors(self):
        for widget in self.colors_frame.winfo_children():
            widget.destroy()

        colors = self.colors.copy()
        if self.sort_var.get():
            colors.sort(key=brightness, reverse=True)

        container = tk.Frame(self.colors_frame, bg="#2e2e2e")
        container.pack(expand=True)

        num_columns = 5
        for idx, color in enumerate(colors):
            hex_code = rgb_to_hex(color)
            frame = tk.Frame(container, bg=hex_code, width=120, height=60, bd=2, relief="ridge")
            frame.grid(row=idx//num_columns, column=idx%num_columns, padx=8, pady=8)
            label = tk.Label(frame, text=f"RGB: {color}\nHEX: {hex_code}",
                             bg=hex_code, fg="white" if brightness(color)<0.5 else "black",
                             font=("Helvetica", 10, "bold"))
            label.pack(expand=True, fill='both')

        for i in range(num_columns):
            container.grid_columnconfigure(i, weight=1)

# ---------- Run ----------
if __name__ == "__main__":
    app = ColorDetectApp()
    app.mainloop()
