import sys
import cx_Freeze
import PySide
import praw
import requests.certs
import requests
from cx_Freeze import setup, Executable

exe = Executable(
      script="WallDit_QT.pyw",
      base="Win32GUI",
      targetName="WallDit_QT.exe"
     )

setup(name = 'WallDit_QT',
    version = '1.0',
    author = 'Disco Dolan',
    description ='Set your wallpaper interactively!',
    executables = [exe],
    options = {
        'build_exe': {
            "include_files": [
                (requests.certs.where(),'cacert.pem'), 
                'praw.ini', 
                'README.md'
            ]
        }
    },
    requires = ['PySide', 'cx_Freeze', 'praw', 'shutil', 'requests']
)