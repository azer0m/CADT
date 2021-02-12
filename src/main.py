import sys
import logging
from cadtlib.fnxs import *
from canvasapi import Canvas

def main(CANVAS_URL, ACCESS_TOKEN):
    # Create Canvas object to fetch data
    canvas = Canvas(CANVAS_URL, ACCESS_TOKEN)
    # Create folder for all files to be downloaded
    downloads_path = "Downloaded_Files"
    # May get Unauthorized exception if trying to access Courses
    try:
        all_courses = canvas.get_courses()
    except Unauthorized:
        print(f"Unauthorized Course access. This is unexpeted behavior!")
    else:
        for course in all_courses:
            course_name = course.name.replace(" ", "_")
            course_term = convert_datetime(course.start_at)
            # Download files
            file_folder_path = os.path.join(downloads_path, course_term,
                                            course_name, "Files")
            download_files(course, file_folder_path, True)
            # Donwnload submissions
            assignments_folder_path = os.path.join(downloads_path,
                                                   course_term, course_name,
                                                   "Assignments")
            download_submissions(course, assignments_folder_path, True)
    # Finally, remove empty folders
    remove_empty_folders("Downloaded_Files/")

# if __name__ == "__main__":
#     # Institution's canvas URL
#     CANVAS_URL = "https://bcourses.berkeley.edu/"
#     # Personal Canvas access token
#     # TO-DO: Create GUI to input TOKEN
#     ACCESS_TOKEN = "1072~3nOf9JP8dkLXiSDyRSsAHAtFYSjFbOkyXOTli4YxQTVUY9OSoPMjBDZ6se47Kjd1"
#     if os.path.isfile("output.log"):
#         print("Deleting old output.log file. . .")
#         os.remove("output.log")
#     # logger = logging.getLogger()
#     # logger.setLevel(logging.DEBUG)
#     # output_file_handler = logging.FileHandler(filename="output.log", mode="w")
#     # # stdout_handler = logging.StreamHandler(sys.stdout)
#     # logger.addHandler(output_file_handler)
#     # # logger.addHandler(stdout_handler)

#     # main(CANVAS_URL, ACCESS_TOKEN, logger=logger)
#     main(CANVAS_URL, ACCESS_TOKEN)

### DEPRECATED ###

    # try:
    #     all_courses = canvas.get_courses()
    #     for course in all_courses:
    #         course_name = course.name.replace(" ", "_")
    #         course_term = convert_datetime(course.start_at)
            
    #         # file_folder_path = os.path.join(downloads_path, course_term,
    #         #                                 course_name, "Files")
    #         # create_folder(file_folder_path)
    #         # download_files(course, file_folder_path, True)

    #         assignments_folder_path = os.path.join(downloads_path,
    #                                                course_term, course_name,
    #                                                "Assignments")
    #         download_submissions(course, assignments_folder_path, True)

    #         # # course_term_subfolder = os.path.join(downloads_path, course_term)
    #         # # create_folder(course_term_subfolder)
    #         # # course_files = course.get_files()
    #         # file_folder_path = os.path.join(downloads_path, course_term,
    #         #                            course_name, "Files")
    #         # create_folder(file_folder_path)
    #         # # download_files(course_files, file_folder_path, course.name, True)
    #         # download_files(course, file_folder_path, True)
    # except Unauthorized:
    #     print(f"Unauthorized Course access. This is unexpected behavior!")