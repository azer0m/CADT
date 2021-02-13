from cadtlib.fnxs import *
from canvasapi import Canvas

def main(CANVAS_URL, ACCESS_TOKEN):
    # Create Canvas object to fetch data
    canvas = Canvas(CANVAS_URL, ACCESS_TOKEN)
    # Folder for all files to be downloaded
    downloads_path = "Downloaded_Files"

    # Download submissions by using User object
    try:
        user = canvas.get_current_user()
    except Unauthorized:
        print_and_log(f"Unauthorized User access. This is unexpeted behavior!")
    download_submissions(user, downloads_path, verbose=True)

    try:
        all_courses = canvas.get_courses()
    except Unauthorized:
        print_and_log(f"Unauthorized Course access. This is unexpeted behavior!")
    download_files(all_courses, downloads_path, verbose=True)