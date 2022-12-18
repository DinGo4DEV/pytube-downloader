import customtkinter
from app import App
from tkinter import PhotoImage
from pathlib import Path
from logging import getLogger
import logging
import logging.handlers

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

if __name__ == "__main__":
    root = getLogger()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logging.basicConfig(filename='output.log', encoding='utf-8', level=logging.DEBUG)
    filehandler = logging.handlers.TimedRotatingFileHandler("output.log","D",1,1)
    filehandler.suffix="%Y%m%d.log"
    root.addHandler(filehandler)
    try:
        app = App()
        icon = PhotoImage(file=Path("assets/images/pytube_downloader_icon.png"))
        app.iconphoto(False,icon)
        app.mainloop()
    except Exception as e:
        root.exception("error",exc_info=e)
        
    