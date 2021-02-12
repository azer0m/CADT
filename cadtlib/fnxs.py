import os
import requests
import logging
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
    # May get Unauthorized exception if trying to access Files for some courses
    try:
        for file in all_files:
            total_size += file.get_size()
            print(f"CURR SIZE: {total_size} BYTES")
    except Unauthorized:
        print(f"Unauthorized Files access for {course_name}!")
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
        print(f"{folder_path} folder doesn't exist. Creating folder. . .")
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

def download_files(course, folder_path, verbose=False):
    """
    Downloads all files in course.

    Parameters
    ----------
    course : canvasapi.course.Course
        Course object from which we can fetch Files objects
    folder_path : str
        Path to where files will be downloaded
    verbose : bool, optional
        If True, prints name of file currently being downloaded, by default False
    """
    create_folder(folder_path)
    course_files = course.get_files()
    # May get Unauthorized exception if trying to access Files for some courses
    try:
        for file in course_files:
            fname = str(file)
            file_path = os.path.join(folder_path, fname)
            file_path = verify_file_path(file_path)
            if verbose:
                with open("output.log", "a") as f:
                    f.write(f"Downloading {fname}. . .\n")
                print(f"Downloading {fname}. . .")
            file.download(file_path)
    except Unauthorized:
        print(f"Unauthorized Files access for {course.name}")

def download_submissions(course, folder_path, verbose=False):
    """
    Downloads all submissions in course.

    Parameters
    ----------
    course : canvasapi.course.Course
        Course object from which we can fetch Submission objects
    folder_path : str
        Path to where submissions will be downloaded
    verbose : bool, optional
        If True, prints name of submission currently being downloaded, by default False
    """
    all_assignments = course.get_assignments()
    try:
        # Iterate through all assignments
        for assignment in all_assignments:
            assignment_subfolder = str(assignment).replace(" ", "_")
            assignment_subfolder_path = os.path.join(folder_path, 
                                                     assignment_subfolder)
            create_folder(assignment_subfolder_path)
            assignment_submissions = assignment.get_submissions()
            try:
                # Iterate through all submissions
                for submission in assignment_submissions:
                    # Will get AttributeError if attachments do not exist
                    try:
                        # Iterate through all attachments
                        for attachment in submission.attachments:
                            # Get attachment URL and download to location
                            attachment_url = attachment["url"]
                            response = requests.request("GET", attachment_url)
                            attachment_fname = attachment["filename"]
                            location = os.path.join(assignment_subfolder_path,
                                                    attachment_fname)
                            if verbose:
                                with open("output.log", "a") as f:
                                    f.write(f"Downloading {attachment_fname}. . .\n")
                                print(f"Downloading {attachment_fname}. . .")
                            with open(location, "wb") as file_out:
                                file_out.write(response.content)
                    except AttributeError:
                        print(f"No attachments for {assignment_subfolder}!")
            except Unauthorized:
                print(f"Unauthorized Submissions access for {course.name}")
    except Unauthorized:
        print(f"Unauthorized Assignments access for {course.name}")

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
        print(f"Removing empty folder: {root}")
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