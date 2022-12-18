from concurrent.futures import ThreadPoolExecutor, wait
import subprocess
import threading
from customtkinter import CTkFrame, StringVar, filedialog
from pathlib import Path
import pytube
from PIL import Image
import customtkinter
import tkinter
from typing import Optional, Union,Tuple, Any
import requests
import ffmpeg
from tkinter.filedialog import askopenfile,askopenfilenames
from tkinter import ttk
import os
        
    # ffmpeg.output(
    #     ffmpeg.input(audio_path),
    #     ffmpeg.input(video_path),
    #     video_path.replace("temp_","")
    # ).run(overwrite_output=True)
    # import os
    # os.remove(video_path)
    # os.remove(audio_path)
    # video_stream = video.streams.filter(file_extension="mp4",only_audio=True if "audio" in yt_type else False)\
    #     .get_highest_resolution()

    # video_stream.download(directory,max_retries=3,skip_existing=True)
class ConcatPage(CTkFrame):
    filenames = []

    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None, border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent", fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None, background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None, overwrite_preferred_drawing_method: Union[str, None] = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        
        self.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
        self.grid_rowconfigure(( 0,1 ), weight=0)
        self.create_component()

    def show(self):
        self.grid(row=0,column=1,columnspan=5,rowspan=4, sticky="NSEW")

    def open_files(self):
        filenames = askopenfilenames(initialdir=self.download_path.get(),typevariable=self.filenames_input)        
        self.filenames = filenames
        if self.filenames:
            
            # try:
            #     self.tree_view.delete("videos")
            # except:
            #     print("no videos found")
            for index,filepath in enumerate(filenames):
                filename = os.path.basename(filepath)
                self.tree_view.insert('',index='end', values=(filename,filepath,), tags=('mp4',))
                self.tree_view.update_idletasks()
                self.tree_frame.update_idletasks()
        
        
    def create_component(self) -> Any:
        LABEL_COL= 0
        LABEL_SPAN=1
        TEXT_SPAN =4
        self.filenames_input = StringVar()
        ## Destination
        self.download_path = StringVar(value=str(Path(Path.home(),"Downloads")))
        self.files_label = customtkinter.CTkLabel(self,text="Files")
        self.files_label.grid(row=0,
                            column=LABEL_COL,
                            columnspan=LABEL_SPAN,
                            padx=(10, 0), pady=(20, 20), sticky=tkinter.W)
        
        self.files_text = customtkinter.CTkEntry(self,
                                    textvariable=self.download_path,
                                )
        self.files_text.grid(row=0,
                              column=LABEL_COL+1,
                              columnspan=TEXT_SPAN,
                              padx=(10, 0), pady=(20, 20),
                              sticky="we")
        self.browse_button = customtkinter.CTkButton(master=self,
                                                     command=self.open_files,
                                                     text="Browse")
        self.browse_button.grid(row=0,
                                column=LABEL_COL+1+TEXT_SPAN,                                
                                padx=(10, 20), pady=(20, 20),                             
                                sticky="nsew")
        self.delete_button = customtkinter.CTkButton(master=self,text="x",command=self.delete)        
        self.delete_button.grid(row=0,
                                column=LABEL_COL+1+TEXT_SPAN+1,                                
                                padx=(10, 20), pady=(20, 20),                             
                                sticky="nsew")        

        self._create_treeview()
        self.output_input = StringVar()
        self.output_path = StringVar(value=str(Path(Path.home(),"Downloads")))
        self.output_label = customtkinter.CTkLabel(self,text="Output filename")
        self.output_label.grid(row=2,
                            column=LABEL_COL,
                            columnspan=LABEL_SPAN,
                            padx=(10, 0), pady=(20, 20), sticky=tkinter.W)
        self.output_text = customtkinter.CTkEntry(self, textvariable=self.output_input)
        self.output_text.grid(row=2,
                              column=LABEL_COL+1,
                              columnspan=TEXT_SPAN,
                              padx=(10, 0), pady=(20, 20),
                              sticky="we"
                              )
        self.output_button = customtkinter.CTkButton(master=self,
                                                     command=self.output,
                                                     text="output")
        self.output_button.grid(row=2,
                                column=LABEL_COL+1+TEXT_SPAN,                                
                                padx=(10, 20), pady=(20, 20),                             
                                sticky="nsew")
        
        self.destination_label = customtkinter.CTkLabel(self,text="Destination :")
        self.destination_label.grid(row=3,
                            column=LABEL_COL,
                            columnspan=LABEL_SPAN,
                            padx=(10, 0), pady=(20, 20), sticky=tkinter.W)
        
        self.destination_text = customtkinter.CTkEntry(self,
                                    textvariable=self.output_path,
                                )
        self.destination_text.grid(row=3,
                              column=LABEL_COL+1,
                              columnspan=TEXT_SPAN,
                              padx=(10, 0), pady=(20, 20),
                              sticky="we")

        self.browse_button = customtkinter.CTkButton(master=self,
                                                     command=self.browse_directory_event,
                                                     text="Browse")
        self.browse_button.grid(row=3,
                                column=LABEL_COL+1+TEXT_SPAN,                                
                                padx=(10, 0), pady=(20, 20),                             
                                sticky="nsew")
        
        return 

    def _create_treeview(self) -> Any:
        self.style = ttk.Style()
        #Pick a theme
        self.style.theme_use("default")
        self.style.map("TView",
            foreground=[('pressed', 'red'), ('active', 'blue')],
            background=[('pressed', '!disabled', 'black'), ('active', 'white')]
        )
        ## Treeview Frame
        self.tree_frame = customtkinter.CTkFrame(self,
                                                 width=500,
                                                 height=500,
                                                 corner_radius=20, 
                                                 bg_color="transparent")
        self.tree_frame.grid(row=1,
                             pady=20, 
                             padx=20, 
                             columnspan=6)
        # Treeview Scrollbar        
        self.tree_scroll = tkinter.Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree_view = ttk.Treeview(self.tree_frame, columns=("filename","path"),
                                      displaycolumns=["filename","path"],
            height=30,
            yscrollcommand=self.tree_scroll.set,
            selectmode="extended",
            show='headings',
            padding=(10,5,20,30)
            # style="TView"
            
        )
        self.tree_view.column('filename',width=450,anchor=tkinter.CENTER)        
        self.tree_view.heading('filename',text='Filename')
        
        self.tree_view.column('path',width=850,anchor=tkinter.W,stretch=True)
        self.tree_view.heading('path',text='Path')

        self.tree_view.pack(fill=tkinter.BOTH)
        self.tree_scroll.config(command=self.tree_view.yview())

        
    def delete(self):
        for select in self.tree_view.selection():
            self.tree_view.delete(select)
    
    def output(self):
        if self.filenames:    
            with open(Path(self.output_path.get(),"tmp.txt"),"w+",encoding="utf-8") as f:
                f.writelines('\n'.join(map(lambda filename: f"file '{filename}'",self.filenames)))
            # ffmpeg_cmd_files = ''.join(map(lambda filename: f' -i "{filename}"', self.filenames))
            # print(ffmpeg_cmd_files)
            # 20221210 田夫仔 雞-01
            print(f'{Path(self.output_path.get(),"tmp.txt").absolute()}')
            print(f'ffmpeg -safe 0 -f concat -y -i "{Path(self.output_path.get(),"tmp.txt").absolute()}"  -c copy "{str(Path(self.output_path.get(),self.output_input.get()))}.mp4"')            
            threading.Thread(target=self.check_result).start()
            
    def check_result(self):
        process = subprocess.run(f'ffmpeg -safe 0 -f concat -y -i "{Path(self.output_path.get(),"tmp.txt").absolute()}"  -c copy "{str(Path(self.output_path.get(),self.output_input.get()))}.mp4"',check=True)
        process.check_returncode()
        tkinter.messagebox.showinfo(title="Success", message="Concated all files")
        os.remove(Path(self.output_path.get(),"tmp.txt"))
        
        
                        
        
    def browse_directory_event(self):
        output_director = filedialog.askdirectory(initialdir=self.download_path.get(), title="")
        self.output_path.set(output_director)
