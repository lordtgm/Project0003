from __future__ import annotations

import contextlib
import os
from tkinter import TclError, Tk, Toplevel
from tkinter.ttk import Button, Entry, Frame, Label, Progressbar, Spinbox, Style
from PIL import Image, ImageTk
from drawing import generate_timer
from pathlib import Path

bundle_dir = Path.cwd().parent  # Path(__file__).parent
resourcepath = Path.cwd() / bundle_dir / "resources"


@contextlib.contextmanager
def working_directory(path):
    """Changes working directory and returns to previous on exit."""
    prev_cwd = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


class Settings:
    def __init__(self, parent: App):
        self.app = parent
        self.root = Toplevel(parent.root)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.frame = Frame(self.root)
        self.frame.grid()

        self.label = Label(self.frame, text="Enter time and title", font=("Lava Arabic", 20))
        self.label.grid(column=0, row=0, columnspan=3)

        self.hours_label = Label(self.frame, text="Hours", font=("Lava Arabic", 20))
        self.hours_label.grid(column=0, row=1)
        self.minutes_label = Label(self.frame, text="Minutes", font=("Lava Arabic", 20))
        self.minutes_label.grid(column=1, row=1)
        self.seconds_label = Label(self.frame, text="Seconds", font=("Lava Arabic", 20))
        self.seconds_label.grid(column=2, row=1)

        self.hours = Spinbox(self.frame, from_=0, to=11, width=5)
        self.hours.set(0)
        self.hours.grid(column=0, row=2)
        self.minutes = Spinbox(self.frame, from_=0, to=59, width=5)
        self.minutes.set(0)
        self.minutes.grid(column=1, row=2)
        self.seconds = Spinbox(self.frame, from_=0, to=59, width=5)
        self.seconds.set(0)
        self.seconds.grid(column=2, row=2)

        self.title = Entry(self.frame, font=("Lava Arabic", 15))
        self.title.grid(column=0, row=3)

        self.ok_button = Button(self.frame, text="OK", command=self.ok)
        self.ok_button.grid(column=2, row=3)

    def ok(self):
        self.app.total_time = int(self.hours.get()) * 3600 + int(self.minutes.get()) * 60 + int(self.seconds.get())
        self.app.current_time = 0
        self.app.update_time_label()
        self.app.title.configure(text=self.title.get())
        self.close()

    def close(self):
        self.root.destroy()
        self.app.root.attributes("-topmost", True)


class App:
    def __init__(self):
        self.total_time = 10
        self.current_time = 0
        self.running = False

        self.root = Tk(screenName="Timer")
        self.root.title("Timer")

        self.style = Style()
        self.style.configure(".", background="#292929")

        self.load_extrafont()
        self.frame = Frame(self.root)
        self.frame.grid_configure()

        self.heart_image = ImageTk.PhotoImage(Image.open(resourcepath / "heart.png").resize((50, 50)))
        self.heart = Label(self.frame, image=self.heart_image)
        self.heart.grid(column=0, row=0)

        self.ans_image = ImageTk.PhotoImage(Image.open(resourcepath / "ans.png").resize((50, 50)))
        self.ans = Label(self.frame, image=self.ans_image)
        self.ans.grid(column=1, row=0)

        self.root.tk.call("extrafont::load", resourcepath / "Lava.ttf")
        self.title = Label(self.frame, text="Title", font=("Lava Arabic", 25))
        self.title.grid(column=2, row=0)

        self.pause_image = ImageTk.PhotoImage(Image.open(resourcepath / "pause.png").resize((50, 50)))
        self.pause = Button(self.frame, image=self.pause_image, command=self.pause, style="TLabel")
        self.pause.grid(column=0, row=1)

        self.play_image = ImageTk.PhotoImage(Image.open(resourcepath / "play.png").resize((50, 50)))
        self.play = Button(self.frame, image=self.play_image, command=self.play, style="TLabel")
        self.play.grid(column=1, row=1)

        self.gear_image = ImageTk.PhotoImage(Image.open(resourcepath / "gear.png").resize((50, 50)))
        self.settings = Button(self.frame, image=self.gear_image, command=self.settings, style="TLabel")
        self.settings.grid(column=3, row=0)

        self.time_image = ImageTk.PhotoImage(generate_timer(100, 60, 5, 36, 36).resize((50, 50)))
        self.time = Label(self.frame, image=self.time_image)
        self.time.grid(column=3, row=1)

    def pause(self):
        self.running = False

    def play(self):
        if self.running:
            return
        if self.current_time >= self.total_time:
            self.current_time = 0
        self.running = True
        self.run()

    def run(self):
        if self.running and self.current_time < self.total_time:
            self.current_time += 1
            self.update_time_label()
            remaining_time = self.total_time - self.current_time
            self.root.after(1000, self.run)

    def settings(self):
        if self.running:
            return
        self.root.attributes("-topmost", False)
        Settings(self)

    def update_time_label(self):
        self.time_image = ImageTk.PhotoImage(
            generate_timer(100, 60, 5, 36, 36 - (self.current_time * 36 // self.total_time)).resize((50, 50)))
        self.time.configure(image=self.time_image)
        self.time.update()

    def load_extrafont(self):
        with working_directory(resourcepath):
            self.root.tk.eval("source pkgIndex.tcl")
            try:
                self.root.tk.eval("package require extrafont")
            except TclError as e:
                if "libfontconfig" in e.message:
                    raise TclError(
                        "Could not load extrafont due to missing fontconfig - See issue #1 on GitHub: "
                        "<https://github.com/TkinterEP/python-tkextrafont/issues/1>")

    def main(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = App()
    app.main()
