
from customtkinter import (
    CTkFrame,
    CTkLabel,
    CTkFont,
    CTkButton
)
from typing import (
    Union,
    Tuple, 
    Optional,
    List,
    Dict,
    Callable
)

class SideBar(CTkFrame):

    buttons:Dict[int,CTkButton] = {}
    
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None, border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent", fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None, background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None, overwrite_preferred_drawing_method: Union[str, None] = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.grid_rowconfigure(4,weight=1)
        self.logo_label = CTkLabel(self.sidebar_frame, text="CustomTkinter", font=CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

    def create_button(command:Callable=None,)
    

    