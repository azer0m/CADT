import os
from canvasapi.course import CourseNickname
import requests
from canvasapi.exceptions import Unauthorized

def calc_files_size(all_files, total_size, course_name):
    """
    Calculates size of all files on canvas for user. May be useful to ensure
    there is enough space on computer to download all files.

    TO-DO: There are some issues: some file sizes cannot be acquired. Figure out
    why and fix.

    Parameters
    ----------
    all_files : PaginatedList of File
        Contains all File objects for a given course
    total_size : int
        This function is used by iterating through all files for all courses,
        and so as to not lose track of total file size [bytes] so far, it is passed back in
        for every new course; naturally, it should start at 0
    course_name : str
        Name of current course associated with all_files

    Returns
    -------
    total_size : int
        Total file size [bytes] for files in courses seen so far
    """
    try:
        for file in all_files:
            total_size += file.get_size()
            print_and_log(f"CURR SIZE: {total_size} BYTES")
    except Unauthorized:
        print_and_log(f"Unauthorized Files access for {course_name}!")
    return total_size

def create_folder(folder_path):
    """
    Create a folder if it does not exist.

    Parameters
    ----------
    folderPath : str
        Relative path to folder
    """
    if not os.path.isdir(folder_path):
        print_and_log(f"{folder_path} folder doesn't exist. Creating folder. . .")
        os.makedirs(folder_path) # Create all folders along path

def convert_datetime(datetime):
    """
    Convert datetime of format YYYY-MM-DDTHH:MM:SS to semester term and year
    (e.g. Fall 2015).

    This function assumes spring semester from January-May, summer semester
    from June-July, and fall semester from August-September.

    TO-DO: Modify function to handle different types of terms (i.e. quarter system).

    Parameters
    ----------
    datetime : str
        Start date for course of format YYYY-MM-DDTHH:MM:SS

    Returns
    -------
    subfolder_name : str
        Name of subfolder for term corresponding to datetime
    """
    year = datetime[:4]
    month = int(datetime[5:7])

    # January - May
    if 1 <= month <= 5:
        term = "Spring"
    # June and July
    elif 6 <= month <= 7:
        term = "Summer"
    # August - December
    elif 8 <= month <= 12:
        term = "Fall"
    else:
        term = "Unknown_Term"
    
    subfolder_name = term+"_"+year
    return subfolder_name

def download_files(all_courses, downloads_path, verbose=False):
    """
    Download all files across all courses.

    Parameters
    ----------
    all_courses : PaginatedList of Course objects
        All active courses for current user
    downloads_path : str
        Start of path where files will be downloaded to
    verbose : bool, optional
        If True, prints name of file currently being downloaded, by default
        False
    """
    for course in all_courses:
        course_name = course.name.replace(" ", "_")
        course_term = convert_datetime(course.start_at)
        file_folder_path = os.path.join(downloads_path, course_term,
                                        course_name, "Files")
        course_files = course.get_files()
        try:
            for file in course_files:
                fname = str(file)
                file_path = os.path.join(file_folder_path, fname)
                create_folder(file_folder_path)
                file_path = verify_file_path(file_path)
                if verbose:
                    print_and_log(f"Downloading {fname}. . .")
                file.download(file_path)
        except Unauthorized:
            print_and_log(f"Unauthorized Files access for {course.name}")

def download_submissions(user, downloads_path, verbose=False):
    """
    Given a user object, gets all submissions associated with user, including
    Canvas export zip files.

    Parameters
    ----------
    user : canvasapi.user.User
        User object from which all folder and file access is exposed
    downloads_path : str
        Start of path where submission files will be downloaded to
    verbose : bool, optional
        If True, prints name of file currently being downloaded, by default
        False
    """
    try:
        all_folders = user.get_folders()
    except Unauthorized:
        print_and_log(f"Unauthorized Folders access. This is unexpected behavior!")
    for folder in all_folders:
        folder_term = convert_datetime(folder.created_at)
        try:
            all_files = folder.get_files()
        except Unauthorized:
            print_and_log(f"Unauthorized Files access for {folder.name}!")
        for file in all_files:
            folder_name = folder.name.replace(" ", "_")
            fname = file.display_name
            file_url = file.url
            if folder.name == "data exports":
                download_folder = os.path.join(downloads_path, folder_name)
            else:
                download_folder = os.path.join(downloads_path, folder_term,
                                               folder_name, "Submissions")
            file_path = os.path.join(download_folder, fname)
            create_folder(download_folder)
            response = requests.request("GET", file_url)
            if verbose:
                print_and_log(f"Downloading {fname}. . .")
            with open(file_path, "wb") as file_out:
                file_out.write(response.content)

def print_and_log(text, output_file="output.log"):
    """
    Prints to console and logs to output.log file.

    Parameters
    ----------
    text : str
        Text to be printed and logged
    output_file : str, optional
        Name of log file, by default "output.log"
    """
    with open(output_file, "a") as f:
        f.write(text+"\n")
    print(text)

def remove_empty_folders(root):
    """
    Recursively remove empty folders in Downloaded_Files.

    Parameters
    ----------
    root : str
        Directory to check for and remove in need be
    """
    # If root doesn't exist, then don't do anything
    if not os.path.isdir(root):
        return

    files = os.listdir(root) # Get all items in current directory
    if len(files): # If there are items
        for f in files: # Iterate through them
            curr_path = os.path.join(root, f) # Get path to ith item
            if os.path.isdir(curr_path): # If it's a directory
                remove_empty_folders(curr_path) # Recursively remove folders
    
    files = os.listdir(root)
    # If the folder is empty and not the Downloaded_Files/ folder
    if len(files) == 0 and root != "Downloaded_Files/":
        print_and_log(f"Removing empty folder: {root}")
        os.rmdir(root)

def verify_file_path(file_path):
    """
    Verifies file path is unique. If not, this function modifies the file name
    such that downloading the file does not overwrite a previous file with the
    same name. In most cases, the files are probably the same. But, in the case
    they are not, this function ensures all unique files will be downloaded.

    TO-DO: This function appends a copy number to the end of the filename
    (pre-extension), but it doesn't modify a copy number if exists already.
    For example, if a file FILE_1.pdf exists, this function will produce
    FILE_1_2.pdf.

    Parameters
    ----------
    file_path : str
        Relative path for the file being downloaded, ending in the file name

    Returns
    -------
    file_path : str
        Modifed relative path for the file being downloaded, if previous
        file_path exists
    """
    if os.path.isfile(file_path):
        copy_num = 1 # Number of copy currently being downloaded
        while os.path.isfile(file_path):
            # Finds the rightmost ".", can add copy number before this index
            extension_idx = file_path.rfind(".")
            # If the file does have an extension (some don't)
            if extension_idx:
                # Add _{copy_num} right before extension
                file_path = file_path[0:extension_idx]+f"_{copy_num}"+\
                            file_path[extension_idx:]
            # If no extension
            else:
                # Just add _{copy_num} to end
                file_path += f"_{copy_num}"
            copy_num += 1
    return file_path