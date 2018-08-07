#!/usr/bin/env python3
import argparse
import math
import os

FILETYPES = {
    ("jpg", "png", "gif", "jpeg"): "Pictures",
    ("mp4", "mkv", "avi", "webm", "flv", "srt"): "Video",
    ("pdf", "doc", "docx", "pptx", "xlst", "odt", "csv", "txt", "md"): "Documents",
    ("zip", "tar", "7z", "xz", "gz", "bz", "tgz"): "Archives",
    ("mp3", "flac", "ogg", "wav", "m3u8", "pls", "oga", "m4a"): "Music",
    ("epub", "fb2", "mobi"): "Books",
    ("json", "ini", "conf", "yaml", "toml", "xml", "ovpn"): "Config",
    ("html", "htm", "mhtml", "css", "js"): "Web",
    ("ttf", "otf", "woff2"): "Fonts",
    ("sh", "py", "rb", "pl", "php"): "Scripts",
    ("deb", "rpm", "dmg", "pkg"): "Packages",
    ("bak", "bk", "backup"): "Backups",
    ("bin", "exe", "dll", "dat"): "Binaries",
    ("img", "iso"): "Images",
    ("sql", "sqlite", "db"): "Databases",
    ("pub", "asc", "gpg"): "Keys",
    ("apk"): "Android",
    ("torrent"): "Torrent",
    ("log"): "Logs",
    ("jar"): "Java",
    ("tdesktop-theme", "tdesktop-palette"): "Telegram Desktop themes",
    ("attheme"): "Telegram Android themes",
    ("psd"): "Photoshop"
}

class color:
    """Terminal ANSI color codes
    
    Full table: https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
    """
    red = '\033[91m'
    green = '\033[92m'
    yellow = '\033[93m'
    blue = '\033[94m'
    default = '\033[0m'

args = argparse.ArgumentParser()
args.add_argument("directory")
args.add_argument("-d", "--destination", help="directory in which the sorted files will be moved", metavar="PATH")
args.add_argument("-t", "--test-run", help="just print what will be done", action="store_true")
args.add_argument("-f", "--force", help="overwrite files if exist", action="store_true")
args.add_argument("-i", "--interactive", help="ask for an action (skip/overwrite) for every file conflict", action="store_true")
args.add_argument("-n", "--include-hidden", help="include files with leading dot in the filename", action="store_true")
options = args.parse_args()

WORKING_DIR = os.path.abspath(os.path.expanduser(options.directory))
if options.destination:
    DESTINATION_DIR = os.path.abspath(os.path.expanduser(options.destination))
else:
    DESTINATION_DIR = WORKING_DIR

def get_file_type(filename):
    """Get file type by its extension"""
    file_extension = filename.lower().split(".")[-1]
    for some_type_extensions in FILETYPES.keys():
        if (file_extension in some_type_extensions) or (file_extension == some_type_extensions):
            return FILETYPES[some_type_extensions]

def get_file_size(path):
    """Get file size in human-readable format (MB, GB, etc)"""
    size_in_bytes = os.stat(path).st_size
    if size_in_bytes == 0:
        return "empty"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_in_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_in_bytes / p, 2)
    return "{} {}".format(s, size_name[i])

def error(error_text):
    """Print text with "Error: " prefix and exit with code 1"""
    print(color.red+"Error: "+str(error_text)+color.default)
    exit(1)

if not os.path.isdir(DESTINATION_DIR) and options.destination:
    error("destination directory doesn't exist: {}".format(DESTINATION_DIR))
if not os.path.isdir(WORKING_DIR):
    error("directory doesn't exist: {}".format(WORKING_DIR))


for current_filename in os.listdir(WORKING_DIR):
    # Get absolute file path
    current_file_path = os.path.abspath(os.path.join(WORKING_DIR, current_filename))
    
    # Skip folders
    if not os.path.isfile(current_file_path):
        continue
    # Skip hidden files by default
    if (not options.include_hidden) and current_filename[0] == ".": 
        continue
    # Skip unknown file types
    file_type = get_file_type(current_filename)
    if not file_type:
        continue

    print("{filename} {size} -> {file_type}".format(
        filename=current_filename,
        size=color.blue+"("+get_file_size(current_file_path)+")"+color.default, 
        file_type=color.green+file_type+color.default)
    )
    # Break switch
    if options.test_run:
        continue

    # Create folder if doesn't exist
    try:
        os.mkdir(os.path.join(DESTINATION_DIR, file_type))
    except FileExistsError:
        pass
    
    final_destination = os.path.join(DESTINATION_DIR, file_type, current_filename)

    if os.path.isfile(final_destination):
        final_file_relative_path = os.path.join(file_type, current_filename)
        message = "{cr} Conflict:{cd} {final_destination} {d_size} already exists.".format(
            cr=color.red,
            cd=color.default,
            final_destination=final_file_relative_path,
            d_size=color.blue+"("+get_file_size(final_destination)+")"+color.default,
        )
        if options.interactive:
            # Ask user for an action
            print(message)
            yn = input("{cy}  Overwrite it? [y/N]: {cd}".format(cy=color.yellow, cd=color.default)).lower()
            if yn == "y":
                print("   File has been overwritten.")
                pass
            else:
                print("   File has been skipped.")
                continue
        elif options.force:
            pass
        else:
            print(message)
            print("  File has been skipped. Use -f/--force or -i/--interactive")
            continue

    # Move file to corresponding folder
    try:
        os.rename(current_file_path, final_destination)
    except OSError as e:
        error(e)

