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
funnycat.jpg -> Pictures
install.sh -> Scripts
uninstall.sh -> Scripts
config.bak -> Backups
IMG_12542912.png -> Pictures
notes.txt -> Documents
```

## More info

```
usage: fsorter.py [-h] [-t] [-i] [-d PATH] directory

positional arguments:
  directory

optional arguments:
  -h, --help            show this help message and exit
  -t, --test-run        just print what will be done
  -i, --include-hidden  include files with leading dot in the filename
  -d PATH, --destination PATH
                        directory in which the sorted files will be moved
```

## License

MIT
