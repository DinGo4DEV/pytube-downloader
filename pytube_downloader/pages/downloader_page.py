from concurrent.futures import ThreadPoolExecutor, wait
import threading
from customtkinter import CTkFrame, StringVar, filedialog
from pathlib import Path
import pytube
from PIL import Image
import customtkinter
import tkinter
from typing import Optional, Union,Tuple, Any
import requests
import validators

def get_thumbnails(data):
    key,thumbnail_url = data
    raw = requests.get(thumbnail_url,stream=True).raw
    return (key,raw)

def _download_1080_video(video:pytube.YouTube,directory):
    return video.streams.filter(res="1080p", progressive=False).first().download(directory,max_retries=3,skip_existing=True)

def _download_1080_audio(video:pytube.YouTube,directory):
    return video.streams.filter(abr="160kbps", progressive=False).first().download(directory,max_retries=3,skip_existing=True)

def download_yt(video: pytube.YouTube,yt_type,directory):                
    with ThreadPoolExecutor() as exc:
        audio_path_future = exc.submit(_download_1080_audio,video,directory)
        video_path_future = exc.submit(_download_1080_video,video,directory)
        done, not_complete  = wait([audio_path_future,video_path_future])
        video_path = video_path_future.result()
        audio_path = audio_path_future.result()
        
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
class DownloadPage(CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None, border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent", fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None, background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None, overwrite_preferred_drawing_method: Union[str, None] = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.show()
        # self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure((0,1,2,3,4,5,6), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure(( 2, 3, 4), weight=0)
        self.create_component()
    
    def show(self):
        self.grid(row=0,column=1,columnspan=5,rowspan=4, sticky="NSEW")
        
    def create_component(self) -> Any:
        LABEL_COL= 0
        LABEL_SPAN=1
        TEXT_SPAN =5
        ## Destination
        self.download_path = StringVar(value=str(Path(Path.home(),"Downloads")))
        self.destination_label = customtkinter.CTkLabel(self,text="Destination :")
        self.destination_label.grid(row=2,
                            column=LABEL_COL,
                            columnspan=LABEL_SPAN,
                            padx=(10, 0), pady=(20, 20), sticky=tkinter.W)
        
        self.destination_text = customtkinter.CTkEntry(self,
                                    textvariable=self.download_path,
                                )
        self.destination_text.grid(row=2,
                              column=LABEL_COL+1,
                              columnspan=TEXT_SPAN,
                              padx=(10, 0), pady=(20, 20),
                              sticky="we")
        self.browse_button = customtkinter.CTkButton(master=self,
                                                     command=self.browse_directory_event,
                                                     text="Browse")
        self.browse_button.grid(row=2,
                                column=LABEL_COL+1+TEXT_SPAN,                                
                                padx=(10, 0), pady=(20, 20),                             
                                sticky="nsew")
        
        ## Youtube URL
        self.yt_url_label = customtkinter.CTkLabel(self,text="Youtube URL :")
        self.yt_url_label.grid(row=3,
                            column=LABEL_COL,
                            columnspan=LABEL_SPAN,
                            padx=(10, 0), pady=(20, 20), sticky=tkinter.W)
        self.yt_url_text = customtkinter.CTkEntry(self, placeholder_text="youtube video url or playlist")
        self.yt_url_text.grid(row=3,
                              column=LABEL_COL+1,
                              columnspan=TEXT_SPAN,
                              padx=(10, 0), pady=(20, 20),
                              sticky="nsew")
        YT_TYPE_OPTIONS = [
            "mp4/best",
            "audio/best",            
        ]
        self.yt_type_var = customtkinter.StringVar(value=YT_TYPE_OPTIONS[0])
        self.yt_type_option = customtkinter.CTkOptionMenu(master=self,
                                       values=YT_TYPE_OPTIONS,
                                       variable=self.yt_type_var)
        self.yt_type_option.grid(row=3, column=LABEL_COL+1+TEXT_SPAN, padx=(10, 0), pady=(20, 20), sticky="nsew")
        self.download_button = customtkinter.CTkButton(master=self, text="Download", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"),command=self.donwload_button_event)
        self.download_button.grid(row=3, column=LABEL_COL+1+TEXT_SPAN+1, padx=(10, 10), pady=(20, 20), sticky="nsew")
        
        self.yt_url_text.setvar("write","https://www.youtube.com/playlist?list=PLcN7SpsPS3WSqTVsyvyaTCDTeO9qDFW02")
        return 
    
    
    ## https://www.youtube.com/playlist?list=PLcN7SpsPS3WSqTVsyvyaTCDTeO9qDFW02
    def donwload_button_event(self):
        
        print("download button clicked")
        url = self.yt_url_text.get()
        if not url:
            print("No value provided")
        else:
            url = url.strip()
            if not validators.url(url):
                print("not valid url")
            # loop = asyncio.get_event_loop_policy().new_event_loop()
            threading.Thread(target=self.extract_info,args=(url,)).start()
            # future = asyncio.run_coroutine_threadsafe(,loop=loop)            
            # future = loop.run_until_complete(self.extract_info(url))
            # future.add_done_callback(
            #     self.after_idle(self.textbox.update)
            # )
            print("call url")

    def extract_info(self,url):
        thumbnails = {}
        self.videos = []
        self.yt_videos = {}
        try:            
            playlist = pytube.Playlist(url)
            for video in playlist.videos: 
                self.yt_videos[video.video_id] = video
                thumbnails[video.video_id] = video.thumbnail_url
                    
        except (pytube.exceptions.RegexMatchError,KeyError) as exc:
            video = pytube.YouTube(url)
            self.yt_videos[video.video_id] = video
            thumbnails[video.video_id] = video.thumbnail_url
            
        with ThreadPoolExecutor( ) as exc:            
            raw_contents = exc.map(get_thumbnails,thumbnails.items())    
            for id,content in raw_contents:
                image =Image.open(content)
                i = customtkinter.CTkImage(light_image=image,
                                dark_image=image,
                                size=(162, 98))
                # tk_image = customtkinter.CTkButton(self.tabview.tab("List"), image=i)
                
                tk_image = customtkinter.CTkButton(self, image=i,text=id)
                # tk_image.pack(expand=True)
                self.videos.append(tk_image)
        
        self.donwload()
        
    def browse_directory_event(self):
        download_director = filedialog.askdirectory(initialdir=self.download_path.get(), title="")
        self.download_path.set(download_director)   
                
    def donwload(self):
        tasks = {}
        directory = self.download_path.get()
        yt_type = self.yt_type_var.get()        
        with ThreadPoolExecutor() as exc:            
            for v in self.yt_videos.values():
                future = exc.submit(download_yt,v,yt_type,directory)
                tasks[future] = v.title
                future.add_done_callback(lambda x: print(f"finished file: {tasks.get(x,None)}"))
                
        wait(tasks.keys())
        tkinter.messagebox.showinfo(title="Success", message="Donwloaded all files")