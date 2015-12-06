import praw
import requests
import shutil
import ctypes
import os
import time
from WallDit_QT import *

# All hope is lost, abandon now

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
def is_ok_submission_url(window, submission):
    suffixes = ['.gif', '.gifv', '.com']
    dont_include = {'/a/', '/gallery/', 'gfy', 'deviantart', 'reddit'}
    url = submission.url

    if any(term in url for term in dont_include) or url.endswith(tuple(suffixes)) or not url:
        print("\n\nSubmission ERROR: image a(n) album/gif, from deviantart or empty.")
        return False
    if submission.over_18 and window.handle_nsfw_checkbox() == False:
        print("Submission is over 18 and NSFW is unchecked.")
        return False
    else:
        print("Submission: no errors.\n\n")
        return True

# Grabs link
def get_link(window):
    link_search_limit = window.handle_post_spinbox() # how many links it's gonna search for images that fit the criteria till it gives up and dies in a fire

    subreddit = get_subreddit_name(window)
    window.handle_progress_bar(5)

    p_type = get_post_type(window) 
    window.handle_progress_bar(10)

    window.handle_status_label("Getting url")
    post_types = ['get_hot', 'get_top_from_hour', 'get_top_from_day', 'get_top_from_week', 'get_top_from_month', 'get_top_from_year', 'get_top_from_all']

    for submission in getattr(subreddit, post_types[p_type])(limit = link_search_limit):
        if "." not in submission.title: 
            print("\nKarma: {submission}\nNSFW: {submission.over_18}".format(submission=submission))
            window.handle_status_label("\nKarma: {submission}\nNSFW: {submission.over_18}".format(submission=submission))
        if is_ok_submission_url(window, submission):
            window.handle_progress_bar(25)
            return submission.url

# Downloads image
def get_image_download(window):
    url = get_link(window)
    window.handle_status_label("Downloading image")

    if ('i.' not in url and 'imgur' in url) and url:
        url += ".png"

    response = requests.get(url, stream=True)
    with open('DownloadedImage.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return url

# Checks for internet connectivity
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

# Sets downloaded image as wallpaper
def set_wallpaper(window):
    cwd = os.getcwd()
    path = os.path.join(cwd, "DownloadedImage.png")
    url = get_image_download(window)
    window.handle_progress_bar(30)
    print("Setting image as desktop background...")
    window.handle_status_label("Setting image as desktop background...")
    if ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0): # Runs on magical pony farts, do not touch
        window.handle_progress_bar(30)
        print("Desktop background set successfully.")
        window.handle_status_label("Desktop background set successfully.")
    else:
        print("\n\nUh uh... Something went wrong.\nSend an email to matas234@gmail.com or message me on reddit /u/FilthyPeasantt")
        print("\n\nSend this: ", url)