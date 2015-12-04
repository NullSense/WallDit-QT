import praw
import requests
import shutil
import ctypes
import os
from WallDit_QT import *

# To future me: sorry for such hacky code :c

user_agent = "windows/linux:WallDit:v0.2 (by /u/FilthyPeasantt)"
r = praw.Reddit(user_agent = user_agent)

# which subreddit the program gets the image from
def get_subreddit_name(window):
    subreddit = r.get_subreddit(window.handle_subreddit_line())
    print("subreddit: " + str(subreddit))
    return subreddit

# what type of post to look for (hot/top/controversial/etc...)
def get_post_type(window):
    type_input = window.handle_post_type_combo_box()
    print("post type number: " + str(type_input))
    return type_input

def is_ok_submission_url(submission):
    suffixes = ['.gif', '.gifv', '.com']
    dont_include = {'/a/', '/gallery/', 'gfy', 'deviantart', 'reddit'}

    url = submission.url
    if any(term in url for term in dont_include) or url.endswith(tuple(suffixes)) or not url:
        print("\n\nSubmission ERROR: image a(n) album/gif, from deviantart or empty.")
        return False
    else:
        print("Submission: no errors.\n\n")
        return True

def get_link(window):
    link_search_limit = window.handle_post_spinbox() # how many links it's gonna search for images that fit the criteria till it gives up
    print("link search limit: " + str(link_search_limit))
    subreddit = get_subreddit_name(window)
    p_type = get_post_type(window) 
    print("p_type: " + str(p_type))
    post_types = ['get_hot', 'get_top_from_hour', 'get_top_from_day', 'get_top_from_week', 'get_top_from_month', 'get_top_from_year', 'get_top_from_all']

    for submission in getattr(subreddit, post_types[p_type])(limit = link_search_limit):
        if "." not in submission.title: 
            print("\nKarma: {submission}\nNSFW: {submission.over_18}".format(submission=submission))
        if is_ok_submission_url(submission):
            return submission.url

def get_image_download(window):
    url = get_link(window)

    has_to_contain = ['.png', '.jpg', '.bmp']
    
    if 'i.' not in url and 'imgur' in url:
        url += ".png"

    print("Downloading Image...")

    response = requests.get(url, stream = True)
    with open('DownloadedImage.png', 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    return url

def set_wallpaper(window):
    cwd = os.getcwd()
    path = os.path.join(cwd, "DownloadedImage.png")
    url = get_image_download(window)
    print("Setting image as desktop background...")
    if ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0):
        print("Desktop background set successfully.")
    else:
        print("\n\nUh uh... Something went wrong.\nSend an email to matas234@gmail.com or message me on reddit /u/FilthyPeasantt")
        print("\n\nSend this: ", url)