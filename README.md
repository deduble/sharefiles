# Sharefiles

sharefiles is a Python 3 library and script for easily sharing files of directory on network.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install sharefiles.

```bash
pip install git+git://github.com/deduble/sharefiles.git
```

## Usage

Execute the installed binary


```bash
sharefiles
```

or

```bash
python -m sharefiles

```

Alternatively you can share custom directories and with custom port
```bash
sharefiles 8080 --directory /path/to/directorywanted/directory
```
## Disclaimer
Anyone with the access to your network can reach the files. This is just uploading enabled handler on http.server. I made this for personal use earlier. You are welcome to contribute.

## License
[MIT](https://choosealicense.com/licenses/mit/)