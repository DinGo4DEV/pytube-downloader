# pytube-downloader

[![PyPI - Version](https://img.shields.io/pypi/v/pytube-downloader.svg)](https://pypi.org/project/pytube-downloader)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pytube-downloader.svg)](https://pypi.org/project/pytube-downloader)

-----

**Table of Contents**

- [pytube-downloader](#pytube-downloader)
  - [Installation](#installation)
  - [License](#license)
  - [Build](#build)
    - [nuitka](#nuitka)
    - [pyinstaller](#pyinstaller)

## Installation

```console
pip install pytube-downloader
```

## License

`pytube-downloader` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Build


### nuitka

1. install nuitka with pip. `pip install nuitka`
2. cd to pytube_downloader
3. `C:\Users\{username}\AppData\Local\Programs\Python\Python310\python.exe -m nuitka --follow-imports --enable-plugin=tk-inter --enable-plugin=numpy --include-package=customtkinter  --windows-icon-from-ico=assets\images\pytube_downloader_icon.png --windows-company-name=devhk --windows-product-name="pytube-downloader" --windows-product-version=0001 --standalone .\pytube_downloader.py`


### pyinstaller

```
pyinstaller --noconfirm --onedir  --add-data "C:\Users\$username\AppData\Local\Programs\Python\Python311\Lib\site-packages\customtkinter;customtkinter\" --paths "d:\git\pytube-downloader\pytube_downloader" --icon "{base_path}\pytube-downloader\pytube_downloader\assets\images\pytube_downloader_icon.png" .\pytube_downloader.py
```