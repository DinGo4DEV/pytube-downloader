import customtkinter
from app import App
from tkinter import PhotoImage
from pathlib import Path

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

if __name__ == "__main__":
    app = App()
    icon = PhotoImage(file=Path("assets/images/pytube_downloader_icon.png"))
    app.iconphoto(False,icon)
    app.mainloop()
    