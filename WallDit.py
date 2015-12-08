import praw
import requests
import shutil
import ctypes
import ctypes.wintypes
import os
import time
from win32com.shell import shell, shellcon
from WallDit_QT import *

# All hope is lost, abandon now

counter = 0 # Counter for checking how many posts that don't fit parameters were skipped

user_agent = "windows/linux:WallDit:v1 (by /u/FilthyPeasantt)"
r = praw.Reddit(user_agent = user_agent)

# which subreddit the program gets the image from
def get_subreddit_name(window):
    window.handle_status_label("Getting subreddit")
    subreddit = r.get_subreddit(window.handle_subreddit_line())
    return subreddit

# what type of post to look for (hot/top/controversial/etc...)
def get_post_type(window):
    type_input = window.handle_post_type_combo_box()
    return type_input

# Checks if the submission fits the specified parameters
def is_ok_submission_url(window, submission, link_search_limit):
    suffixes = ['.gif', '.gifv', '.com']
    dont_include = {'/a/', '/gallery/', 'gfy', 'deviantart', 'reddit', 'artstation', 'flickr'}
    url = submission.url
    global counter
    if any(term in url for term in dont_include) or url.endswith(tuple(suffixes)) or not url:
        counter = counter +1
        return False
    elif submission.over_18 and window.handle_nsfw_checkbox() == False:
        counter = counter +1
        return False
    elif counter == link_search_limit:
        window.handle_status_label("Error: Submission are all invalid, up the counter or try again")
    else:
        return True

# Gets links that meet the specified parameter requirements
def get_link(window):
    link_search_limit = window.handle_post_spinbox() # how many links it's gonna search for images that fit the criteria till it gives up and dies in a fire

    subreddit = get_subreddit_name(window)
    window.handle_progress_bar(5)

    p_type = get_post_type(window) 
    window.handle_progress_bar(10)

    window.handle_status_label("Getting url")
    post_types = ['get_hot', 'get_top_from_hour', 'get_top_from_day', 'get_top_from_week', 'get_top_from_month', 'get_top_from_year', 'get_top_from_all']

    for submission in getattr(subreddit, post_types[p_type])(limit = link_search_limit):
        if is_ok_submission_url(window, submission, link_search_limit):
            window.handle_progress_bar(25)
            return submission.url

# Downloads image
def get_image_download(window, image_name):
    url = get_link(window)
    window.handle_status_label("Downloading image")

    if ('i.' not in url and 'imgur' in url) and url:
        url += ".png"

    response = requests.get(url, stream=True)

    with open(image_name, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return url

# Checks for internet connectivity finish this shit when u wake up
def check_connectivity(window):
    window.handle_status_label("Checking internet connection")
    try: 
        req = requests.get('http://www.google.com', timeout=1)
        req.raise_for_status()
        return True
    except requests.HTTPError as e:
        print("Checking internet connection failed, status code {0}".format(e.response.status_code))
    except requests.ConnectionError:
        print("No internet connection is available.")
        window.handle_status_label("No internet connection is available")
        return False

# Seriously, don't ask, yet another windows function
def get_path_to_folder():
    desktop_pidl = shell.SHGetFolderLocation (0, shellcon.CSIDL_DESKTOP, 0, 0)
    pidl, display_name, image_list = shell.SHBrowseForFolder (0, desktop_pidl, "Choose a folder", 0, None, None)

    return shell.SHGetPathFromIDList(pidl)

def save_image(window):
    date = time.strftime("%Y-%d-%m-%H-%M")
    image_ext = ".png"
    image = "DownloadedImage" + date + image_ext

    # Adds the date and time to the downloaded image, before moving it to the Pictures directory
    os.rename("DownloadedImage.png", image)

    cwd = os.getcwd()
    path = os.path.join(cwd, image)

    path_to_folder = str(get_path_to_folder())

    newstr = path_to_folder.replace("b", "")
    nnewstr = newstr.replace("'", "")
    # Copies image to a dir
    shutil.copy(path, nnewstr)

# Sets downloaded image as wallpaper
def set_wallpaper(window):
    cwd = os.getcwd()
    
    image_name = "DownloadedImage.png"
    path = os.path.join(cwd, image_name)
    url = get_image_download(window, image_name)
    window.handle_progress_bar(30)
    window.handle_status_label("Setting image as desktop background...")
    if ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0): # Runs on magic, do not touch
        window.handle_progress_bar(30)
        window.handle_status_label("Desktop background set successfully.")
    else:
        print("\n\nUh uh... Something went wrong.\nSend an email to matas234@gmail.com or message me on reddit /u/FilthyPeasantt")
        print("\n\nSend this: ", url)