import customtkinter
from app import App

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

if __name__ == "__main__":
    app = App()
    app.mainloop()
    