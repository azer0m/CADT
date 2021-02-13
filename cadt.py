"""
Author: Ahmed Malik
github: https://github.com/azer0m
"""

from cadtlib.fnxs import print_and_log
import os
from credentials import CANVAS_URL, ACCESS_TOKEN
from src.main import main

# Delete old output.log file
if os.path.isfile("output.log"):
    print_and_log("Deleting old output.log file. . .")
    # print("Deleting old output.log file. . .")
    os.remove("output.log")
# Raise error if user did not input CANVAS_URL or ACCESS_TOKEN
if CANVAS_URL == "" or ACCESS_TOKEN == "":
    raise ValueError("CANVAS_URL and ACCESS_TOKEN must be filled "+\
                      "out in credentials.py before proceeding!")

main(CANVAS_URL, ACCESS_TOKEN)