import youtube_dl
# from .logging import getLogger
from logging import getLogger
import logging

logging.basicConfig()


class PyTubeDonwloader(youtube_dl.YoutubeDL):   
    logger = getLogger(__name__)
    logger.setLevel(0)    
    


    ydl_opts:dict

    def __init__(self, params=None, auto_init=True):
        if params != None:
            self.ydl_opts = params
        else:
            self.ydl_opts = {
            'format': 'best',
            # 'postprocessors': [{
            #     'key': 'FFmpegExtractAudio',
            #     'preferredcodec': 'mp3',
            #     'preferredquality': '192',
            # }],
            # 'logger': self.logger,
            # 'progress_hooks': [self.hook],
        }
        super().__init__(self.ydl_opts, auto_init)        

    @classmethod
    def hook(cls,d):
        if d['status'] == 'finished':
            print('Done downloading, now converting ...')
    
    

