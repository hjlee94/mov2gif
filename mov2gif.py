#! python

from moviepy.editor import VideoFileClip
from tkinter.filedialog import askopenfilename, asksaveasfilename

from PIL import ImageTk, Image

from tkinter import Tk
from tkinter import ttk
import os

class Window(Tk):
    def __init__(self):
        super().__init__()

        self.title("MOV to GIF")

        self.button_open = ttk.Button(text="Open", command=self.handle_open)
        self.button_open.pack()

        self.label_path = ttk.Label(text="")
        self.label_path.pack()

        self.preview = ttk.Label()
        self.preview.pack()

        self.clip = None
        self.preview_img = None

        self._fps = 10
        self.label_fps = ttk.Label(text=f"FPS: {self._fps}")
        self.label_fps.pack()

        self.slider = ttk.Scale(from_=10, to=60, command=self.handle_slider)
        self.slider.pack()

        self.button_convert = ttk.Button(text="Convert", command=self.handle_convert)
        self.button_convert.pack()

        self.label_status = ttk.Label(text="")
        self.label_status.pack()

    def handle_slider(self, val):
        val = int(val.split('.')[0])
        self._fps = val
        self.label_fps.config(text=f"FPS: {str(self._fps)}")

    def handle_open(self):
        in_path = askopenfilename(defaultextension="mov")

        if not in_path:
            return
        
        in_path = os.path.abspath(in_path)
        
        self.label_path.config(text=in_path)

        self.clip = VideoFileClip(in_path)
        img = Image.fromarray(self.clip.get_frame(0))
        
        if img.height > 100:
            img = img.resize((img.width * 100 // img.height, 100))
        
        self.preview_img = ImageTk.PhotoImage(image=img, size=10)
        self.preview.config(image=self.preview_img)

    def handle_convert(self):
        out_path = asksaveasfilename(defaultextension="gif", initialfile="output", initialdir=os.path.expanduser("~/Downloads"))
        
        self.label_status.config(text="processing...")
        try:
            self.clip.write_gif(out_path, fps=self._fps, loop=0)
            self.label_status.config(text="succeeded")

        except:
            self.label_status.config(text="failed")

# Start the event loop.
window = Window()
window.minsize(200,200)
window.mainloop()