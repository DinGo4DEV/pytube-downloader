import tkinter
from tkinter import StringVar
import tkinter.messagebox
import customtkinter
import validators
import time
import json
from PIL import Image
import asyncio
import threading
import requests
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor,wait,as_completed
import pytube
from pathlib import Path
from tkinter import messagebox, filedialog
from pages.downloader_page import DownloadPage
from pages.concat_page import ConcatPage
# import ffmpeg
import os


def _asyncio_thread(async_loop,task):
    async_loop.run_until_complete(task)


def do_tasks(async_loop,task):
    """ Button-Event-Handler starting the asyncio part. """
    threading.Thread(target=_asyncio_thread, args=(async_loop,task)).start()

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
    

class App(customtkinter.CTk):
    videos = []
    yt_videos={}
    def __init__(self):
         videos = []
    yt_videos={}
    def __init__(self):
        super().__init__()
        self.task_loop = asyncio.get_event_loop_policy().new_event_loop()

        # configure window
        self.title("PyTube Downloader")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure((2, 3,4,5), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure(( 2, 3, 4), weight=0)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="",image=customtkinter.CTkImage(light_image=Image.open("assets/images/pytube_downloader_icon.png"),dark_image=Image.open("assets/images/pytube_downloader_icon.png"),size=(189,189)), font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.download_page_button_event, text="YT下載")
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_concat_page_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.concat_page_button_event, text="合拼影片")
        self.sidebar_concat_page_2.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        MAIN_WIDTH, MAIN_HEIGHT = 700, 300
        
        self.main = DownloadPage(master=self,corner_radius=20,bg_color="transparent",fg_color="transparent")
        # self.main.grid(row=0,column=1,columnspan=5,rowspan=4, sticky="NSEW")
        # self.main.grid_columnconfigure(1, weight=0)
        # self.main.grid_columnconfigure((0,1,2,3,4,5), weight=1)
        # self.main.grid_rowconfigure((0, 1), weight=1)
        # self.main.grid_rowconfigure(( 2, 3, 4), weight=0)
        self.main.update()
        # self.main.grid(row=0,column=1,columnspan=5,rowspan=4, sticky="NSEW")
        # self.main.grid_columnconfigure(1, weight=0)
        # self.main.grid_columnconfigure((2, 3,4,5), weight=1)
        # self.main.grid_rowconfigure((0, 1), weight=1)
        # self.main.grid_rowconfigure(( 2, 3, 4), weight=0)
        
        self.concat_page = ConcatPage(master=self,width=MAIN_WIDTH,height=MAIN_HEIGHT,corner_radius=20,bg_color="transparent",fg_color="transparent")
        # self.concat_page.grid(row=0,column=1,columnspan=5,rowspan=4, sticky="NSEW")
        # self.concat_page.grid_columnconfigure(1, weight=0)
        # self.concat_page.grid_columnconfigure((2, 3,4,5), weight=1)
        # self.concat_page.grid_rowconfigure((0, 1), weight=1)
        # self.concat_page.grid_rowconfigure(( 2, 3, 4), weight=0)

        self.scaling_optionemenu.set("100%")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")
        
    def download_page_button_event(self):
        self.concat_page.grid_forget()
        self.main.show()
        
    def concat_page_button_event(self):
        self.main.grid_forget()
        self.concat_page.show()

    # def browse_directory_event(self):
    #     download_director = filedialog.askdirectory(initialdir=self.download_path.get(), title="")
    #     self.download_path.set(download_director)        

    # ## https://www.youtube.com/playlist?list=PLcN7SpsPS3WSqTVsyvyaTCDTeO9qDFW02
    # def donwload_button_event(self):
        
    #     print("download button clicked")
    #     url = self.yt_url_text.get()
    #     if not url:
    #         print("No value provided")
    #     else:
    #         url = url.strip()
    #         if not validators.url(url):
    #             print("not valid url")
    #         # loop = asyncio.get_event_loop_policy().new_event_loop()
    #         threading.Thread(target=self.extract_info,args=(url,)).start()
    #         # future = asyncio.run_coroutine_threadsafe(,loop=loop)            
    #         # future = loop.run_until_complete(self.extract_info(url))
    #         # future.add_done_callback(
    #         #     self.after_idle(self.textbox.update)
    #         # )
    #         print("call url")

    # def extract_info(self,url):
    #     thumbnails = {}
    #     self.videos = []
    #     self.yt_videos = {}
    #     try:            
    #         playlist = pytube.Playlist(url)
    #         for video in playlist.videos: 
    #             self.yt_videos[video.video_id] = video
    #             thumbnails[video.video_id] = video.thumbnail_url
                    
    #     except (pytube.exceptions.RegexMatchError,KeyError) as exc:
    #         video = pytube.YouTube(url)
    #         self.yt_videos[video.video_id] = video
    #         thumbnails[video.video_id] = video.thumbnail_url
            
    #     with ThreadPoolExecutor( ) as exc:            
    #         raw_contents = exc.map(get_thumbnails,thumbnails.items())    
    #         for id,content in raw_contents:
    #             image =Image.open(content)
    #             i = customtkinter.CTkImage(light_image=image,
    #                             dark_image=image,
    #                             size=(162, 98))
    #             # tk_image = customtkinter.CTkButton(self.tabview.tab("List"), image=i)
                
    #             tk_image = customtkinter.CTkButton(self.main_canvas, image=i,text=id)
    #             # tk_image.pack(expand=True)
    #             self.videos.append(tk_image)
        
    #     self.donwload()
                
    # def donwload(self):
    #     tasks = {}
    #     directory = self.download_path.get()
    #     yt_type = self.yt_type_var.get()        
    #     with ThreadPoolExecutor(max_workers=os.cpu_count()//2 or 1) as exc:            
    #         for v in self.yt_videos.values():
    #             future = exc.submit(download_yt,v,yt_type,directory)
    #             tasks[future] = v.title
    #             future.add_done_callback(lambda x: print(f"finished file: {tasks.get(x,None)}"))
                
    #     wait(tasks.keys())
    #     tkinter.messagebox.showinfo(title="Success", message="Donwloaded all files")