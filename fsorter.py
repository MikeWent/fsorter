#!/usr/bin/env python3
import argparse
import os

filetypes = {
    ("jpg", "png", "gif", "jpeg"): "Pictures",
    ("mp4", "mkv", "avi", "webm", "flv"): "Videos",
    ("pdf", "doc", "docx", "pptx", "odt", "csv", "txt", "epub", "fb2", "md"): "Documents",
    ("zip", "tar", "7z", "xz", "gz", "bz", "tgz"): "Archives",
    ("mp3", "flac", "ogg", "wav", "m3u8", "pls"): "Music",
    ("json", "ini", "conf", "yaml", "toml", "xml"): "Configs",
    ("html", "htm", "css", "js"): "Web",
    ("sh", "py", "rb", "pl"): "Scripts",
    ("deb", "rpm", "dmg", "pkg"): "Packages",
    ("bak", "bk", "backup"): "Backups",
    ("bin", "exe", "dll"): "Binaries",
    ("sql", "sqlite"): "Databases",
    ("pub", "asc"): "Keys",
    ("apk"): "Android",
    ("log"): "Logs",
    ("jar"): "Java"
}

args = argparse.ArgumentParser()
args.add_argument("directory")
args.add_argument("-t", "--test-run", help="just print what will be done", action="store_true")
args.add_argument("-i", "--include-hidden", help="include files with leading dot in the filename", action="store_true")
args.add_argument("-d", "--destination", help="directory in which the sorted files will be moved", metavar="PATH")
options = args.parse_args()

working_dir = os.path.abspath(os.path.expanduser(options.directory))
if options.destination:
    desination_dir = os.path.abspath(os.path.expanduser(options.destination))
else:
    desination_dir = working_dir

def get_file_type(filename):
    file_extension = filename.lower().split(".")[-1]
    for some_type_extensions in filetypes.keys():
        if file_extension in some_type_extensions or file_extension == some_type_extensions:
            return filetypes[some_type_extensions]

for file in os.listdir(options.directory):
    absolute_file_path = os.path.abspath(os.path.join(options.directory, file))
    # Skip folders
    if not os.path.isfile(absolute_file_path):
        continue
    # Skip hidden files by default
    if (not options.include_hidden) and file[0] == ".": 
        continue
    file_type = get_file_type(file)
    # Skip unknown file types
    if not file_type:
        continue
    print(file, "->", file_type)
    # Break switch
    if options.test_run:
        continue
    # Create folder if doesn't exist
    try:
        os.mkdir(os.path.join(desination_dir, file_type))
    except FileExistsError:
        pass
    # Move file to corresponding folder
    final_destination = os.path.join(desination_dir, file_type, file) 
    try:
        os.rename(absolute_file_path, final_destination)
    except OSError as e:
        print("Error: {}".format(e))
