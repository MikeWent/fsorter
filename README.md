# Fsorter

A file sort utility which helps you to organize your "Downloads" folder, for example.

Requirements: Python 3.

## How to use

Simply run `fsorter.py` with directory specified:

```bash
./fsorter.py ~/Downloads
```

Example output:

```
funnycatHD.jpg (4.95 MB) -> Pictures
install.sh (12.1 KB) -> Scripts
vacation_20180801.mp4 (182.7 MB) -> Video
dump.bak (5.32 MB) -> Backups
blog_posts.sql (578.64 KB) -> Databases
notes.txt (832.83 KB) -> Documents
copy81.zip (355.5 KB) -> Archives
```


## More info

```
usage: fsorter.py [-h] [-d PATH] [-t] [-f] [-i] [-n] directory

positional arguments:
  directory

optional arguments:
  -h, --help            show this help message and exit
  -d PATH, --destination PATH
                        directory in which the sorted files will be moved
  -t, --test-run        just print what will be done
  -f, --force           overwrite files if exist
  -i, --interactive     ask for an action (skip/overwrite) for every file
                        conflict
  -n, --include-hidden  include files with leading dot in the filename
```

## License

MIT
