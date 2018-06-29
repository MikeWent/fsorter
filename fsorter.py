#!/usr/bin/env python3
import argparse
import math
import os

FILETYPES = {
    ("jpg", "png", "gif", "jpeg"): "Pictures",
    ("mp4", "mkv", "avi", "webm", "flv"): "Video",
    ("pdf", "doc", "docx", "pptx", "xlst", "odt", "csv", "txt", "md"): "Documents",
    ("zip", "tar", "7z", "xz", "gz", "bz", "tgz"): "Archives",
    ("mp3", "flac", "ogg", "wav", "m3u8", "pls", "oga", "m4a"): "Music",
    ("epub", "fb2", "mobi"): "Books",
    ("json", "ini", "conf", "yaml", "toml", "xml"): "Config",
    ("html", "htm", "mhtml", "css", "js"): "Web",
    ("ttf", "otf", "woff2"): "Fonts",
    ("sh", "py", "rb", "pl", "php"): "Scripts",
    ("deb", "rpm", "dmg", "pkg"): "Packages",
    ("bak", "bk", "backup"): "Backups",
    ("bin", "exe", "dll", "dat"): "Binaries",
    ("img", "iso"): "Images",
    ("sql", "sqlite"): "Databases",
    ("pub", "asc", "gpg"): "Keys",
    ("apk"): "Android",
    ("torrent"): "Torrent",
    ("log"): "Logs",
    ("jar"): "Java"
}

args = argparse.ArgumentParser()
args.add_argument("directory")
args.add_argument("-t", "--test-run", help="just print what will be done", action="store_true")
args.add_argument("-i", "--include-hidden", help="include files with leading dot in the filename", action="store_true")
args.add_argument("-f", "--force", help="overwrite files if exist", action="store_true")
args.add_argument("-d", "--destination", help="directory in which the sorted files will be moved", metavar="PATH")
options = args.parse_args()

WORKING_DIR = os.path.abspath(os.path.expanduser(options.directory))
if options.destination:
    DESTINATION_DIR = os.path.abspath(os.path.expanduser(options.destination))
else:
    DESTINATION_DIR = WORKING_DIR

def get_file_type(filename):
    """Get file type by its name"""
    file_extension = filename.lower().split(".")[-1]
    for some_type_extensions in FILETYPES.keys():
        if (file_extension in some_type_extensions) or (file_extension == some_type_extensions):
            return FILETYPES[some_type_extensions]

def get_file_size(filename):
    """Get file size in human-readable format (MB, GB, etc)"""
    size_in_bytes = os.stat(filename).st_size
    if size_in_bytes == 0:
        return "empty"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)
    return "{} {}".format(s, size_name[i])

for current_filename in os.listdir(WORKING_DIR):
    current_file_path = os.path.abspath(os.path.join(WORKING_DIR, current_filename))
    
    # Skip folders
    if not os.path.isfile(current_file_path):
        continue

    # Skip hidden files by default
    if (not options.include_hidden) and current_filename[0] == ".": 
        continue

    file_type = get_file_type(current_filename)
    # Skip unknown file types
    if not file_type:
        continue

    print(current_filename, "->", file_type)
    # Break switch
    if options.test_run:
        continue

    # Create folder if doesn't exist
    try:
        os.mkdir(os.path.join(DESTINATION_DIR, file_type))
    except FileExistsError:
        pass
    
    final_destination = os.path.join(DESTINATION_DIR, file_type, current_filename)
    # Ask user if file already exists
    if os.path.isfile(final_destination) and (not options.force):
        final_file_relative_path = os.path.join(file_type, current_filename)
        message = "File '{}' ({}) already exists.\nOverwrite it with '{}' ({})? [y/N]: ".format(
            final_file_relative_path, get_file_size(final_destination),
            current_filename, get_file_size(current_file_path)
        )
        yn = input(message).lower()
        if yn == "y":
            print("Done.")
            pass
        else:
            print("File skipped.")
            continue

    # Move file to corresponding folder
    try:
        os.rename(current_file_path, final_destination)
    except OSError as e:
        print("Error: {}".format(e))
